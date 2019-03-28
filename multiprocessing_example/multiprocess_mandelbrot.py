from multiprocessing.pool import Pool
import multiprocessing
from typing import Iterable, Generator, List
import numpy as np
from multiprocessing_example.mandelbrot import calc_num_it_where_absZ_smaller_threshold


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
        x = [v for i,batch in pool.imap(compute_batch_fun, batch_g) for v in batch]

    number_of_iterations_matrix = np.array(x).reshape(height,width).transpose()
    return number_of_iterations_matrix
