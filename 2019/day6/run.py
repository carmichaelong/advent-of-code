# -*- coding: utf-8 -*-

from dataclasses import dataclass

@dataclass
class Node:
    name: str
    parent: str

def count_num_transfers(traverse_1, traverse_2):
    diff_list = list(set(traverse_1)^set(traverse_2))
    return len(diff_list) + 2

def traverse_to_center(node, node_list):
    traverse_list = []
    parent_node = find_node_by_name(node.parent, node_list)
    while not parent_node == None:
        traverse_list.append(parent_node.name)
        parent_node = find_node_by_name(parent_node.parent, node_list)
    return traverse_list

def find_SAN_YOU_objects(node_list):
    for node in node_list:
        if node.name == 'SAN':
            SAN_node = find_node_by_name(node.parent, node_list)
        if node.name == 'YOU':
            YOU_node = find_node_by_name(node.parent, node_list)
    return SAN_node, YOU_node

def find_node_by_name(node_name, node_list):
    for node in node_list:
        if node_name == node.name:
            return node
    return None

def count_orbits(node_list):
    count = 0
    for node in node_list:
        count += 1
        parent_node = find_node_by_name(node.parent, node_list)
        while not parent_node == None:
            count += 1
            parent_node = find_node_by_name(parent_node.parent, node_list)
        
    return count

def construct_tree(lines_orbit):
    node_list = []
    for line in lines_orbit:
        split = line.split(')')
        name = split[1]
        parent = split[0]
        this_node = Node(name, parent)
        node_list.append(this_node)
        
    return node_list

def get_lines_from_file(filename):
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]

    return lines

lines = get_lines_from_file('day6_test_input_1.txt')
node_list = construct_tree(lines)
num_orbits = count_orbits(node_list)

lines = get_lines_from_file('day6_input.txt')
node_list = construct_tree(lines)
#num_orbits = count_orbits(node_list)

#lines = get_lines_from_file('day6_test_input_2.txt')
node_list = construct_tree(lines)
node_SAN, node_YOU = find_SAN_YOU_objects(node_list)
traverse_SAN = traverse_to_center(node_SAN, node_list)
traverse_YOU = traverse_to_center(node_YOU, node_list)
transfer_count = count_num_transfers(traverse_SAN, traverse_YOU)