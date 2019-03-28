import numpy as np
import time

from resmonres.monitor_system_parameters import MonitorSysParams


def numpy_matrix_multiplications(size = 2 ** 12, repetitions = 20):
    np.random.seed(0)
    A, B = np.random.random((size, size)), np.random.random((size, size))

    t = time.time()
    for i in range(repetitions):
        np.dot(A, B)
    delta = time.time() - t
    print('Dotted two %dx%d matrices in %0.2f s.' % (size, size, delta / repetitions))


if __name__ == '__main__':

    with MonitorSysParams(log_path='.'):
        time.sleep(2)
        numpy_matrix_multiplications()
        time.sleep(2)