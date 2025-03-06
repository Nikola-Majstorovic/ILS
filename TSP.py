# https://econ.upf.edu/~ramalhin/PDFfiles/2001_MIC_FILS.pdf

import random
from copy import deepcopy
import math
import numpy as np

import matplotlib.pyplot as plt
import time

import ILS as mh2

def read_city_coords(f):
   floats = [float(x) for x in f.readline().split()]  
   return floats[1:]

def read_TSP_file(file_path):
     with open(file_path, 'r') as f:
        _, name = [x for x in f.readline().split()]
        _ = f.readline()
        comment = [x for x in f.readline().split()]
        _, n = [x for x in f.readline().split()]
        _ = f.readline()
        _ = f.readline()
        n = int(n)
        points = np.array([read_city_coords(f) for _ in range(n)])
        return points

def calculate_distance_matrix(file_path):
    points = read_TSP_file(file_path)
    n = len(points)
    matrix = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            matrix[i][j] = np.sqrt(np.sum((points[i] - points[j])**2))
    return matrix

def TSP(distances_matrix, time_limit, num_iters, search, local_minimizing_function, init_function, output_file_name):
    individual_timestamps = []
    individual_values = []
    solutions = []
    path_lengths = []
    for iter in range(num_iters):
        solution, path_length, values, time_stamps, end_time = search(distances_matrix, 50*len(distances_matrix), time_limit, local_minimizing_function, init_function)
        individual_timestamps.append(time_stamps)
        individual_values.append(values)
        solutions.append(solution)
        path_lengths.append(path_length)
        print(f'path_length: {path_length} | Num of points: {len(values)} | Time: {end_time}s')
    
    with open(f'results/{output_file_name}.txt', 'w') as f:
        f.write(f'{num_iters}\n')
        for i in range(num_iters):
            f.write(f'PATH LENGTH: {path_lengths[i]}\n')
            f.write('SOLUTION: \n')
            f.write(" ".join([f'{int(x)}' for x in solutions[i]]) + '\n')
    with open(f'results/{output_file_name}_history.txt', 'w') as f:
        f.write(f'{num_iters}\n')
        for i in range(num_iters):
            f.write('HISTORY: \n')
            f.write(" ".join([f'{float(x)}' for x in individual_values[i]]) + '\n')
            f.write(" ".join([f'{float(x)}' for x in individual_timestamps[i]]) + '\n')

    return solutions, path_lengths

tsp_file_path = input('TSP file path: ')
distance_matrix = calculate_distance_matrix(tsp_file_path)
time_limit = input('Time limit: ')
num_iters = input('Number of TSP calls: ')
output_file_name = input('Output file name: ')

solutions = TSP(distance_matrix, float(time_limit), int(num_iters), mh2.iterated_local_search, mh2.three_opt_best_improvement, mh2.greedy_start, output_file_name)

