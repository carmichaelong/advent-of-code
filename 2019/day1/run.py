# -*- coding: utf-8 -*-

import numpy as np

def calc_fuel_for_this_module(initial_mass):
    this_fuel = np.floor_divide(initial_mass, 3) - 2
    if this_fuel <= 0:
        return 0
    else:
        return this_fuel + calc_fuel_for_this_module(this_fuel)

initial_masses = np.loadtxt('prob1.txt')
total_module_fuel = 0
for this_module in initial_masses:
    this_module_fuel = calc_fuel_for_this_module(this_module)
    total_module_fuel += this_module_fuel
