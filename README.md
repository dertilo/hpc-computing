# computing on TUB's HPC (High Performance Cluster)
## links
[tu-berlin-docu](https://hpc.tu-berlin.de/doku.php)  
[hpcc.usc.edu](https://hpcc.usc.edu/support/documentation/)  
[examples](https://hpc.uni.lu/users/docs/slurm_examples.html)
## hardware on the cluster
(see: https://hpc.tu-berlin.de/doku.php?id=hpc:hardware)
* 132x MPP-Nodes with 40 threads, 256 GB memory
* 20x GPU-Nodes with 40 threads, 512 GB memory, 2x NVIDIA Tesla P100 16GB
* smp002  and smp003 also have 2 GPUs 

## basic concepts
* the __frontend__ serves as a __gateway__ to the __computing nodes__ which themselves have no internet-connection
* you use the frontend only for: 
    1. transferring data 
    2. installing (python packages) -> __no__ computing on the frontened
    3. managing jobs via SLURM (just keep on reading, this will be explained)

## 1. setup connection with frontend / gateway
### access-rights
some admin needs to grant permissions to you

### 1.1 ssh to the frontend/gateway  
`ssh <TUBIT_NAME>@gateway.hpc.tu-berlin.de`  -> asks for tubit-password  

__optionally__ give the gateway your public ssh key so that you don't need to type your password  
on linux: `ssh-copy-id -i ~/.ssh/id_rsa.pub <TUBIT_NAME>@gateway.hpc.tu-berlin.de`  
on windows: `cat ~/.ssh/id_rsa.pub | ssh <TUBIT_NAME>@gateway.hpc.tu-berlin.de "cat >> ~/.ssh/authorized_keys"`    

### 1.2 copy files to gateway
* rsync over ssh [recommended]: `rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --exclude=.git <YOUR_FOLDER> <TUBIT_NAME>@gateway.hpc.tu-berlin.de:/home/users/<FIRST_LETTER>/<TUBIT_NAME>/`
* scp [__not__ recommended]: `scp -r /local/directory/ <TUBIT_NAME>@gateway.hpc.tu-berlin.de:/home/users/<FIRST_LETTER_OF_TUBIT_NAME>/<TUBIT_NAME>/`
  
#### _optionally_ mount the gateway/frontend to your local system  
could be very slow
`sshfs <TUBIT_NAME>@gateway.hpc.tu-berlin.de:/home/users/<FIRST_LETTER_OF_TUBIT_NAME>/<TUBIT_NAME> ~/hpc`  

## 2. SLURM
[SLURM](https://en.wikipedia.org/wiki/Slurm_Workload_Manager) is a Job-Scheduler and Workload Manager

### 2.1 interactive session on node:
`srun -t 30 -c 40 -n 1 --pty /bin/bash`
* max run- __t__ ime = 30 min
* __c__ ores = 40
* __n__ odes = 1
* __pty__ makes it interactive   

interactive session with __GPU__:  `srun -t 30 -c 40 -n 1 --gres=gpu:tesla:2 --partition=gpu --pty /bin/bash`  
### 2.2 misc SLURM-stuff
* status of jobs: `squeue`  
* shows your account-type: `sacctmgr show user <TUBIT_NAME> accounts`    
* cancel job `scancel <JOB_ID>`  
* one can have __multiple connections to a node__ simply open up another ssh-connection to the gateway and there you can: `ssh <NODE_NAME>` (example: `ssh node123`)

## 3. setup python environment
I recommend [miniconda](https://docs.conda.io/en/latest/miniconda.html) cause it installs its own python  
1. get miniconda `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`  
2. go on a cpu-node: `srun -t 30 -c 40 -n 1 --pty /bin/bash` -> _this is necessary cause the miniconda-install-script demands multiple cores (does some python multiprocessing) and on frontend number of processes to be used by single user is restricted_  
2.a) TODO: is it really necessary to install miniconda on the node?? using `OMP_NUM_THREADS=8` is not doing the trick?
3. install it: `OMP_NUM_THREADS=8 bash Miniconda3-latest-Linux-x86_64.sh`  

### 3.1 conda pip tensorflow issue 

if one wants __tensorflow__ it needs to be installed via: `conda install tensorflow`  
trying to install tensorflow via conda's pip leads to malformed link to `libstdc++.so.6`
so tensorflow dependency in requirements.txt wont work -> TODO: is this still relevant/uptodate?
### 3.2 torch + tensorflow issue
* working: `python -c "from tensorflow.python.client import device_lib; import torch; print(device_lib.list_local_devices())"`  
* not working: `python -c "import torch; from tensorflow.python.client import device_lib; print(device_lib.list_local_devices())"`    

-> TODO: confirm this is still an issue

## 4. hpc-tutorial
clone it: `git clone https://gitlab.tubit.tu-berlin.de/tilo-himmelsbach/hpc-computing.git`  
cd: `cd hpc-computing`  
create environment: `conda create -n hpc-tutorial python=3.7`  
activate environment: `conda activate hpc-tutorial`  
install dependencies: `pip install -r requirements.txt`  

### 4.1 monitoring example
#### 4.1.1 interactive 
open interactive session `srun -t 30 -c 40 -n 1 --pty /bin/bash`  
activate env: `source activate hpc-tutorial`  or  `~/miniconda/bin/conda activate hpc-tutorial`  
run: `python monitoring_example/monitor_matrix_multiplications.py`
#### 4.1.2 batch
on hpc-gateway we run hpc_job.sh with sbatch-command (still in `hpc-computing`-folder) run 

    sbatch hpc_job.sh hpc-tutorial monitoring_example/monitor_matrix_multiplications.py
    
* the `sbatch` command tells slurm to put our job in the queue  
* the job is defined by the shell-script and its arguments  
    * first arguement `hpc-tutorial` specifies the name of the conda-environment  
    * second argument is the python-script to be run
* the `monitor_matrix_multiplications.py` does some numpy matrix multiplications and creates a `cpu.png`- and `mem.png`-file; notice that numpy uses all 40 cores (4000% usage)
![cpu-usage](monitoring_example/cpu.png)
memory usage is around 4.3%
![mem-usage](monitoring_example/mem.png)

### 5 multiprocessing example
calculate mandelbrot-set  

![mandelbrot-formula](multiprocessing_example/mandelbrot_formula.svg)
-> this formula produces chaos == makes it unpredictable whether or not abs(z) converges or diverges after n-iterations; 
this chaotic behavior justifies a parallel computing -> no GPU even though its an image!
![mandelbrot-set](multiprocessing_example/mandelbrot_set.png)

#### the more cores the faster  
![cores-durations](multiprocessing_example/cores_durations.png)  
#### cpu-usage over time
![cpu-usage](multiprocessing_example/cpu.png)
![mem-usage](multiprocessing_example/mem.png)

## 6. pytorch-image-classifier-example
frog; truck; horse; frog  
![mem-usage](pytorch_image_classifier_example/example_images.png)  

#### interactive
on gateway  
`python pytorch_image_classifier_example/download_data.py`  
on GPU-node  
`srun -t 30 -c 40 -n 1 --gres=gpu:tesla:2 --partition=gpu --pty /bin/bash`  
`cd hpc-computing`  
`source activate hpc-tutorial`  
`python python pytorch_image_classifier_example/cifar10_tutorial.py `  
cpu-usage: towards the ends it high cause evaluation is done on CPUs not on GPUs!
![cpu-usage](pytorch_image_classifier_example/cpu.png)  
gpu-usage: around 14%
![mem-usage](pytorch_image_classifier_example/gpu_util.png)
gpu-memory-usage: some error in plot: y-axis displays MiB not percentage!!
![mem-usage](pytorch_image_classifier_example/gpu_mem.png)






