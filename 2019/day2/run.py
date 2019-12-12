# -*- coding: utf-8 -*-

import numpy as np

def calc_array(input_array, noun, verb):
    input_array[1] = noun
    input_array[2] = verb
    start_ind = 0
    while start_ind <= input_array.size - 3:
        this_set = input_array[start_ind:start_ind+4]
        if this_set[0] == 1:
            input_array[this_set[3]] = input_array[this_set[1]] + input_array[this_set[2]]
        elif this_set[0] == 2:
            input_array[this_set[3]] = input_array[this_set[1]] * input_array[this_set[2]]
        elif this_set[0] == 99:
            break
        else:
            print('unknown code')
        
        start_ind += 4

    return input_array

input_array = np.loadtxt('prob1.txt',delimiter=',', dtype=int)
out_array_1 = calc_array(input_array, 12, 2)

correct_set = []
for noun in range(100):
    for verb in range(100):
        input_array = np.loadtxt('prob1.txt',delimiter=',', dtype=int)
        if calc_array(input_array, noun, verb)[0] == 19690720:
            correct_set.append((noun,verb))

correct_noun = correct_set[0][0]
correct_verb = correct_set[0][1]
answer_2 = 100*correct_noun + correct_verb
