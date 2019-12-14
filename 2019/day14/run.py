# -*- coding: utf-8 -*-

import re
import numpy as np


def load_reaction_file(filename):
    names = []
    with open(filename) as f:
        for line in f:
            input_output_split = line.split('=>')
            input_split = re.findall(r'[^,\s]+', input_output_split[0])
            output_split = re.findall(r'[^,\s]+', input_output_split[1])
            
            for input_name in input_split[1::2]:
                if input_name not in names:
                    names.append(input_name)
                    
            for output_name in output_split[1::2]:
                if output_name not in names:
                    names.append(output_name)
                    
    input_matrix = np.zeros((len(names), len(names)), dtype=int)
    output_matrix = np.zeros_like(input_matrix, dtype=int)
    
    with open(filename) as f:
        for i, line in enumerate(f):
            input_output_split = line.split('=>')
            input_split = re.findall(r'[^,\s]+', input_output_split[0])
            output_split = re.findall(r'[^,\s]+', input_output_split[1])
            
            for j in range(0, len(input_split), 2):
                name_to_find = input_split[j+1]
                name_ind = names.index(name_to_find)
                input_matrix[i, name_ind] = input_split[j]
                    
            for j in range(0, len(output_split), 2):
                name_to_find = output_split[j+1]
                name_ind = names.index(name_to_find)
                output_matrix[i, name_ind] = output_split[j]
                
    return names, input_matrix, output_matrix

def is_done(names, input_need, output_made, num_fuel):
    fuel_ind = names.index('FUEL')
    if not output_made[fuel_ind] >= num_fuel:
        return False
    for i in range(output_made.size):
        if not names[i] == 'ORE':
            if input_need[i] > output_made[i]:
                return False
    return True

def calc_ore_needed(names, input_matrix, output_matrix, num_fuel=1):
    num_reactions = np.zeros((len(names),1))
        
    ore_ind = names.index('ORE')
    ore_reaction_inds = np.nonzero(input_matrix)[0][np.nonzero(input_matrix)[1] == ore_ind]
    
    fuel_ind = names.index('FUEL')
    fuel_reaction_ind = np.nonzero(output_matrix)[0][np.nonzero(output_matrix)[1] == fuel_ind]
    num_reactions[fuel_reaction_ind] = num_fuel
    
    input_need = np.sum(input_matrix*num_reactions, axis=0)
    output_made = np.sum(output_matrix*num_reactions, axis=0)
    output_made_prev = output_made.copy()
    
    while True:
#        if is_done(names, input_need, output_made, num_fuel):
#            break
#        for i in range(num_reactions.size):
        for i in np.nonzero(input_need > output_made)[0]:
            if not names[i] == 'ORE':
                if input_need[i] > output_made[i]:
                    reaction_ind = np.nonzero(output_matrix)[0][np.nonzero(output_matrix)[1] == i]
                    if not reaction_ind in ore_reaction_inds:
                        output_per_reaction = np.sum(output_matrix[reaction_ind,:])
                        input_needed = input_need[i]
                        num_reactions[reaction_ind] = np.ceil(input_needed / output_per_reaction)
        input_need = np.sum(input_matrix*num_reactions, axis=0)
        output_made = np.sum(output_matrix*num_reactions, axis=0)
        
        if (output_made_prev == output_made).all():
            break
        else:
            output_made_prev = output_made.copy()
    
    ore_ind = names.index('ORE')
    ore_needed = input_need[ore_ind]
    ore_output_inds = np.nonzero((output_matrix[ore_reaction_inds]))[1]
    ore_needed = 0
    for i in ore_output_inds:
        reaction_ind = np.nonzero(output_matrix)[0][np.nonzero(output_matrix)[1] == i]
        output_per_reaction = np.sum(output_matrix[reaction_ind,:])
        this_ore_needed = input_need[i]
        ore_reactions = np.ceil(this_ore_needed / output_per_reaction)
        ore_needed += ore_reactions*np.sum(input_matrix[reaction_ind,:])
        
    
    return ore_needed

names, input_matrix, output_matrix = load_reaction_file('input.txt')
ore_needed_1 = calc_ore_needed(names, input_matrix, output_matrix, num_fuel=1)

ore_budget = 1000000000000
num_fuel = 1330000
while True:
    if num_fuel % 100 == 0:
        print(num_fuel)
    ore_needed_2 = calc_ore_needed(names, input_matrix, output_matrix,
                                                    num_fuel=num_fuel)
    if ore_needed_2 > ore_budget:
        num_fuel -= 1 # go back one
        break
    else:
        num_fuel += 1