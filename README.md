# computing on TUB's HPC (High Performance Cluster)
## links
https://hpc.tu-berlin.de/doku.php

## access-rights
Tobias magically makes that you're granted permissions

## hardware on the cluster
(see: https://hpc.tu-berlin.de/doku.php?id=hpc:hardware)
* 132x MPP-Nodes with 40 threads, 256 Gb memory
* 20x GPU-Nodes with 40 threads, 512 GB memory, 2x NVIDIA Tesla P100 16GB
## ssh to the "frontend" == "gateway"
first give gateway your public ssh key  
`ssh-copy-id -i ~/.ssh/id_rsa.pub <TUBIT_NAME>@gateway.hpc.tu-berlin.de`  
log onto the gateway  
`ssh <TUBIT_NAME>@gateway.hpc.tu-berlin.de`  
## setup python environment on gateway
get miniconda  
`wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
install it  
`bash Miniconda3-latest-Linux-x86_64.sh`

