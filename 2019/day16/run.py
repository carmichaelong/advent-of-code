# -*- coding: utf-8 -*-

import joblib
import random
from dataclasses import dataclass

import numpy as np

def read_input_signal(filename):
    digits = []
    with open(filename) as f:
        for line in f:
            for ch in line:
                digits.append(int(ch))
    return np.array(digits, dtype=int)

def construct_multiply_pattern(base_pattern, signal_length, position):
    phase_pattern = np.array([])
    for digit in base_pattern:
        phase_pattern = np.append(phase_pattern, digit*np.ones(position))
    
    num_repeat = int(np.ceil(signal_length / phase_pattern.size) + 1)
    multiply_pattern = np.tile(phase_pattern, num_repeat)
    multiply_pattern = np.delete(multiply_pattern, 0)
    multiply_pattern = multiply_pattern[0:signal_length]
    return multiply_pattern

input_signal = read_input_signal('input.txt')
base_pattern = np.array([0, 1, 0, -1])

phases = 4
cur_signal = np.array(input_signal)
for i in range(1, phases+1):
    next_signal = np.zeros_like(cur_signal)
    for j in range(1, input_signal.size+1):
        multiply_pattern = construct_multiply_pattern(base_pattern, input_signal.size, j)
        next_signal[j-1] = np.abs(np.sum(cur_signal*multiply_pattern)) % 10
    cur_signal = np.array(next_signal)
answer_1 = cur_signal[0:8]

phases = 100
signal_repeat = 10000
message_offset = 5978783
input_signal_2 = np.tile(input_signal, signal_repeat)
cur_signal_shrink = np.array(input_signal_2[message_offset:])
for i in range(1, phases+1):
    next_signal = np.zeros_like(cur_signal_shrink)
    cumulative_sum = 0
    for j in range(cur_signal_shrink.size-1, -1, -1):
        cumulative_sum += cur_signal_shrink[j]
        next_signal[j] = np.abs(cumulative_sum) % 10
    print('phase = ' + str(i))
    cur_signal_shrink = np.array(next_signal)
answer_2 = cur_signal_shrink[0:8]