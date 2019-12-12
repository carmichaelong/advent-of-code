# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def fill_array(filename):
    num_array = []
    with open(filename) as fileobj:
        for line in fileobj:  
           for ch in line: 
               num_array.append(int(ch))
    num_array = np.array(num_array)
    return num_array

def fill_layers_flattened(num_array, num_pixels_layer):
    layers = []
    start_ind = 0
    while start_ind < num_array.size:
        layers.append(num_array[start_ind:start_ind+num_pixels_layer])
        start_ind += num_pixels_layer
    return layers

def update_image_from_layer(cur_image, input_layer):
    out_image = np.zeros_like(cur_image)
    for i, (px_image, px_layer) in enumerate(zip(cur_image, input_layer)):
        if px_image == 2:
            out_image[i] = px_layer
        else:
            out_image[i] = px_image
    return out_image

def calc_final_image_pixels_flattened(layers):
    image = 2*np.ones_like(layers[0])
    for layer in layers:
        image = update_image_from_layer(image, layer)
    return image

def unflatten_image(image_flattened, width, height):
    return np.reshape(image_flattened, (height, width))

pixel_width = 25
pixel_height = 6
num_pixels_layer = pixel_width*pixel_height

filename = 'day8_input.txt'
num_array = fill_array(filename)
layers = fill_layers_flattened(num_array, num_pixels_layer)
min_num_zeros = num_pixels_layer
for layer in layers:
    this_num_zeros = np.count_nonzero(layer == 0)
    if this_num_zeros < min_num_zeros:
        min_num_zeros = this_num_zeros
        min_num_zeros_layer = layer
answer_1 = np.count_nonzero(min_num_zeros_layer == 1) * np.count_nonzero(min_num_zeros_layer == 2)

image_flattened = calc_final_image_pixels_flattened(layers)
image = unflatten_image(image_flattened, pixel_width, pixel_height)
plt.imshow(image)
