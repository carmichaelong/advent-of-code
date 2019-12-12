# -*- coding: utf-8 -*-

from dataclasses import dataclass
import itertools
import numpy as np

@dataclass
class AmpState:
    name: str
    program: np.array
    pointer_ind: int
    phase: int
    input_count: int
    relative_base: int

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

def parse_param_mode(digits, params, op_ind, relative_base=None):
    for i in range(0,len(params)):
        if digits[i+1] == 1:
            params[i] = op_ind+i+1
        if digits[i+1] == 2:
            params[i] = params[i] + relative_base
    
    return params

def calc_array(input_array, noun=None, verb=None, phase=None, 
               input_val=None, input_count=None, op_ind=None, 
               relative_base=None):
    if not noun == None:
        input_array[1] = noun
    if not verb == None:
        input_array[2] = verb
    
    output = []    
    #op_ind = 0
    while op_ind <= input_array.size:
        op = input_array[op_ind]
        digits = parse_op(op)
        op = digits[0]
        if op == 1:
            params = np.array(input_array[op_ind+1:op_ind+4])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            input_array[params[2]] = input_array[params[0]] + input_array[params[1]]
            op_ind += 4
        elif op == 2:
            params = np.array(input_array[op_ind+1:op_ind+4])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            input_array[params[2]] = input_array[params[0]] * input_array[params[1]]
            op_ind += 4
        elif op == 3:
            params = np.array([input_array[op_ind+1]])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            if input_count == 0:
                input_array[params[0]] = phase
            else:
                input_array[params[0]] = input_val
            input_count += 1
            op_ind += 2

        elif op == 4:
            params = np.array([input_array[op_ind+1]])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            output.append(input_array[params[0]])
            op_ind += 2

        elif op == 5:
            params = np.array(input_array[op_ind+1:op_ind+3])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            if input_array[params[0]] == 0:
                op_ind += 3
            else:
                op_ind = input_array[params[1]]
        elif op == 6:
            params = np.array(input_array[op_ind+1:op_ind+3])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            if input_array[params[0]] == 0:
                op_ind = input_array[params[1]]
            else:
                op_ind +=3
        elif op == 7:
            params = np.array(input_array[op_ind+1:op_ind+4])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            if input_array[params[0]] < input_array[params[1]]:
                input_array[params[2]] = 1
            else:
                input_array[params[2]] = 0
            op_ind += 4
        elif op == 8:
            params = np.array(input_array[op_ind+1:op_ind+4])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            if input_array[params[0]] == input_array[params[1]]:
                input_array[params[2]] = 1
            else:
                input_array[params[2]] = 0
            op_ind += 4
        elif op == 9:
            params = np.array([input_array[op_ind+1]])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            relative_base += input_array[params[0]]
            op_ind += 2
        elif op == 99:
            break

    return output, input_array, op_ind, input_count

def run_program(program, phase=None, input_val=None, input_count=None, op_ind=0, relative_base=None):
    output_array, modified_prog, op_ind, input_count = \
        calc_array(program, phase=phase, input_val=input_val, 
                   input_count=input_count, op_ind=op_ind, 
                   relative_base=relative_base)
#    if len(output_array) == 0:
#        return output_array, modified_prog, op_ind, input_count
#    if not len(output_array) == 1:
#        Exception('run_program: more than one output detected')
    return output_array, modified_prog, op_ind, input_count


        
test_day9_prog = np.array([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
test_day9_prog_padded = np.zeros(10*test_day9_prog.size, dtype='int64')
test_day9_prog_padded[0:test_day9_prog.size] = test_day9_prog
test_day9_prog_output, modified_prog, op_ind, input_count = run_program(test_day9_prog_padded, phase=1, relative_base=0)

day9_prog = np.loadtxt('day9_input.txt', delimiter=',', dtype=int)
day9_prog_padded = np.zeros(10*day9_prog.size, dtype='int64')
day9_prog_padded[0:day9_prog.size] = day9_prog
day9_prog_output, modified_prog, op_ind, input_count = run_program(day9_prog_padded, phase=1, input_val=1, input_count=0, relative_base=0)
day9_prog_output_2, modified_prog, op_ind, input_count = run_program(day9_prog_padded, phase=2, input_val=2, input_count=0, relative_base=0)
