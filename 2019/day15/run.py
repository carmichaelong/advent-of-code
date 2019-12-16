# -*- coding: utf-8 -*-

import joblib
import random
from dataclasses import dataclass

import numpy as np

@dataclass
class IntcodeState:
    program: np.array
    pointer_ind: int
    relative_base: int

@dataclass
class BoardState:
    board: np.array
    pos: np.array

@dataclass
class BoardStateOxygen:
    board: np.array
    cur_oxygen_nodes: list

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

def calc_array(input_array, input_val=None, op_ind=None, relative_base=None):
    output = []    
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
            input_array[params[0]] = input_val
            op_ind += 2

        elif op == 4:
            params = np.array([input_array[op_ind+1]])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            output.append(input_array[params[0]])
            op_ind += 2
            break
        
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

def init_board_state(row, col):
    board = np.zeros((row, col), dtype=int)
    pos = np.array([np.floor_divide(row,2), np.floor_divide(col,2)], dtype=int)
    return BoardState(board, pos)

def update_board_state(board_state, input_val, prog_output):
    cur_board = board_state.board
    cur_pos = board_state.pos
    if prog_output == 0:
        
        if input_val == 1:
            cur_board[cur_pos[0]-1, cur_pos[1]] = 9
            
        elif input_val == 2:
            cur_board[cur_pos[0]+1, cur_pos[1]] = 9
            
        elif input_val == 3:
            cur_board[cur_pos[0], cur_pos[1]-1] = 9
            
        elif input_val == 4:
            cur_board[cur_pos[0], cur_pos[1]+1] = 9
            
    elif prog_output == 1 or prog_output == 2:
        
        if input_val == 1:
            cur_pos[0] += -1
            
        elif input_val == 2:
            cur_pos[0] += 1
            
        elif input_val == 3:
            cur_pos[1] += -1
            
        elif input_val == 4:
            cur_pos[1] += 1
        
        if prog_output == 1:
            cur_board[cur_pos[0], cur_pos[1]] = 1
        elif prog_output == 2:
            cur_board[cur_pos[0], cur_pos[1]] = 2

    board_state = BoardState(cur_board, cur_pos)
    return board_state

def initialize_board_state_oxygen(board):
    cur_oxygen_nodes = []
    start_node = np.zeros(2, dtype=int)
    start_node[0] = np.nonzero(board == 2)[0][0]
    start_node[1] = np.nonzero(board == 2)[1][0]
    cur_oxygen_nodes.append(start_node)
    board_state_oxygen = BoardStateOxygen(board_state.board, cur_oxygen_nodes)
    return board_state_oxygen


def update_intcode_state(intcode_state, modified_prog, op_ind, relative_base):
    intcode_state.program = modified_prog
    intcode_state.pointer_ind = op_ind
    intcode_state.relative_base = relative_base
    return intcode_state

# initialization
program = np.loadtxt('input.txt', delimiter=',', dtype='int64')
program_padded = np.zeros(10*program.size, dtype='int64')
program_padded[0:program.size] = program
intcode_state = IntcodeState(program_padded, 0, 0)
board_state = init_board_state(50, 50)
board_state.board[board_state.pos[0], board_state.pos[1]] = 1 

# random search part 1
for i in range(1000000):
    input_val = random.randint(1,4)
    output, modified_prog, op_ind, relative_base = \
        run_program(intcode_state.program, input_val=input_val,
                    op_ind=intcode_state.pointer_ind,
                    relative_base=intcode_state.relative_base)
    intcode_state = update_intcode_state(intcode_state, modified_prog, op_ind, relative_base)
    board_state = update_board_state(board_state, input_val, output[0])
joblib.dump(board_state, 'board_state_full.joblib')

# oxygen (label 2) at [39,37]

# part 2
board_state = joblib.load('board_state_full.joblib')
board_state_oxygen = initialize_board_state_oxygen(board_state.board)
elapsed_min = 0
while True:
    board = board_state_oxygen.board
    cur_nodes = board_state_oxygen.cur_oxygen_nodes
    next_nodes = []
    for cur_node in cur_nodes:
        up_node = np.array([cur_node[0]-1, cur_node[1]])
        down_node = np.array([cur_node[0]+1, cur_node[1]])
        left_node = np.array([cur_node[0], cur_node[1]-1])
        right_node = np.array([cur_node[0], cur_node[1]+1])
        neighbor_nodes = [up_node, down_node, left_node, right_node]
        
        for this_node in neighbor_nodes:
            if board[this_node[0], this_node[1]] == 1:
                board[this_node[0], this_node[1]] = 2
                next_nodes.append(this_node)
    
    elapsed_min += 1
    print('elapsed_min = ' + str(elapsed_min))
    num_ones = np.nonzero(board == 1)[0].size
    print('num_ones = ' + str(num_ones))
    if num_ones == 0:
        break
    else:
        board_state_oxygen = BoardStateOxygen(board, next_nodes)