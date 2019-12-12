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

def calc_array(input_array, noun=None, verb=None, phase=None, input_val=None, input_count=None, op_ind=None):
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
            params = parse_param_mode(digits, params, op_ind)
            input_array[params[2]] = input_array[params[0]] + input_array[params[1]]
            op_ind += 4
        elif op == 2:
            params = np.array(input_array[op_ind+1:op_ind+4])
            params = parse_param_mode(digits, params, op_ind)
            input_array[params[2]] = input_array[params[0]] * input_array[params[1]]
            op_ind += 4
        elif op == 3:
            if input_count == 0:
                input_array[input_array[op_ind+1]] = phase
            else:
                input_array[input_array[op_ind+1]] = input_val
            input_count += 1
            op_ind += 2
        elif op == 4:
            if digits[1] == 1:
                output.append(input_array[op_ind+1])
            else:
                output.append(input_array[input_array[op_ind+1]])
            op_ind += 2
            break
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

    return output, input_array, op_ind, input_count

def run_program(program, phase=None, input_val=None, input_count=None, op_ind=0):
    output_array, modified_prog, op_ind, input_count = calc_array(program, phase=phase, input_val=input_val, input_count=input_count, op_ind=op_ind)
    if len(output_array) == 0:
        return output_array, modified_prog, op_ind, input_count
    if not len(output_array) == 1:
        Exception('run_program: more than one output detected')
    return output_array[0], modified_prog, op_ind, input_count

def run_amp_series(program, phase_sequence):
    input_val = 0
    for phase in phase_sequence:
        output_val, modified_prog, op_ind, input_count = run_program(program, phase, input_val, input_count=0, op_ind=0)
        input_val = output_val
    return output_val



def run_feedback_loop(program, phase_sequence):
    amp_A = AmpState('A', program.copy(), 0, phase_sequence[0], 0)
    amp_B = AmpState('B', program.copy(), 0, phase_sequence[1], 0)
    amp_C = AmpState('C', program.copy(), 0, phase_sequence[2], 0)
    amp_D = AmpState('D', program.copy(), 0, phase_sequence[3], 0)
    amp_E = AmpState('E', program.copy(), 0, phase_sequence[4], 0)
    
    is_running = True
    input_val = 0
    output_val = -99999
    while is_running:
        output_val, modified_prog, op_ind, input_count = \
            run_program(amp_A.program, phase=amp_A.phase, input_val=input_val, input_count=amp_A.input_count, op_ind=amp_A.pointer_ind)
        amp_A.program = modified_prog
        amp_A.pointer_ind = op_ind
        amp_A.input_count = input_count
        input_val = output_val
        
        output_val, modified_prog, op_ind, input_count = \
            run_program(amp_B.program, phase=amp_B.phase, input_val=input_val, input_count=amp_B.input_count, op_ind=amp_B.pointer_ind)
        amp_B.program = modified_prog
        amp_B.pointer_ind = op_ind
        amp_B.input_count = input_count
        input_val = output_val
    
        output_val, modified_prog, op_ind, input_count = \
            run_program(amp_C.program, phase=amp_C.phase, input_val=input_val, input_count=amp_C.input_count, op_ind=amp_C.pointer_ind)
        amp_C.program = modified_prog
        amp_C.pointer_ind = op_ind
        amp_C.input_count = input_count
        input_val = output_val
        
        output_val, modified_prog, op_ind, input_count = \
            run_program(amp_D.program, phase=amp_D.phase, input_val=input_val, input_count=amp_D.input_count, op_ind=amp_D.pointer_ind)
        amp_D.program = modified_prog
        amp_D.pointer_ind = op_ind
        amp_D.input_count = input_count
        input_val = output_val
        
        output_val, modified_prog, op_ind, input_count = \
            run_program(amp_E.program, phase=amp_E.phase, input_val=input_val, input_count=amp_E.input_count, op_ind=amp_E.pointer_ind)
        amp_E.program = modified_prog
        amp_E.pointer_ind = op_ind
        amp_E.input_count = input_count
        input_val = output_val
        
        if amp_E.program[amp_E.pointer_ind] == 99:
            if not output_val == 0:
                last_output_val = output_val
            is_running = False
        else:
            last_output_val = output_val
    
    return last_output_val
        
phase_array = np.array([0,1,2,3,4])
day7_program = np.loadtxt('day7_input.txt',delimiter=',', dtype=int)
phase_sequences_to_test = list(itertools.permutations(phase_array))
max_thrust_series = -9999999
for phase_sequence in phase_sequences_to_test:
    this_thrust = run_amp_series(day7_program.copy(), phase_sequence)
    if this_thrust > max_thrust_series:
        max_thrust_series = this_thrust


test_feedback_prog = np.array([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5])
test_phase_sequence = np.array([9,8,7,6,5])
test_feedback_output = run_feedback_loop(test_feedback_prog, test_phase_sequence)

day7_program = np.loadtxt('day7_input.txt',delimiter=',', dtype=int)
feedback_phase_array = np.array([5,6,7,8,9])
feedback_phase_sequences_to_test = list(itertools.permutations(feedback_phase_array))
feedback_max_thrust = -9999999
for phase_sequence in feedback_phase_sequences_to_test:
    this_thrust = run_feedback_loop(day7_program, phase_sequence)
    if this_thrust > feedback_max_thrust:
        feedback_max_thrust = this_thrust