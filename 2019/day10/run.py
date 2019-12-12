# -*- coding: utf-8 -*-

from fractions import Fraction
from itertools import compress
import numpy as np

def load_asteroid_field(filename):
    field = []
    row = 0
    with open(filename) as fileobj:
        for line in fileobj:
            col = 0
            for ch in line:
                if ch == '#':
                    field.append((col,row))
                col += 1
            row += 1
    return field

def simplify_slope(col,row):
    if col == 0 and row == 0:
        Exception('slope cannot be 0,0')
    if col == 0:
        if row > 0:
            slope = (0,1)
        else:
            slope = (0, -1)
    elif row == 0:
        if col > 0:
            slope = (1,0)
        else:
            slope = (-1,0)
    else:
        frac = Fraction(col, row)
        if row < 0:
            slope = (-frac.numerator, -frac.denominator)
        else:
            slope = (frac.numerator, frac.denominator)
    
    return slope

def is_detectable_asteroid(source, target, field):
    diff = np.subtract(target, source)
    slope = simplify_slope(diff[0], diff[1])
    
    cur_target = target
    while not cur_target == source:
        cur_target = tuple(np.subtract(cur_target, slope))
        if cur_target == source:
            return 1
        elif cur_target in field:
            return 0

def build_asteroid_array(field):
    asteroid_array = np.zeros((len(field), len(field)), dtype=int)
    
    for i in range(len(field)):
        for j in range(len(field)):
            if not i == j:
                asteroid_array[i,j] = is_detectable_asteroid(field[i], field[j], field)
    
    return asteroid_array

def count_quadrants(rel_positions):
    quadrant_counts = np.zeros(4, dtype=int)
    for asteroid in rel_positions:
        if asteroid[0] >= 0 and asteroid[1] > 0:
            quadrant_counts[0] += 1
        elif asteroid[0] > 0 and asteroid[1] <= 0:
            quadrant_counts[1] += 1
        elif asteroid[0] <= 0 and asteroid[1] < 0:
            quadrant_counts[2] += 1
        elif asteroid[0] < 0 and asteroid[1] >= 0:
            quadrant_counts[3] += 1
    return quadrant_counts

def get_quadrant_asteroids(rel_positions, quadrant):
    asteroids = []
    for asteroid in rel_positions:
        if asteroid[0] >= 0 and asteroid[1] > 0 and quadrant == 0:
            asteroids.append(asteroid)
        elif asteroid[0] > 0 and asteroid[1] <= 0 and quadrant == 1:
            asteroids.append(asteroid)
        elif asteroid[0] <= 0 and asteroid[1] < 0 and quadrant == 2:
            asteroids.append(asteroid)
        elif asteroid[0] < 0 and asteroid[1] >= 0 and quadrant == 3:
            asteroids.append(asteroid)
    return np.array(asteroids)


def find_nth_asteroid_lasered(rel_positions, n=200):
    quadrant_counts = count_quadrants(rel_positions)
    num_asteroids_destroyed = 0
    quadrant_to_consider = 0
    while num_asteroids_destroyed + quadrant_counts[quadrant_to_consider] <= n:
        num_asteroids_destroyed += quadrant_counts[quadrant_to_consider]
        quadrant_to_consider += 1

    # by inspection we see we'll be in upper left quadrant
    quadrant_asteroids = get_quadrant_asteroids(rel_positions, 3)
    quadrant_asteroids_float = np.array(quadrant_asteroids, dtype=float)
    quadrant_asteroids_float[:,1][quadrant_asteroids_float[:,1] < 0.0001] = 0.0001
    row_div_col = quadrant_asteroids_float[:,0] / quadrant_asteroids_float[:,1]
    ascending_sort = row_div_col.argsort()
    num_asteroids_remaining = n - num_asteroids_destroyed
    sorted_asteroids = quadrant_asteroids[ascending_sort]
    nth_asteroid = sorted_asteroids[num_asteroids_remaining-1]
    
    return nth_asteroid
    

field = load_asteroid_field('input.txt')
asteroid_array = build_asteroid_array(field)
counts = np.sum(asteroid_array, axis=0)
max_asteroids = np.max(counts)
max_asteroid_ind = np.argmax(counts)
loc = field[max_asteroid_ind]

asteroids_mask = asteroid_array[:, max_asteroid_ind]
viewable_asteroids = list(compress(field, asteroids_mask))
rel_positions = np.subtract((loc[0], loc[1]), viewable_asteroids)
rel_positions[:,0] *= -1
nth_asteroid_rel = find_nth_asteroid_lasered(rel_positions, n=200)
nth_asteroid_x = loc[0] + nth_asteroid_rel[0]
nth_asteroid_y = loc[1] - nth_asteroid_rel[1]
answer_2 = 100*nth_asteroid_x + nth_asteroid_y
