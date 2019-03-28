import time
from matplotlib import pyplot as plt
import numpy as np
from resmonres.monitor_system_parameters import MonitorSysParams

from multiprocessing_example.mandelbrot import mandelbrot_set
from multiprocessing_example.multiprocess_mandelbrot import multiprocessing_mandelbrot_set


def plot_cores_vs_computetime(cores_durations):
    cores, durations = zip(*cores_durations)
    f = plt.figure()
    f.add_axes()  # WTF !?
    axes = f.subplots()
    f.suptitle('cores vs computing-times')
    plt.plot(cores, durations,'.')
    axes.set_xlabel('num cores')
    axes.set_ylabel('duration in seconds')
    plt.savefig('./cores_durations.png')


if __name__ == '__main__':
    h = w = 1000
    ranges = (-2, 1, -1, 1)
    cores_durations = []
    with MonitorSysParams(log_path='.'):
        time.sleep(2)
        start = time.time()
        x = mandelbrot_set(ranges,width=w,height=h)
        duration = time.time() - start
        cores_durations.append((1,duration))
        print('single-core took: %0.2f seconds' % (duration))
        plt.imshow(np.mod(x,20)/20*255)
        plt.savefig('./mandelbrot_set.png')

        for num_cores in [2,4,8,16,32]:
            start = time.time()
            x = multiprocessing_mandelbrot_set(ranges, width=w, height=h, num_processes=num_cores)
            duration = time.time() - start
            cores_durations.append((num_cores, duration))
            print('%d-cores took: %0.2f seconds' % (num_cores, duration))
            plt.imshow(np.mod(x,20)/20*255)

        plt.savefig('./mandelbrot_set_multicore.png')
        time.sleep(10)

    plot_cores_vs_computetime(cores_durations)
