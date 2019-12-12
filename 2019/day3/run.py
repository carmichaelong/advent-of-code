# -*- coding: utf-8 -*-

import csv
import numpy as np

def find_min_num_steps(crossings, wire_list_0, wire_list_1):
    min_steps = 1e10
    for this_crossing in crossings:
        steps_0 = wire_list_0.index(this_crossing) + 1
        steps_1 = wire_list_1.index(this_crossing) + 1
        num_steps = steps_0 + steps_1
        if num_steps < min_steps:
            min_steps = num_steps

    return min_steps

def find_min_crossing_distance(crossings):
    min_distance = 1e10
    for pair in crossings:
        this_distance = np.abs(pair[0]) + np.abs(pair[1])
        if this_distance < min_distance:
            min_distance = this_distance
    return min_distance

def calc_all_positions(wire_list):
    x_cur = 0
    y_cur = 0
    pos_list = []
    
    for el in wire_list:
        direction = el[0]
        distance = int(el[1:])
        
        for i in range(distance):
            if direction == 'R':
                x_cur += 1
            elif direction == 'L':
                x_cur -= 1
            elif direction == 'U':
                y_cur += 1
            elif direction == 'D':
                y_cur -= 1
            else:
                Exception('not a valid diretion')
            pos_list.append((x_cur, y_cur))
    
    return pos_list

wire_lists = []
with open('prob1.txt', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for el in reader:
        wire_lists.append(el)
wire_0 = wire_lists[0]
wire_1 = wire_lists[1]

pos_wire_0 = calc_all_positions(wire_0)
pos_wire_1 = calc_all_positions(wire_1)
crossings = set(pos_wire_0) & set(pos_wire_1)
min_distance = find_min_crossing_distance(crossings)

min_steps = find_min_num_steps(crossings, pos_wire_0, pos_wire_1)