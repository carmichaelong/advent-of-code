# -*- coding: utf-8 -*-

import numpy as np

def parse_op(op):
    digits = np.zeros(4)
    
    digits[0] = op % 100
    op = np.floor_divide(op, 100)
    
    digits[1] = op % 10
    op = np.floor_divide(op, 10)
    
    digits[2] = op % 10
    op = np.floor_divide(op, 10)
    
    digits[3] = op % 10
    
    return digits

def parse_param_mode(digits, params, op_ind):
    for i in range(0,len(params)):
        if digits[i+1] == 1:
            params[i] = op_ind+i+1
    
    return params

def calc_array(input_array, noun=None, verb=None, input_val=None):
    output = []
    op_ind = 0
    if not noun == None:
        input_array[1] = noun
    if not verb == None:
        input_array[2] = verb

    while op_ind <= input_array.size:
        op = input_array[op_ind]
        digits = parse_op(op)
        op = digits[0]
        if op == 1:
            params = np.array(input_array[op_ind+1:op_ind+4])
            params = parse_param_mode(digits, params, op_ind)
            input_array[params[2]] = input_array[params[0]] + input_array[params[1]]
            op_ind += 4
        elif op == 2:
            params = np.array(input_array[op_ind+1:op_ind+4])
            params = parse_param_mode(digits, params, op_ind)
            input_array[params[2]] = input_array[params[0]] * input_array[params[1]]
            op_ind += 4
        elif op == 3:
            input_array[input_array[op_ind+1]] = input_val
            op_ind += 2
        elif op == 4:
            if digits[1] == 1:
                output.append(input_array[op_ind+1])
            else:
                output.append(input_array[input_array[op_ind+1]])
            op_ind += 2
        elif op == 5:
            params = np.array(input_array[op_ind+1:op_ind+3])
            params = parse_param_mode(digits, params, op_ind)
            if input_array[params[0]] == 0:
                op_ind += 3
            else:
                op_ind = input_array[params[1]]
        elif op == 6:
            params = np.array(input_array[op_ind+1:op_ind+3])
            params = parse_param_mode(digits, params, op_ind)
            if input_array[params[0]] == 0:
                op_ind = input_array[params[1]]
            else:
                op_ind +=3
        elif op == 7:
            params = np.array(input_array[op_ind+1:op_ind+4])
            params = parse_param_mode(digits, params, op_ind)
            if input_array[params[0]] < input_array[params[1]]:
                input_array[params[2]] = 1
            else:
                input_array[params[2]] = 0
            op_ind += 4
        elif op == 8:
            params = np.array(input_array[op_ind+1:op_ind+4])
            params = parse_param_mode(digits, params, op_ind)
            if input_array[params[0]] == input_array[params[1]]:
                input_array[params[2]] = 1
            else:
                input_array[params[2]] = 0
            op_ind += 4
        elif op == 99:
            break

    return output

#input_array = np.loadtxt('day2_input.txt',delimiter=',', dtype=int)
#out_array_1 = calc_array(input_array, 12, 2)
#
#correct_set = []
#for noun in range(100):
#    for verb in range(100):
#        input_array = np.loadtxt('day2_input.txt',delimiter=',', dtype=int)
#        if calc_array(input_array, noun, verb)[0] == 19690720:
#            correct_set.append((noun,verb))
#
#correct_noun = correct_set[0][0]
#correct_verb = correct_set[0][1]
#answer_2 = 100*correct_noun + correct_verb

input_array = np.loadtxt('day5_input.txt',delimiter=',', dtype=int)
#out_array_day5 = calc_array(input_array, input_val=1)

test_1 = np.array([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
out_test_1 = calc_array(test_1, input_val=23232)
out_array_day5_part2 = calc_array(input_array, input_val=5)