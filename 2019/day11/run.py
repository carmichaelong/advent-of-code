# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt

@dataclass
class IntcodeState:
    program: np.array
    pointer_ind: int
    relative_base: int

@dataclass
class BoardState:
    board: np.array
    pos: np.array
    heading: str
    painted: np.array

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
            input_array[params[0]] = input_val
            op_ind += 2

        elif op == 4:
            params = np.array([input_array[op_ind+1]])
            params = parse_param_mode(digits, params, op_ind, relative_base)
            output.append(input_array[params[0]])
            op_ind += 2
            if len(output) == 2:
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
    heading = 'up'
    painted = np.zeros_like(board)
    return BoardState(board, pos, heading, painted)

def paint_board(board_state, prog_output):
    board = board_state.board
    pos = board_state.pos
    painted = board_state.painted
    board[pos[0], pos[1]] = prog_output[0]
    painted[pos[0], pos[1]] = 1
    
    return board_state

def update_pos_heading(board_state, prog_output):
    cur_heading = board_state.heading
    cur_pos = board_state.pos
    
    if cur_heading == 'up':
        if prog_output[1] == 0:
            cur_heading = 'left'
        elif prog_output[1] == 1:
            cur_heading = 'right'
    
    elif cur_heading == 'left':
        if prog_output[1] == 0:
            cur_heading = 'down'
        elif prog_output[1] == 1:
            cur_heading = 'up'
            
    elif cur_heading == 'down':
        if prog_output[1] == 0:
            cur_heading = 'right'
        elif prog_output[1] == 1:
            cur_heading = 'left'
            
    elif cur_heading == 'right':
        if prog_output[1] == 0:
            cur_heading = 'up'
        elif prog_output[1] == 1:
            cur_heading = 'down'
    
    board_state.heading = cur_heading
    
    if cur_heading == 'up':
        cur_pos[0] -= 1
    elif cur_heading == 'left':
        cur_pos[1] -= 1
    elif cur_heading == 'down':
        cur_pos[0] += 1
    elif cur_heading == 'right':
        cur_pos[1] += 1
    
    board_state.pos = cur_pos
    
    return board_state

def update_board_state(board_state, prog_output):
    board_state = paint_board(board_state, prog_output)
    board_state = update_pos_heading(board_state, prog_output)
    return board_state

def update_intcode_state(intcode_state, modified_prog, op_ind, relative_base):
    intcode_state.program = modified_prog
    intcode_state.pointer_ind = op_ind
    intcode_state.relative_base = relative_base
    return intcode_state
    
program = np.loadtxt('input.txt', delimiter=',', dtype='int64')
program_padded = np.zeros(10*program.size, dtype='int64')
program_padded[0:program.size] = program
intcode_state = IntcodeState(program_padded, 0, 0)
board_state = init_board_state(100, 100)
board_state.board[board_state.pos[0], board_state.pos[1]] = 1 #part 2
while True:
    input_color = board_state.board[board_state.pos[0], board_state.pos[1]]
    output, modified_prog, op_ind, relative_base = \
        run_program(intcode_state.program, input_val=input_color,
                    op_ind=intcode_state.pointer_ind,
                    relative_base=intcode_state.relative_base)
    intcode_state = update_intcode_state(intcode_state, modified_prog, op_ind, relative_base)
    if len(output) == 2:
        board_state = update_board_state(board_state, output)
    else:
        break

#answer_1 = np.sum(board_state.painted)
plt.imshow(board_state.board)