import time
from multiprocessing.pool import Pool
import multiprocessing
from typing import Iterable, Generator, List
import datetime
from matplotlib import pyplot as plt
import numpy as np
from resmonres.monitor_system_parameters import MonitorSysParams


def calc_num_it_where_absZ_smaller_threshold(c, threshold = 20, maxiter=300):
    z = c
    for it in range(maxiter):
        if abs(z) > threshold:
            return it
        z = z*z + c
    return 0


def mandelbrot_set(ranges, width, height):
    xmin, xmax, ymin, ymax = ranges
    real_part = np.linspace(xmin, xmax, width)
    imaginary_part = np.linspace(ymin, ymax, height)
    number_of_iterations_matrix = np.empty((height,width))
    for col in range(width):
        for row in range(height):
            complex_number = real_part[col] + 1j * imaginary_part[row]
            number_of_iterations_matrix[row, col] = calc_num_it_where_absZ_smaller_threshold(complex_number)

    return number_of_iterations_matrix


def compute_fun(c):
    return calc_num_it_where_absZ_smaller_threshold(c)

def compute_batch_fun(batch_idx_c_numbers):
    print(multiprocessing.current_process())
    # print(datetime.datetime.now())
    batch_idx, c_numbers = batch_idx_c_numbers
    return batch_idx,[calc_num_it_where_absZ_smaller_threshold(c) for c in c_numbers]

def iterable_to_batches(g:Iterable, batch_size)->Generator[List[object], None, None]:
    g = iter(g) if isinstance(g,list) else g
    batch = []
    while True:
        try:
            batch.append(next(g))
            if len(batch)==batch_size:
                yield batch
                batch = []
        except StopIteration as e: # there is no next element in iterator
            break
    if len(batch)>0:
        yield batch

def multiprocessing_mandelbrot_set(ranges, width, height,num_processes):
    xmin, xmax, ymin, ymax = ranges
    real_part = np.linspace(xmin, xmax, width)
    imaginary_part = np.linspace(ymin, ymax, height)
    c_number_g = (real_part[col] + 1j * imaginary_part[row] for col in range(width) for row in range(height))
    batch_size = int(np.ceil(height * width / num_processes))
    print('batch-size: %d'%batch_size)
    batch_g = ((i,b) for i,b in enumerate(iterable_to_batches(c_number_g,batch_size)))

    with Pool(processes=num_processes) as pool:
        # x = sorted(pool.imap_unordered(compute_batch_fun, batch_g, chunksize=1),key=lambda ib:ib[0])
        # x = [v for i,batch in x for v in batch]
        x = [v for i,batch in pool.imap(compute_batch_fun, batch_g) for v in batch]
    number_of_iterations_matrix = np.array(x)

    return number_of_iterations_matrix.reshape(height,width).transpose()

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

    cores,durations = zip(*cores_durations)

    f = plt.figure()
    f.add_axes() # WTF !?
    axes = f.subplots()
    f.suptitle('cores vs computing-times')
    plt.plot(cores,durations)
    axes.set_xlabel('num cores')
    axes.set_ylabel('duration in seconds')
    plt.savefig('./cores_durations.png')
