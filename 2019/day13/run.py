# -*- coding: utf-8 -*-

from dataclasses import dataclass
import numpy as np

@dataclass
class IntcodeState:
    program: np.array
    pointer_ind: int
    relative_base: int

def find_paddle_ball_loc(output):
    tile_info_start = 0
    loc_paddle = None
    loc_ball = None
    while tile_info_start < len(output):
        this_tile_info = output[tile_info_start:tile_info_start+3]
        if this_tile_info[2] == 3:
            loc_paddle = np.array(this_tile_info)
        elif this_tile_info[2] == 4:
            loc_ball = np.array(this_tile_info)
        if loc_paddle is not None and loc_ball is not None:
            break
        tile_info_start += 3
    return loc_paddle, loc_ball

def get_score(output):
    tile_info_start = 0
    
    score = None
    while tile_info_start < len(output):
        this_tile_info = output[tile_info_start:tile_info_start+3]
        if this_tile_info[0] == -1 and this_tile_info[1] == 0:
            score = this_tile_info[2]
        tile_info_start += 3
    return score

def construct_block_locs(output):
    output_array = np.array(output)
    block_tiles = np.where(output_array[2::3] == 2)[0]
    block_locs = []
    for this_block in block_tiles:
        block_locs.append(output_array[3*this_block:3*this_block+3])
    return np.array(block_locs)

def update_block_locs(block_locs, output):
    output_array = np.array(output)
    empty_tiles = np.where(output_array[2::3] == 0)[0]
    for empty in empty_tiles:
        empty_loc = np.array(output[3*empty:3*empty+2])
        for i in range(block_locs.shape[0]):
            if (block_locs[i,0:2] == empty_loc).all():
                block_locs[i,2] = 0
    return block_locs
                
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

def calc_array(input_array, phase=None, 
               input_val=None, op_ind=None, 
               relative_base=None):

    output = []
    input_count = 0
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
            if input_count == 0:
                block_locs = construct_block_locs(output)
                score = get_score(output)
            else:
                block_locs = update_block_locs(block_locs, output)
                update_score = get_score(output)
                if update_score is not None:
                    score = update_score
            loc_paddle, loc_ball = find_paddle_ball_loc(output)
            num_blocks = np.sum(block_locs[:,2])/2
            print('num_blocks = ' + str(num_blocks))
            print('score = ' + str(score))
            if loc_paddle is not None and loc_ball is not None:
                if loc_ball[0] < loc_paddle[0]:
                    input_val = -1
                elif loc_ball[0] > loc_paddle[0]:
                    input_val = 1
                else:
                    input_val = 0

            params = np.array([input_array[op_ind+1]])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            input_array[params[0]] = input_val
            op_ind += 2
            output = []
            input_count += 1
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

    return output, input_array, op_ind, relative_base

def run_program(program, input_val=None, op_ind=None, relative_base=None):
    output_array, modified_prog, op_ind, relative_base = \
        calc_array(program, input_val=input_val, op_ind=op_ind, 
                   relative_base=relative_base)

    return output_array, modified_prog, op_ind, relative_base

def update_intcode_state(intcode_state, modified_prog, op_ind, relative_base):
    intcode_state.program = modified_prog
    intcode_state.pointer_ind = op_ind
    intcode_state.relative_base = relative_base
    return intcode_state

program = np.loadtxt('input.txt', delimiter=',', dtype=int)
program_padded = np.zeros(300*program.size, dtype=int)
#program_padded[0:program.size] = program
#intcode_state = IntcodeState(program_padded, 0, 0)
#
#output, modified_prog, op_ind, relative_base = \
#    run_program(intcode_state.program,
#                op_ind=intcode_state.pointer_ind,
#                relative_base=intcode_state.relative_base)
#intcode_state = update_intcode_state(intcode_state, modified_prog, op_ind, relative_base)
#
#answer_1 = output[2::3].count(2)

program_padded_2 = np.zeros_like(program_padded)
program_padded_2[0:program.size] = program
program_padded_2[0] = 2
intcode_state_2 = IntcodeState(program_padded_2,0,0)

while True:
    output, modified_prog, op_ind, relative_base = \
        run_program(intcode_state_2.program,
                    op_ind=0,
                    relative_base=intcode_state_2.relative_base)
    intcode_state_2 = update_intcode_state(intcode_state_2, modified_prog, op_ind, relative_base)
    num_blocks = output[2::3].count(2)
#    if num_blocks == 0:
#        break
