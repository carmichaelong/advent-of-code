# -*- coding: utf-8 -*-

import numpy as np

def calc_gravity(pos):
    num_rows = np.shape(pos)[0]
    num_col = np.shape(pos)[1]
    gravity = np.zeros_like(pos)
    for i in range(num_rows):
        this_gravity = np.zeros(num_col)
        for j in range(num_rows):
            if not i == j:
                this_gravity += np.sign(pos[j,:] - pos[i,:])
        gravity[i,:] = this_gravity
    return gravity

def simulate_step(pos, vel):
    gravity = calc_gravity(pos)
    vel += gravity
    pos += vel
    
    return pos, vel

def calc_total_energy(pos, vel):
    PE = np.sum(np.abs(pos), axis=1)
    KE = np.sum(np.abs(vel), axis=1)
    
    return np.sum(PE*KE)

init_pos = [[17, 5, 1],
           [-2, -8, 8],
            [7, -6, 14],
            [1, -10, 4]]

init_pos = np.array(init_pos)
init_vel = np.zeros_like(init_pos)
pos = np.array(init_pos)
vel = np.array(init_vel)
num_steps = 1000
for i in range(num_steps):
    pos, vel = simulate_step(pos, vel)
answer_1 = calc_total_energy(pos, vel)

x_pos_init = np.array(init_pos[:,[0]])
x_vel_init = np.array(init_vel[:,[0]])
x_pos = np.array(x_pos_init)
x_vel = np.array(x_vel_init)
x_count = 0

y_pos_init = np.array(init_pos[:,[1]])
y_vel_init = np.array(init_vel[:,[1]])
y_pos = np.array(y_pos_init)
y_vel = np.array(y_vel_init)
y_count = 0

z_pos_init = np.array(init_pos[:,[2]])
z_vel_init = np.array(init_vel[:,[2]])
z_pos = np.array(z_pos_init)
z_vel = np.array(z_vel_init)
z_count = 0

while True:
    x_pos, x_vel = simulate_step(x_pos, x_vel)
    x_count += 1
    if ((x_pos == x_pos_init).all() and (x_vel == x_vel_init).all()):
        break

while True:
    y_pos, y_vel = simulate_step(y_pos, y_vel)
    y_count += 1
    if ((y_pos == y_pos_init).all() and (y_vel == y_vel_init).all()):
        break
    
while True:
    z_pos, z_vel = simulate_step(z_pos, z_vel)
    z_count += 1
    if ((z_pos == z_pos_init).all() and (z_vel == z_vel_init).all()):
        break
    
answer_2 = np.lcm.reduce([x_count, y_count, z_count], dtype='int64')
