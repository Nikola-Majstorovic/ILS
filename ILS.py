import random
from copy import deepcopy
import math
import numpy as np
import time

def initialize_random_solution(distances_matrix):
    n = len(distances_matrix)
    cities = list(range(n))
    random.shuffle(cities)
    return cities

def greedy_start(distances_matrix):
    cities = [0]
    visited = {0}
    n = len(distances_matrix)
    for i in range(1, n):
        closest_unvisited_city = min((j for j,x in enumerate(distances_matrix[cities[i-1]]) if j not in visited), key = lambda j: distances_matrix[cities[i-1]][j])
        cities.append(closest_unvisited_city)
        visited.add(closest_unvisited_city)
    return cities

def calculate_path_length(solution, distances_matrix):
    path_length = 0
    n = len(solution) - 1
    for i in range(n):
        path_length += distances_matrix[solution[i]][solution[i+1]]
    path_length += distances_matrix[solution[0]][solution[-1]]
    return path_length

def calculate_k_closest_neighbours(distances_matrix, k):
    neighbours = []
    n = len(distances_matrix)
    for i in range(n):
        neighbours.append(sorted((j for j, x in enumerate(distances_matrix[i])), key=lambda j: distances_matrix[i][j])[1:k+1])  
    return neighbours 

def update_positions(position, solution, i, k):
    for j in range(i, k+1):
        position[solution[j]] = j 

def apply_reconnecting(option, solution, i, j, k):
    if option == 0:
        solution[i+1:j+1] = solution[i+1:j+1][::-1]
    elif option == 1:
        solution[i+1:j+1] = solution[i+1:j+1][::-1]
        solution[j+1:k+1] = solution[j+1:k+1][::-1]
    elif option == 2:
        solution[j+1:k+1] = solution[j+1:k+1][::-1]
    elif option == 3:
        solution[i+1:k+1] = solution[j+1:k+1] + solution[i+1:j+1]
    elif option == 4:
        solution[i+1:k+1] = solution[j+1:k+1] + solution[i+1:j+1][::-1]
    elif option == 5:
        solution[i+1:k+1] = solution[j+1:k+1][::-1] + solution[i+1:j+1][::-1]
    elif option == 6:
        solution[i+1:k+1] = solution[j+1:k+1][::-1] + solution[i+1:j+1]   

def three_opt_first_improvement(solution, distances_matrix, position, neighbours):
    start_time = time.time()
    path_length = calculate_path_length(solution, distances_matrix)
    improved = True
    while improved:
        improved = False
        for i in range(len(solution)-5):
            for city_1 in neighbours[solution[i]]:
                if position[city_1] < i+2 or position[city_1] >= len(solution) - 3:
                    continue
                for city_2 in neighbours[city_1]:
                    if position[city_2] < position[city_1]+2:
                        continue
                    j = position[city_1]
                    k = position[city_2]
                    removed_edges_length = distances_matrix[solution[i]][solution[i+1]] + distances_matrix[solution[j]][solution[j+1]] + distances_matrix[solution[k]][solution[k+1 if k < len(solution)-1 else 0]]    
                    new_edges_length_1 = distances_matrix[solution[i]][solution[j]] + distances_matrix[solution[i+1]][solution[j+1]] + distances_matrix[solution[k]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_2 = distances_matrix[solution[i]][solution[j]] + distances_matrix[solution[i+1]][solution[k]] + distances_matrix[solution[j+1]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_3 = distances_matrix[solution[i]][solution[i+1]] + distances_matrix[solution[j]][solution[k]] + distances_matrix[solution[j+1]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_4 = distances_matrix[solution[i]][solution[j+1]] + distances_matrix[solution[k]][solution[i+1]] + distances_matrix[solution[j]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_5 = distances_matrix[solution[i]][solution[j+1]] + distances_matrix[solution[k]][solution[j]] + distances_matrix[solution[i+1]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_6 = distances_matrix[solution[i]][solution[k]] + distances_matrix[solution[j+1]][solution[j]] + distances_matrix[solution[i+1]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_7 = distances_matrix[solution[i]][solution[k]] + distances_matrix[solution[j+1]][solution[i+1]] + distances_matrix[solution[j]][solution[k+1 if k < len(solution)-1 else 0]]
                    best_option, new_edges_length = min(enumerate([new_edges_length_1, new_edges_length_2, new_edges_length_3, new_edges_length_4, new_edges_length_5, new_edges_length_6, new_edges_length_7]), key = lambda x:x[1]) 
                    if new_edges_length + 0.01 < removed_edges_length:
                        path_length -= removed_edges_length
                        path_length += new_edges_length
                        apply_reconnecting(best_option, solution, i, j, k)
                        update_positions(position, solution, i, k)
                        improved = True
                        break
                if improved:
                        break
            if improved:
                break    
    end_time = time.time()
    return solution, path_length

def three_opt_best_improvement(solution, distances_matrix, position, neighbours):
    start_time = time.time()
    path_length = calculate_path_length(solution, distances_matrix)
    while True:
        best_edges_to_remove = None
        best_reconnection_type = -1
        best_improvement = 0
        for i in range(len(solution)-5):
            for city_1 in neighbours[solution[i]]:
                if position[city_1] < i+2 or position[city_1] >= len(solution) - 3:
                    continue
                for city_2 in neighbours[city_1]:
                    if position[city_2] < position[city_1]+2:
                        continue
                    j = position[city_1]
                    k = position[city_2]
                    removed_edges_length = distances_matrix[solution[i]][solution[i+1]] + distances_matrix[solution[j]][solution[j+1]] + distances_matrix[solution[k]][solution[k+1 if k < len(solution)-1 else 0]]    
                    new_edges_length_1 = distances_matrix[solution[i]][solution[j]] + distances_matrix[solution[i+1]][solution[j+1]] + distances_matrix[solution[k]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_2 = distances_matrix[solution[i]][solution[j]] + distances_matrix[solution[i+1]][solution[k]] + distances_matrix[solution[j+1]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_3 = distances_matrix[solution[i]][solution[i+1]] + distances_matrix[solution[j]][solution[k]] + distances_matrix[solution[j+1]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_4 = distances_matrix[solution[i]][solution[j+1]] + distances_matrix[solution[k]][solution[i+1]] + distances_matrix[solution[j]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_5 = distances_matrix[solution[i]][solution[j+1]] + distances_matrix[solution[k]][solution[j]] + distances_matrix[solution[i+1]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_6 = distances_matrix[solution[i]][solution[k]] + distances_matrix[solution[j+1]][solution[j]] + distances_matrix[solution[i+1]][solution[k+1 if k < len(solution)-1 else 0]]
                    new_edges_length_7 = distances_matrix[solution[i]][solution[k]] + distances_matrix[solution[j+1]][solution[i+1]] + distances_matrix[solution[j]][solution[k+1 if k < len(solution)-1 else 0]]
                    best_option, new_edges_length = min(enumerate([new_edges_length_1, new_edges_length_2, new_edges_length_3, new_edges_length_4, new_edges_length_5, new_edges_length_6, new_edges_length_7]), key = lambda x:x[1]) 
                    improvement = new_edges_length - removed_edges_length
                    if improvement + 0.001 < best_improvement:
                        best_improvement = improvement
                        best_edges_to_remove = (i, j, k)
                        best_reconnection_type = best_option
        if best_edges_to_remove is None:
            break
        apply_reconnecting(best_reconnection_type, solution, best_edges_to_remove[0], best_edges_to_remove[1], best_edges_to_remove[2])
        update_positions(position, solution, best_edges_to_remove[0], best_edges_to_remove[2])
        path_length += best_improvement
    end_time = time.time()
    return solution, path_length

def two_opt_first_improvement(solution, distances_matrix, position, neighbours):
    start_time = time.time()
    path_length = calculate_path_length(solution, distances_matrix)
    improved = True
    while improved:
        improved = False
        for i in range(len(solution)-3):
            for j in range(i+2, len(solution) if i>0 else len(solution)-1): 
                k = j+1 if j < len(solution)-1 else 0
                path_length_change = distances_matrix[solution[i]][solution[j]] + distances_matrix[solution[i+1]][solution[k]] - distances_matrix[solution[i]][solution[i+1]] - distances_matrix[solution[j]][solution[k]]
                if path_length_change < -0.05:
                    path_length += path_length_change
                    solution = solution[:i+1] + solution[i+1:j+1][::-1] + solution[j+1:]
                    improved = True
                    break
            if improved:
                break
    end_time = time.time()

    return solution, path_length

def two_opt_best_improvement(solution, distances_matrix, position, neighbours):
    start_time = time.time()
    path_length = calculate_path_length(solution, distances_matrix)
    while True:
        best_improvement = 0
        best_pair = None
        for i in range(len(solution)-3):
            for j in range(i+2, len(solution) if i>0 else len(solution)-1): 
                k = j+1 if j < len(solution)-1 else 0
                path_length_change = distances_matrix[solution[i]][solution[j]] + distances_matrix[solution[i+1]][solution[k]] - distances_matrix[solution[i]][solution[i+1]] - distances_matrix[solution[j]][solution[k]]
                if path_length_change + 0.05 < best_improvement:
                    best_improvement = path_length_change
                    best_pair = (i, j)
        if best_pair is None:
            break
        path_length += best_improvement
        i, j = best_pair
        solution = solution[:i+1] + solution[i+1:j+1][::-1] + solution[j+1:]
    return solution, path_length

def double_bridge_simple(solution):
    breaking_points = sorted(random.sample(range(len(solution)), 4))
    segments = [
        solution[breaking_points[3]:]+solution[:breaking_points[0]], 
        solution[breaking_points[0]:breaking_points[1]],
        solution[breaking_points[1]:breaking_points[2]],
        solution[breaking_points[2]:breaking_points[3]]
        ]
    new_order = random.sample(range(4), 4)
    new_solution = segments[new_order[0]] + segments[new_order[1]] + segments[new_order[2]] + segments[new_order[3]]
    new_position = list(range(len(new_solution)))
    update_positions(new_position, new_solution, 0, len(new_solution)-1)
    return new_solution, new_position

def double_bridge(solution, n):
    breaking_points = sorted(random.sample(range(len(solution)), n))
    segments = [solution[breaking_points[n-1]:]+solution[:breaking_points[0]]]
    for i in range(n-1):
        segments.append(solution[breaking_points[i]:breaking_points[i+1]])
    new_order = random.sample(range(n), n)
    new_solution = []
    for i in range(n):
        new_solution += segments[new_order[i]]
    new_position = list(range(len(new_solution)))
    update_positions(new_position, new_solution, 0, len(new_solution)-1)
    return new_solution, new_position

def iterated_local_search(distances_matrix, max_iter_without_improvement, time_limit, local_search, init_method):
    values = []
    time_stamps = []
    neighbours = calculate_k_closest_neighbours(distances_matrix, 20)
    position = list(range(len(distances_matrix)))
    solution = init_method(distances_matrix)
    for i in range(len(solution)):
        position[solution[i]] = i
    values.append(calculate_path_length(solution, distances_matrix))
    time_stamps.append(0.0)
    start_time = time.time()
    solution, path_length = local_search(solution, distances_matrix, position, neighbours)
    values.append(path_length)
    time_stamps.append(time.time()-start_time)
    iter_without_improvement = 0
    itters = 0
    while True:
        itters += 1
        new_solution, new_position = double_bridge_simple(solution)
        new_solution, new_path_length = local_search(new_solution, distances_matrix, new_position, neighbours)
        if new_path_length < path_length:
            path_length = new_path_length
            solution = deepcopy(new_solution)
            position = deepcopy(new_position)
            values.append(path_length)
            time_stamps.append(time.time() - start_time)
            iter_without_improvement = 0
        else:
            iter_without_improvement += 1
        if iter_without_improvement == max_iter_without_improvement or time.time() - start_time > time_limit:
            break
    end_time = time.time()
    return solution, path_length, values, time_stamps, end_time - start_time

