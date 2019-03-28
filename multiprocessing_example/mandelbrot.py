import numpy as np


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