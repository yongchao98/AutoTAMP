import copy
import numpy as np
from PWLPlan import plan, Node
from vis import vis
import time
import os
import openai
from openai_func import *
import ast
import re

def test(domain, input_stl_original,  prop2block_dir, x0 = [-1., -1], goal = [1, 1],tmax = 50., vmax = 5.):
    input_stl = copy.deepcopy(input_stl_original)

    while not (len(input_stl) ==1 and type(input_stl[0]) != str):
        for i in range(len(input_stl) - 1, -1, -1):
            if type(input_stl[i]) != str:
                pass
            elif input_stl[i][:5] == 'enter':
                input_stl[i] = prop2block_dir['prop_' + input_stl[i][10:-1]][-1]
                phi = Node('mu', info={'A': input_stl[i][0], 'b': input_stl[i][1]})
                input_stl.pop(i)
                input_stl.insert(i,phi)
                if i==0 or type(input_stl[i-1]) != str or not (input_stl[i-1][0:4]=='glob' and input_stl[i-1][0:4]=='fina'):
                    phi_2 = Node('F', deps=[phi, ], info={'int': [0, tmax]})
                    input_stl.pop(i)
                    input_stl.insert(i, phi_2)
            elif input_stl[i][:9] == 'not_enter':
                input_stl[i] = prop2block_dir['prop_' + input_stl[i][14:-1]][-1]
                phi = Node('negmu', info={'A': input_stl[i][0], 'b': input_stl[i][1]})
                input_stl.pop(i)
                input_stl.insert(i, phi)
                if i==0 or type(input_stl[i-1]) != str:
                    phi_2 = Node('A', deps=[phi, ], info={'int': [0, tmax]})
                    input_stl.pop(i)
                    input_stl.insert(i, phi_2)
            elif input_stl[i] == 'and' or input_stl[i] == 'or':
                phi = Node(input_stl[i], deps=[input_stl[i+1], input_stl[i+2]])
                input_stl.pop(i+2)
                input_stl.pop(i+1)
                input_stl.pop(i)
                input_stl.insert(i, phi)
            elif input_stl[i] == 'globally':
                phi = Node('A', deps=[input_stl[i+1], ], info={'int': [0, tmax]})
                input_stl.pop(i+1)
                input_stl.pop(i)
                input_stl.insert(i, phi)
            elif input_stl[i] != 'globally' and input_stl[i].split(' ')[0] == 'globally':
                s = copy.deepcopy(input_stl[i])
                # Find all instances of the pattern
                matches = re.findall(r'\[([^\]]+)\]', s)
                # For each match, split the string by comma and strip whitespace
                time_expressions = [item.strip() for match in matches for item in match.split(',')]
                # Convert numerical strings to integers and leave 'infinite' as string
                time_expressions = [int(item) if item.isdigit() else item for item in time_expressions]

                if len(time_expressions) == 2:
                    time_int1 = int(time_expressions[0])
                    if time_expressions[1] == 'infinite':
                        time_int2 = tmax
                    else:
                        time_int2 = time_expressions[1]
                else: print('error')
                phi = Node('A', deps=[input_stl[i+1], ], info={'int': [time_int1, time_int2]})
                input_stl.pop(i+1)
                input_stl.pop(i)
                input_stl.insert(i, phi)
            elif input_stl[i] == 'finally':
                phi = Node('F', deps=[input_stl[i+1], ], info={'int': [0, tmax]})
                input_stl.pop(i+1)
                input_stl.pop(i)
                input_stl.insert(i, phi)
            elif input_stl[i] != 'finally' and input_stl[i].split(' ')[0] == 'finally':
                s = copy.deepcopy(input_stl[i])
                # Find all instances of the pattern
                matches = re.findall(r'\[([^\]]+)\]', s)
                # For each match, split the string by comma and strip whitespace
                time_expressions = [item.strip() for match in matches for item in match.split(',')]
                # Convert numerical strings to integers and leave 'infinite' as string
                time_expressions = [int(item) if item.isdigit() else item for item in time_expressions]

                if len(time_expressions) == 2:
                    time_int1 = int(time_expressions[0])
                    if time_expressions[1] == 'infinite':
                        time_int2 = tmax
                    else:
                        time_int2 = time_expressions[1]
                else: print('error')
                phi = Node('F', deps=[input_stl[i+1], ], info={'int': [time_int1, time_int2]})
                input_stl.pop(i+1)
                input_stl.pop(i)
                input_stl.insert(i, phi)
            elif input_stl[i] == 'until':
                phi = Node('U', deps=[input_stl[i + 1], input_stl[i + 2]], info={'int': [0, tmax]})
                input_stl.pop(i+2)
                input_stl.pop(i+1)
                input_stl.pop(i)
                input_stl.insert(i, phi)
            elif input_stl[i] != 'until' and input_stl[i].split(' ')[0] == 'until':
                s = copy.deepcopy(input_stl[i])
                # Find all instances of the pattern
                matches = re.findall(r'\[([^\]]+)\]', s)
                # For each match, split the string by comma and strip whitespace
                time_expressions = [item.strip() for match in matches for item in match.split(',')]
                # Convert numerical strings to integers and leave 'infinite' as string
                time_expressions = [int(item) if item.isdigit() else item for item in time_expressions]

                if len(time_expressions) == 2:
                    time_int1 = int(time_expressions[0])
                    if time_expressions[1] == 'infinite':
                        time_int2 = tmax
                    else:
                        time_int2 = time_expressions[1]
                else: print('error')
                phi = Node('U', deps=[input_stl[i + 1], input_stl[i + 2]], info={'int': [time_int1, time_int2]})
                input_stl.pop(i+2)
                input_stl.pop(i+1)
                input_stl.pop(i)
                input_stl.insert(i, phi)
    print('Finish parsing STL!')
    spec = input_stl[0]

    x0s = [x0,]
    specs = [spec,]
    goals = [goal, ]
    if domain == 'chip':
        PWL = plan(x0s, specs, bloat=0.18, MIPGap=0.99, num_segs=30, tmax=tmax, vmax=vmax)
    elif domain == 'HouseWorld':
        PWL = plan(x0s, specs, bloat=0.05, size=0.11 / 2, num_segs=20, tmax=tmax, vmax=vmax, hard_goals=goals)

    return x0s, PWL

def NL2action(index, saving_path, original_sent = 'Go to one room.', start_position = [-0.5, -1.1], end_position = [1.15, 1.15], syntactic_correct_loop = True, semantic_correct_loop = True, model_name = 'gpt-4', environment = 'env1', domain = 'chip'):
    time_start_total = time.time()
    time_semantic = 0
    time_total = 0
    time_syntactic = 0
    semantic_iteration_times = 0
    syntactic_iteration_times = 0
    #print('\n\nStart the new round of NL2action!\n\n')
    wall_half_width = 0.1
    A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])

    if domain == 'chip':
        if environment == 'env1':
            # Chip environment1
            _doors = []
            _doors.append(np.array([2, 2, 0, 1], dtype=np.float64))
            _doors.append(np.array([6, 6, 5, 6], dtype=np.float64))
            _doors.append(np.array([6, 8, 2, 2], dtype=np.float64))
            _doors.append(np.array([0, 2, 4, 4], dtype=np.float64))
            _doors.append(np.array([7, 8, 6, 6], dtype=np.float64))

            doors = []
            for index_env, door in enumerate(_doors):
                if door[0] == door[1]:
                    door[0] -= wall_half_width
                    door[1] += wall_half_width
                elif door[2] == door[3]:
                    door[2] -= wall_half_width
                    door[3] += wall_half_width
                else:
                    raise ValueError('wrong shape for axis-aligned door')
                door *= np.array([-1, 1, -1, 1])
                doors.append(door.tolist() + ['door' + str(index_env + 1)])

            _keys = []
            _keys.append(np.array([5, 1], dtype=np.float64))
            _keys.append(np.array([3, 3], dtype=np.float64))
            _keys.append(np.array([1, 1], dtype=np.float64))
            _keys.append(np.array([7, 1], dtype=np.float64))
            _keys.append(np.array([3, 5], dtype=np.float64))

            keys = []
            key_half_width = 0.55
            for index_env, key in enumerate(_keys):
                key = np.array(
                    [-(key[0] - key_half_width), (key[0] + key_half_width), -(key[1] - key_half_width),
                     (key[1] + key_half_width)])
                keys.append(key.tolist() + ['key' + str(index_env + 1)])

            goals = []
            b = np.array([-0.5, 1.5, -6.5, 7.5], dtype=np.float64)
            goals.append(b.tolist() + ['goal'])
            b2 = np.array([-6.7, 7.5, -3.7, 4.5], dtype=np.float64)
            goals.append(b2.tolist() + ['goal'])

            _walls = []

            _walls.append(np.array([0, 0, 0, 8], dtype=np.float64))
            _walls.append(np.array([8, 8, 0, 8], dtype=np.float64))
            _walls.append(np.array([0, 8, 0, 0], dtype=np.float64))
            _walls.append(np.array([0, 8, 8, 8], dtype=np.float64))
            _walls.append(np.array([0, 7, 6, 6], dtype=np.float64))
            _walls.append(np.array([2, 2, 1, 4], dtype=np.float64))
            _walls.append(np.array([2, 4, 4, 4], dtype=np.float64))
            _walls.append(np.array([4, 4, 4, 6], dtype=np.float64))
            _walls.append(np.array([6, 6, 0, 5], dtype=np.float64))

            walls = []
            for wall in _walls:
                if wall[0] == wall[1]:
                    wall[0] -= wall_half_width
                    wall[1] += wall_half_width
                elif wall[2] == wall[3]:
                    wall[2] -= wall_half_width
                    wall[3] += wall_half_width
                else:
                    raise ValueError('wrong shape for axis-aligned wall')
                wall *= np.array([-1, 1, -1, 1])
                walls.append(wall.tolist() + ['wall'])

            tag_and_shape = {
                'green': keys,
                'blue': goals,
                'red': doors,
                'black': walls}
        elif environment == 'env2':
            # Chip environment2

            _walls = []

            _walls.append(np.array([0, 0, 0, 8], dtype=np.float64))
            _walls.append(np.array([8, 8, 0, 8], dtype=np.float64))
            _walls.append(np.array([0, 8, 0, 0], dtype=np.float64))
            _walls.append(np.array([0, 8, 8, 8], dtype=np.float64))
            _walls.append(np.array([3.5, 7, 6, 6], dtype=np.float64))
            _walls.append(np.array([0, 2.5, 6, 6], dtype=np.float64))
            _walls.append(np.array([2, 4, 1, 1], dtype=np.float64))
            _walls.append(np.array([5, 6, 1, 1], dtype=np.float64))
            _walls.append(np.array([2, 2, 1, 4], dtype=np.float64))
            _walls.append(np.array([2, 4, 4, 4], dtype=np.float64))
            _walls.append(np.array([4, 4, 4, 6], dtype=np.float64))
            _walls.append(np.array([2, 2, 4, 6], dtype=np.float64))
            _walls.append(np.array([6, 6, 0, 5], dtype=np.float64))

            walls = []
            for wall in _walls:
                if wall[0] == wall[1]:
                    wall[0] -= wall_half_width
                    wall[1] += wall_half_width
                elif wall[2] == wall[3]:
                    wall[2] -= wall_half_width
                    wall[3] += wall_half_width
                else:
                    raise ValueError('wrong shape for axis-aligned wall')
                wall *= np.array([-1, 1, -1, 1])
                walls.append(wall.tolist() + ['wall'])

            tag_and_shape = {
                'red': [[-2.5, 3.5, -5.9, 6.1, 'door1'], [-5.9, 6.1, -5, 6, 'door2'], [-4, 5, -0.9, 1.1, 'door3']],
                'green': [[-2.5, 2.9, -4.5, 4.9, 'key1'], [-3.4, 3.8, -5.4, 5.8, 'key2'], [-6.5, 7.5, -1.5, 2.5, 'key3']],
                'black': walls,
                'blue': [[-0.5, 1.5, -6.5, 7.5, 'goal'], [-2.5, 3.5, -1.7, 2.7, 'goal'], [-4.5, 5.5, -2, 3, 'goal'],
                         [-0.5, 1.5, -3.5, 4.5, 'goal']]}
        elif environment == 'env3':
            # Chip environment3
            _walls = []

            _walls.append(np.array([0, 0, 0, 8], dtype=np.float64))
            _walls.append(np.array([8, 8, 0, 8], dtype=np.float64))
            _walls.append(np.array([0, 8, 0, 0], dtype=np.float64))
            _walls.append(np.array([0, 8, 8, 8], dtype=np.float64))
            _walls.append(np.array([3.5, 7, 6, 6], dtype=np.float64))
            _walls.append(np.array([0, 2.5, 6, 6], dtype=np.float64))
            _walls.append(np.array([2, 4, 1, 1], dtype=np.float64))
            _walls.append(np.array([5, 6, 1, 1], dtype=np.float64))
            _walls.append(np.array([2, 2, 1, 4], dtype=np.float64))
            _walls.append(np.array([2, 4, 4, 4], dtype=np.float64))
            _walls.append(np.array([4, 4, 4, 6], dtype=np.float64))
            _walls.append(np.array([2, 2, 4, 6], dtype=np.float64))
            _walls.append(np.array([6, 6, 0, 5], dtype=np.float64))

            wall_data = []
            for wall in _walls:
                if wall[0] == wall[1]:
                    wall[0] -= wall_half_width
                    wall[1] += wall_half_width
                elif wall[2] == wall[3]:
                    wall[2] -= wall_half_width
                    wall[3] += wall_half_width
                else:
                    raise ValueError('wrong shape for axis-aligned wall')
                wall *= np.array([-1, 1, -1, 1])
                wall_data.append(wall.tolist())

            walls_with_tags = [data + ['wall'] for data in wall_data]

            tag_and_shape = {
                'red': [[-2.5, 3.5, -5.9, 6.1, 'door1'], [-7, 8, -5.9, 6.1, 'door2'], [-5.9, 6.1, -5, 6, 'door3'],
                        [-4, 5, -0.9, 1.1, 'door4'], [-6, 8, -0.9, 1.1, 'door5'], [0, 2, -2.9, 3.1, 'door6'],
                        [0, 2, -1.9, 2.1, 'door7']],
                'green': [[-2.5, 2.9, -4.5, 4.9, 'key1'], [-3.2, 3.8, -7.2, 7.8, 'key2'], [-3.4, 3.8, -5.4, 5.8, 'key3'],
                          [-6.5, 7.5, -1.5, 2.5, 'key4'], [-4.5, 5.5, -6.5, 7.5, 'key5'], [-2.2, 2.9, -5.2, 5.9, 'key6'],
                          [-7.3, 7.8, -0.2, 0.7, 'key7']],
                'black': walls_with_tags,
                'blue': [[-0.5, 1.5, -6.5, 7.5, 'goal'], [-2.5, 3.5, -1.7, 2.7, 'goal'], [-4.5, 5.5, -2, 3, 'goal'],
                         [-0.5, 1.5, -3.5, 4.5, 'goal'], [-6.5, 7.1, -0.2, 0.8, 'goal']]}

    elif domain == 'HouseWorld':
        wall_half_width = 0.05
        A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
        walls = []

        wall_half_len = 1.5
        walls.append(np.array([-wall_half_len, -wall_half_len, -wall_half_len, wall_half_len], dtype=np.float64))
        walls.append(np.array([wall_half_len, wall_half_len, -wall_half_len, wall_half_len], dtype=np.float64))
        walls.append(np.array([-wall_half_len, wall_half_len, -wall_half_len, -wall_half_len], dtype=np.float64))
        walls.append(np.array([-wall_half_len, wall_half_len, wall_half_len, wall_half_len], dtype=np.float64))

        wall_data = []
        for wall in walls:
            if wall[0] == wall[1]:
                wall[0] -= wall_half_width
                wall[1] += wall_half_width
            elif wall[2] == wall[3]:
                wall[2] -= wall_half_width
                wall[3] += wall_half_width
            else:
                raise ValueError('wrong shape for axis-aligned wall')
            wall *= np.array([-1, 1, -1, 1])
            wall_data.append(wall.tolist())

        walls_with_tags = [data + ['wall'] for data in wall_data]

            # LTLMOP environment
        tag_and_shape = {'cyan': [[1.2, -0.8, 1.4, -0.7, 'Kitchen']], 'red': [[0, 0.9, 1.4, -0.7, 'RestRoom2']],
                         'green': [[-0.2, 1.43, -0.8, 1.43, 'MasterBedroom']],
                         'pink': [[-0.6, 1.43, -0.2, 0.8, 'Bedroom']],
                         'blue': [[0.5, 0.5, 0.5, 0.5, 'LivingRoom'], [1.2, -0.7, 0.05, 0.5, 'ExerciseRoom']],
                         'yellow': [[1.4, -0.2, -0.8, 1.43, 'RestRoom']],
                         'purple': [[0.7, -0.3, 1.4, -0.8, 'DiningRoom']],
                         'black': walls_with_tags}
    else:
        raise ValueError('unknown domain')

    # Start the parsing and planning
    #print('Start the parsing and planning')
    plots = []
    prop2block_dir = {}

    i = 0
    for color, block_array in tag_and_shape.items():
        for block_item_list in block_array:
            block_item = block_item_list[:-1]
            block_item_func_str = block_item_list[-1]
            B_item = (A, np.array(block_item, dtype=np.float64))
            plots.append([[B_item, ], color, block_item_func_str])
            i = i + 1
            prop2block_dir['prop_' + str(i)] = [color, block_item, block_item_func_str, B_item]

    # First round
    action_list = 'available scene objects: '
    for i in range(len(prop2block_dir.items())):
      prop_item_list = prop2block_dir['prop_'+str(i+1)]
      action_list += ('[name : room' + str(i+1) + ', color: ' + prop_item_list[0] + ', function: ' + prop_item_list[2] + ', position and size: ' + '(' + str(prop_item_list[1])[1:-1] +')' + '], ')

    action_list = action_list[:-2] + '\n'
    action_list += 'available actions: [enter(), not_enter()]'

    part1="Please help me detect the actions in the sentence and transform the action expression into corresponding Signal Temporal Logics (STL) representation with closest meanings. The operators are: imply, and, equal, until, globally, finally, or. The STL should follow pre-order expression. The until, finally, and globally operators can be appended with time expressions. The time is integer or 'infinite' to express infinite time. Some examples of natural language and STL pairs are:\nnatural language: only under the case of going to room2, will entering room_1 not happen\nSTL:  ['imply', 'not_enter(room_1)', 'enter(room_2)']\n\nnatural language: going into room_1 always follows with entering room_2.\nSTL:  ['globally', 'imply', 'enter(room_1)', 'finally', 'enter(room_2)']\n\nnatural language: only under the case of going to room2, will entering room_1 not happen\nSTL:  ['imply', 'not_enter(room_1)', 'enter(room_2)']\n\nnatural language: Maintain enter(room_1) until enter(room_2) is satisfied.\nSTL:  ['globally', 'until', 'enter(room_1)', 'enter(room_2)']\n\nnatural language: Go to room1 and always avoid both room2 and room3.\nSTL:  ['and', 'finally', 'enter(room_1)', 'globally', 'and', 'negation', 'enter(room_2)', 'negation', 'enter(room_3)']\n\nnatural language: If reaching room1 happens before reaching room_3 then start room_2 and cancel ( room_4 ) anytime within 0 to 10 timesteps.\nSTL:  ['globally', 'imply', 'and', 'enter(room_1)', 'finally', 'enter(room_3)', 'and', 'enter(room_2)', 'finally', 'negation', 'enter(room_4)']\n\nnatural language: For time steps between 0 and 20, until enter(room_1) and enter(room_2) is true, don’t start enter(room_3).\nSTL:  ['globally [0,20]', 'until', 'negation', 'enter(room_3)', 'and', 'enter(room_1)', 'enter(room_2)']\n\nnatural language: If room_1 and room_2 and not room_3 or room_4, then room_5 happens after 10 timesteps.\nSTL:  ['imply', 'and', 'and', 'enter(room_1)', 'enter(room_2)', 'negation', 'or', 'enter(room_3)', 'enter(room_4)', 'finally [10,infinite]', 'enter(room_5)']\n\nI will give you the position and size of each box in the whole environment and the instruction is to enter or avoid the box. Each box is of square shape, I will give you (x_start, x_end, y_start, y_end) to describe the shape of square. x_start, x_end denote the boundary of squares in x coordinates. y_start, y_end denote the boundary of squares in y coordinates.\n\nHere are examples:\nInput:\navailable scene objects: ['name' : room1, 'color': yellow, 'position and size': (-1, -0.7, -0.25, 0.5)], ['name' : room2, 'color': red, 'position and size': (0, 0.9, -1, -0.5)], ['name' : room3, 'color': green, 'position and size': (0.2, 0.7, 0.8, 1.2)], ['name' : room4, 'color': blue, 'position and size': (-0.4, 0.4, -0.4, 0.4)], ['name' : room5, 'color': blue, 'position and size': (0.6, 0.8, -0.2, 0.2)],\navailable actions: [enter(), not_enter()]\nsentence: Finally reach the green region, and you have to go to cyan area ahead to enter yellow room.\nOutput:\ntransformed sentence: finally prop_1 and prop_2.\n'prop_1' : ['enter(room3)'] ; 'prop_2' : ['until', 'negation', 'enter(room1)', 'enter(room4)']\n\nInput:\navailable scene objects: ['name' : room1, 'function': key1 for door1],  ['name' : room2, 'function': key2 for door2],  ['name' : room3, 'function': key3 for door3],  ['name' : room4, 'function': key4 for door4],  ['name' : room5, 'function': key5 for door5],  ['name' : room6, 'function': door1], ['name' : room7, 'function': door2], ['name' : room8, 'function': door3], ['name' : room9, 'function': door4], ['name' : room10, 'function': door5], ['name' : room11, 'function': goal], ['name' : room12, 'function': walls],\navailable actions: [enter(), not_enter()]\nsentence: Finally reach the goal region, and you have to get the corresponding key ahead to open each door, such as entering key1 before door1, remember not touch the wall at any time.\nOutput:\ntransformed sentence: finally prop_1 and prop_2 and globally prop_3.\n'prop_1' : ['enter(room11)'] ; 'prop_2' : ['and', 'and', 'and', 'and', 'until', 'negation', 'enter(room6)', 'enter(room1)', 'until', 'negation', 'enter(room7)', 'enter(room2)', 'until', 'negation', 'enter(room8)', 'enter(room3)', 'until', 'negation', 'enter(room9)', 'enter(room4)', 'until', 'negation', 'enter(room10)', 'enter(room5)'] ; 'prop_3' : ['not_enter(room12)']\n\nInput:\navailable scene objects: ['name' : room1, 'function': goal region, 'color': green],  ['name' : room2, 'function': goal region, 'color': green],  ['name' : room3, 'function': goal region, 'color': green],  ['name' : room7, 'function': charging station, 'color': blue], ['name' : room12, 'function': walls],\navailable actions: [enter(), not_enter()]\nsentence: room_1, then room_2 and stay there for 5 seconds, remember always not room_12.\nOutput:\ntransformed sentence: prop_1 and prop_2 and globally prop_3.\n'prop_1' : ['enter(room1)'] ; 'prop_2' : ['finally', 'globally [0,5]', 'prop_2'] ; 'prop_3' : ['not_enter(room12)']\n\nInput:\navailable scene objects: ['name' : room1, 'function': goal region, 'color': green],  ['name' : room2, 'function': goal region, 'color': green],  ['name' : room3, 'function': goal region, 'color': green],  ['name' : room7, 'function': charging station, 'color': blue], ['name' : room12, 'function': walls],\navailable actions: [enter(), not_enter()]\nsentence: Every rover should room_3 within 40 time units every time they leave room_7. After room_1, the rover should room_2 within 20 time units.\nOutput:\ntransformed sentence: globally prop_1 and prop_2.\n'prop_1' : ['imply', 'not_enter(room7)', 'finally [0,40]', 'enter(room3)'] ; 'prop_2' : ['imply', 'enter(room1)', 'finally [0,20]', 'enter(room2)']\n\nInput:\navailable scene objects: ['name' : room1, 'function': goal region, 'color': green],  ['name' : room2, 'function': goal region, 'color': green],  ['name' : room3, 'function': goal region, 'color': green],  ['name' : room4, 'function': goal region, 'color': green], ['name' : room5, 'function': transmitting region, 'color': green],  ['name' : room6, 'function': transmitting region, 'color': green], ['name' : room7, 'function': charging station, 'color': blue], ['name' : room12, 'function': walls],\navailable actions: [enter(), not_enter()]\nsentence:1) Every rover should visit the charging station (blue) within 10 time units every time they leave the charging station; 2) After visiting a goal region, the rover should visit a transmitter (yellow) within 5 time units, to transmit the collected data to the remote control; 3) The rovers should avoid the walls (black) and each other. 4) visit all the goal regions\nOutput:\ntransformed sentence: globally prop_1 and globally prop_2 and globally prop_3 and prop_4.\n'prop_1' : ['imply', 'not_enter(room7)', 'finally [0,10]', 'enter(room7)'] ; 'prop_2' : ['imply', 'or', 'or', 'or', 'enter(room1)', 'enter(room2)', 'enter(room3)', 'enter(room4)', 'finally [0,5]', 'or', 'enter(room5)', 'enter(room6)'] ; 'prop_3' : ['not_enter(room12)'] ; 'prop_4' : ['and', 'and', 'and', 'enter(room1)', 'enter(room2)', 'enter(room3)', 'enter(room4)']\n\nInput:\navailable scene objects: [name : room1, color: cyan, function: Kitchen, position and size: (1.2, -0.8, 1.4, -0.7)], [name : room2, color: red, function: RestRoom2, position and size: (0, 0.9, 1.4, -0.7)], [name : room3, color: green, function: MasterBedroom, position and size: (-0.2, 1.43, -0.8, 1.43)], [name : room4, color: pink, function: Bedroom, position and size: (-0.6, 1.43, -0.2, 0.8)], [name : room5, color: blue, function: LivingRoom, position and size: (0.5, 0.5, 0.5, 0.5)], [name : room6, color: blue, function: ExerciseRoom, position and size: (1.2, -0.7, 0.05, 0.5)], [name : room7, color: yellow, function: RestRoom, position and size: (1.4, -0.2, -0.8, 1.43)], [name : room8, color: purple, function: DiningRoom, position and size: (0.7, -0.3, 1.4, -0.8)]\navailable actions: [enter(), not_enter()]\nsentence: Go to one room with cyan color, then enter the bedroom and stay there for 5 seconds, finally reach the restroom. remember always do not touch the two true blue areas.\nOutput:\ntransformed sentence: prop_1 and prop_2 and finally prop_3 and globally prop_4.\n'prop_1' : ['enter(room1)'] ; 'prop_2' : ['finally', 'globally [0,5]', 'enter(room4)'] ; 'prop_3' : ['enter(room7)'] ; 'prop_4' : ['and', 'not_enter(room5)', 'not_enter(room6)']\n\n"

    part3 = '\nsentence: '
    user_prompt_1 = part1 + 'Input:\n' + action_list + part3 + original_sent + '\nOutput: '
    #print(user_prompt_1)
    if model_name == 'gpt-4':
        AP_and_lifted_NL = GPT_response_first_round(user_prompt_1, 'gpt-4')
    elif model_name == 'gpt-3':
        AP_and_lifted_NL = GPT_response_GPT_3(user_prompt_1)
    print(AP_and_lifted_NL)

    lifted_NL, AP_dict = parse_string(AP_and_lifted_NL)

    print(lifted_NL)
    TL_list = ast.literal_eval(GPT_NL2TL_preorder(lifted_NL, model_name_NL2TL = model_name))
    print(AP_dict)
    print(TL_list)

    time_syntactic_start = time.time()
    if syntactic_correct_loop == True:
        try:
            AP_and_lifted_NL, syntactic_iteration_times = func_syntactic_correct_loop(model_name, user_prompt_1, AP_and_lifted_NL)
            lifted_NL, AP_dict = parse_string(AP_and_lifted_NL)
            TL_list = ast.literal_eval(GPT_NL2TL_preorder(lifted_NL, model_name_NL2TL = model_name))
            if check_syntactic_correct(TL_list) != 'correct':
                # Second round
                if check_syntactic_correct(TL_list) != 'correct' and type(check_syntactic_correct(TL_list)) == int:
                    if check_syntactic_correct(TL_list) > 1:
                        TL_list = ['and'] * (check_syntactic_correct(TL_list) - 1) + TL_list
                    elif check_syntactic_correct(TL_list) < 1:
                        TL_list = TL_list[abs(check_syntactic_correct(TL_list)-1):]
        except:
            pass
    time_syntactic_end = time.time()
    time_syntactic = time_syntactic_end - time_syntactic_start

    # transform TL_list into input_stl
    input_stl = []
    for item in TL_list:
        if item[0:4] == 'prop':
            input_stl += AP_dict[item]
        else:
            input_stl += [item]

    input_stl = filter_negation_imply(input_stl)
    print('Input lifted TL: ', TL_list)
    print('input stl for list check: ', input_stl)

    if check_syntactic_correct_inverse_order(input_stl) == 'correct' and not 'negation' in input_stl and not 'imply' in input_stl:
        mark_syntactic = 1
        print('Input_NL: ', lifted_NL)
        print('Output STL: ', input_stl)
        _, PWLs = test(domain, input_stl, prop2block_dir, x0 = start_position, goal = end_position)
        if PWLs != [None,]:
            #results = vis(plots, PWLs)
            PWL = PWLs[0]
            position_time_list = [[P[0][0], P[0][1], P[1]] for P in PWL]
            with open(saving_path + '/myfile' + str(index) +'.txt', 'wb') as f:
                # save your array into the file
                np.savetxt(f, np.array(position_time_list), fmt='%f')
            f.close()

            trajectory_len_total = trajectory_len_cal(PWLs)
            print('trajectory_len_total: ', trajectory_len_total)

            time_semantic_start = time.time()
            if semantic_correct_loop == True:
                output_stl_1 = copy.deepcopy(input_stl)

                for index_semantic in range(3):
                    semantic_iteration_times += 1
                    print('\nSemantic loop' + str(index_semantic + 1) + ':\n\n')
                    #print(position_time_list)
                    #print('position_time_list length: ', len(position_time_list))
                    state_time_list = judge_trajectory_output_state(tag_and_shape, position_time_list, divide_path_time_ratio=1)
                    state_time_list_abbre = abbreviate_list_state_check(state_time_list)
                    user_prompt_2_original = '['
                    for index_abbre, item in enumerate(state_time_list_abbre):
                        if index_abbre != len(state_time_list_abbre) - 1:
                            user_prompt_2_original += 'in ' + str(item[0]) + ' ' + str(item[1]) + ' at time ' + str(
                                item[2]) + ', '
                        else:
                            user_prompt_2_original += 'in ' + str(item[0]) + ' ' + str(item[1]) + ' at time ' + str(
                                item[2]) + '].'

                    user_prompt_2 = 'Based on your predicted STL ' + str(
                        output_stl_1) + ' , the state sequence [[location, time]] of the generated trajectory is: ' + user_prompt_2_original + \
                        '\n \nPlease print the initial instruction again and check whether this state sequence follows the instruction. ' \
                        'Let us do it step by step, first specifically explain the semantic meanings of the instruction, and then list all the available rooms in the given environment, ' \
                        'then determine the rooms planned to visit or avoid and whether the trajectory is consistent. ' \
                        'Next modify or keep the final STL based on above analysis. First output your thinking steps and in the last line output the full final STL beginning with STL: . ' \
                        '\nOutput:'
                    LLM_response2 = GPT_response_second_round(user_prompt_1, AP_and_lifted_NL, user_prompt_2,
                                                              model_name_NL2TL=model_name)
                    output_stl_after_semantic = extract_list_for_semantic_check_LLM_response(LLM_response2)
                    if check_syntactic_correct(output_stl_after_semantic) != 'correct':
                        # Second round
                        if check_syntactic_correct(output_stl_after_semantic) != 'correct' and type(
                                check_syntactic_correct(output_stl_after_semantic)) == int:
                            if check_syntactic_correct(output_stl_after_semantic) > 1:
                                output_stl_after_semantic = ['and'] * (check_syntactic_correct(output_stl_after_semantic) - 1) + output_stl_after_semantic
                            elif check_syntactic_correct(output_stl_after_semantic) < 1:
                                output_stl_after_semantic = output_stl_after_semantic[abs(check_syntactic_correct(output_stl_after_semantic) - 1):]

                    print('The updated STL in semantic check iteration' + str(index_semantic) + ' is: ', output_stl_after_semantic)
                    if output_stl_after_semantic == output_stl_1:
                        print('The updated STL in semantic check iteration' + str(index_semantic) + ' is the same as the previous one, stop semantic check!')
                        break
                    else:
                        print('The updated STL in semantic check iteration' + str(index_semantic) + ' is different from the previous one, continue semantic check!')
                        output_stl_1 = copy.deepcopy(output_stl_after_semantic)
                        input_stl = copy.deepcopy(output_stl_after_semantic)

                        if check_syntactic_correct_inverse_order(
                            input_stl) == 'correct' and not 'negation' in input_stl and not 'imply' in input_stl:
                            _, PWLs = test(domain, input_stl, prop2block_dir, x0=start_position, goal=end_position)
                            if PWLs != [None, ]:
                                # results = vis(plots, PWLs)
                                PWL = PWLs[0]
                                position_time_list = [[P[0][0], P[0][1], P[1]] for P in PWL]
                                with open(saving_path + '/myfile' + str(index) + '.txt', 'wb') as f:
                                    # save your array into the file
                                    np.savetxt(f, np.array(position_time_list), fmt='%f')
                                f.close()
            time_semantic_end = time.time()
            time_semantic = time_semantic_end - time_semantic_start

        else: # PWLs == [None,]

            with open(saving_path + '/myfile' + str(index) +'.txt', 'wb') as f:
                # save your array into the file
                np.savetxt(f, np.array([0,0,0]), fmt='%f')
            f.close()
            print('No solution found!')
    else:
        mark_syntactic = 0
        print('Input_STL is wrong!')
        print(input_stl)
        with open(saving_path + '/myfile' + str(index) + '.txt',
                  'wb') as f:
            # save your array into the file
            np.savetxt(f, np.array([0,0]), fmt='%f')
    time_end_total = time.time()
    print('Total time: ', time_end_total - time_start_total)
    print('Syntactic check time: ', time_syntactic)
    print('Semantic check time: ', time_semantic)
    time_total = time_end_total - time_start_total
    with open(saving_path + '/myfile_time_consume' + str(index) + '.txt', 'w') as f:
        # save your array into the file
        f.write('Total time: ' + str(time_total) +'\n')
        f.write('Syntactic time: ' + str(time_syntactic) + '\n')
        f.write('Semantic time: ' + str(time_semantic) + '\n')
        f.write('Syntactic check iteration: ' + str(syntactic_iteration_times) + '\n')
        f.write('Semantic check iteration: ' + str(semantic_iteration_times))
    return input_stl, TL_list, mark_syntactic, time_total, time_syntactic, time_semantic
