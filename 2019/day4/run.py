# -*- coding: utf-8 -*-

import numpy as np

def check_single_adjacent_repeat_digits(number):
    num_str = str(number)
    has_single_adjacent_repeat_digits = False
    counter = 1
    for i in range(len(num_str)-1):
        if num_str[i] == num_str[i+1]:
            counter += 1
        else:
            if counter == 2:
                has_single_adjacent_repeat_digits = True
                break
            else:
                counter = 1
    if counter == 2:
        has_single_adjacent_repeat_digits = True
    return has_single_adjacent_repeat_digits

def check_repeat_adjacent_digits(number):
    num_str = str(number)
    has_repeat_adjacent_digits = False
    for i in range(len(num_str)-1):
        if num_str[i] == num_str[i+1]:
            has_repeat_adjacent_digits = True
            break
    return has_repeat_adjacent_digits

def check_increasing_digits(number):
    num_str = str(number)
    digits = np.zeros(len(num_str))
    for i in range(len(num_str)):
        digits[i] = int(num_str[i])
    has_increasing_digits = True
    for i in range(len(digits)-1):
        if num_str[i] > num_str[i+1]:
            has_increasing_digits = False
            break
    return has_increasing_digits

num_min = 356261
num_max = 846303
num_possible_1 = 0
for num in range(num_min, num_max, 1):
    if check_repeat_adjacent_digits(num) and check_increasing_digits(num):
        num_possible_1 += 1     
print(num_possible_1)

num_possible_2 = 0
for num in range(num_min, num_max, 1):
    if check_repeat_adjacent_digits(num) and check_increasing_digits(num) and check_single_adjacent_repeat_digits(num):
        num_possible_2 += 1
print(num_possible_2)
