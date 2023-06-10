from openai_func import *
import random
import os

domain = 'chip' # 'HouseWorld' or 'chip'
experiment_result_dir = 'path-to-submission_code/experiment_result' # the directory of experiment_result
model_name = 'gpt-4' # 'gpt-3' or 'gpt-4'

def end2end_prompt(sentence, start_location_list, end_location_list):
  part1="I am a mobile robot and I hope you can help me plan the trajectory to fulfill the navigation instruction. I will give you the position and size of each box in the whole environment and the instruction is to enter or avoid the box. Each box is of square shape, I will give you (x_start, x_end, y_start, y_end) to describe the shape of square. x_start, x_end denote the boundary of squares in x coordinates. y_start, y_end denote the boundary of squares in y coordinates.\n\nDuring navigation, the trajectory should always not touch the black wall. The entrance of the car in each box is denoted by the whole area of the car is within the box area. The avoidance of the car in each box is denoted by the complete division of the car and the box area. I will give you the starting and ending locations of the robot. The car should fulfill the instruction, start from the starting location and in the end stop at the ending location.\n\nCould you give me the trajectory to realize the above instruction. Please report a list of the specific locations of transition points and the time point at each specific location, and the final trajectory is by connecting the linear line between these transition points. The velocity of the robot should not exceed 50.\n\nHere are examples:\nInput:\navailable scene objects: [name : room1, color: cyan, function: Kitchen, position and size: (1.2, -0.8, 1.4, -0.7)], [name : room2, color: red, function: RestRoom2, position and size: (0, 0.9, 1.4, -0.7)], [name : room3, color: green, function: MasterBedroom, position and size: (-0.2, 1.43, -0.8, 1.43)], [name : room4, color: pink, function: Bedroom, position and size: (-0.6, 1.43, -0.2, 0.8)], [name : room5, color: blue, function: LivingRoom, position and size: (0.5, 0.5, 0.5, 0.5)], [name : room6, color: blue, function: ExerciseRoom, position and size: (1.2, -0.7, 0.05, 0.5)], [name : room7, color: yellow, function: RestRoom, position and size: (1.4, -0.2, -0.8, 1.43)], [name : room8, color: purple, function: DiningRoom, position and size: (0.7, -0.3, 1.4, -0.8)]\nStarting location: [-1.35, -1.1]\nEnding location: [1.15, 1.15]\nsentence: Go to one room with cyan color, then enter the bedroom and finally reach the restroom.\nOutput: \nx_location, y_location, time_point\n-1.35, -1.1, 0\n-1.0, -1.1, 0.05\n1.1, 0.3, 1\n0.12, -1.1, 2\n1.1, 1.2, 4\n\nInput:\navailable scene objects: [name : room1, color: cyan, function: Kitchen, position and size: (1.2, -0.8, 1.4, -0.7)], [name : room2, color: red, function: RestRoom2, position and size: (0, 0.9, 1.4, -0.7)], [name : room3, color: green, function: MasterBedroom, position and size: (-0.2, 1.43, -0.8, 1.43)], [name : room4, color: pink, function: Bedroom, position and size: (-0.6, 1.43, -0.2, 0.8)], [name : room5, color: blue, function: LivingRoom, position and size: (0.5, 0.5, 0.5, 0.5)], [name : room6, color: blue, function: ExerciseRoom, position and size: (1.2, -0.7, 0.05, 0.5)], [name : room7, color: yellow, function: RestRoom, position and size: (1.4, -0.2, -0.8, 1.43)], [name : room8, color: purple, function: DiningRoom, position and size: (0.7, -0.3, 1.4, -0.8)]\nStarting location: [-1.35, -1.1]\nEnding location: [1.15, 1.15]\nsentence: Go to one room with yellow color, but do not touch the two blue rooms\nOutput: \nx_location, y_location, time_point\n-1.35, -1.1, 0\n-1.35, 1.1, 1\n-0.7, 1.1, 1.5\n\nInput:\navailable scene objects: [name : room1, color: cyan, function: Kitchen, position and size: (1.2, -0.8, 1.4, -0.7)], [name : room2, color: red, function: RestRoom2, position and size: (0, 0.9, 1.4, -0.7)], [name : room3, color: green, function: MasterBedroom, position and size: (-0.2, 1.43, -0.8, 1.43)], [name : room4, color: pink, function: Bedroom, position and size: (-0.6, 1.43, -0.2, 0.8)], [name : room5, color: blue, function: LivingRoom, position and size: (0.5, 0.5, 0.5, 0.5)], [name : room6, color: blue, function: ExerciseRoom, position and size: (1.2, -0.7, 0.05, 0.5)], [name : room7, color: yellow, function: RestRoom, position and size: (1.4, -0.2, -0.8, 1.43)], [name : room8, color: purple, function: DiningRoom, position and size: (0.7, -0.3, 1.4, -0.8)]\nStarting location: [-1.35, -1.1]\nEnding location: [1.15, 1.15]\nsentence: Reach one room closest to the center location and stay there for five seconds.\nOutput: \nx_location, y_location, time_point\n-1.35, -1.1, 0\n0.5, 0.5, 2\n0.5, 0.5, 7\n\nInput:\navailable scene objects: [name : room1, color: cyan, function: Kitchen, position and size: (1.2, -0.8, 1.4, -0.7)], [name : room2, color: red, function: RestRoom2, position and size: (0, 0.9, 1.4, -0.7)], [name : room3, color: green, function: MasterBedroom, position and size: (-0.2, 1.43, -0.8, 1.43)], [name : room4, color: pink, function: Bedroom, position and size: (-0.6, 1.43, -0.2, 0.8)], [name : room5, color: blue, function: LivingRoom, position and size: (0.5, 0.5, 0.5, 0.5)], [name : room6, color: blue, function: ExerciseRoom, position and size: (1.2, -0.7, 0.05, 0.5)], [name : room7, color: yellow, function: RestRoom, position and size: (1.4, -0.2, -0.8, 1.43)], [name : room8, color: purple, function: DiningRoom, position and size: (0.7, -0.3, 1.4, -0.8)]"
  prompt_end2end = part1 + '\nStarting location: ' + str(start_location_list) + '\nEnding location: ' + str(end_location_list) + '\nsentence: ' + sentence + 'Output: \nx_location, y_location, time_point'
  return prompt_end2end


if domain == 'HouseWorld':
    for index in range(10):
        instruction_path = experiment_result_dir + '/HouseWorld/instr_dir'
        saving_path_test_case = experiment_result_dir + '/HouseWorld/' + model_name + '-end2end'
        if not os.path.exists(saving_path_test_case):
            os.mkdir(saving_path_test_case)

        saving_path = saving_path_test_case + '/sent' + str(index)
        if not os.path.exists(saving_path):
            os.mkdir(saving_path)
        with open(instruction_path + '/myfile_sent' + str(index+1) + '.txt', 'r') as file:
            input_instruction = file.read().split('\n\n')
        print('Length of different instructions of this kind is: ', len(input_instruction))

        for i in range(len(input_instruction)):
            if len(input_instruction[i]) > 5:
                print('input_instruction' + str(i) + ': ', input_instruction[i])
                if index == 8:
                    prompt = end2end_prompt(input_instruction[i], [-1.35, -1.1],[1.15, 1.15])
                    response = GPT_response_first_round(prompt, model_name_NL2TL=model_name)
                    with open(saving_path + '/myfile' + str(i) + '.txt',
                              'w') as f:
                        # save your array into the file
                        f.write(response)
                    f.close()

                    prompt = end2end_prompt(input_instruction[i], [-1.35, -0.6],[1.15, 1.35])
                    response = GPT_response_first_round(prompt, model_name_NL2TL=model_name)
                    with open(saving_path + '/myfile' + str(i + 10) + '.txt',
                              'w') as f:
                        # save your array into the file
                        f.write(response)
                    f.close()
                else:
                    prompt = end2end_prompt(input_instruction[i], [random.uniform(1.2, 1.41), random.uniform(-1.2, -1.41)],[random.uniform(-0.2, 0.2), random.uniform(1.2, 1.41)])
                    response = GPT_response_first_round(prompt, model_name_NL2TL=model_name)
                    with open(saving_path + '/myfile' + str(i) + '.txt',
                              'w') as f:
                        # save your array into the file
                        f.write(response)
                    f.close()

                    prompt = end2end_prompt(input_instruction[i], [random.uniform(-1.4, -0.6), random.uniform(-0.1, -0.6)],[random.uniform(-0.2, 0.2), random.uniform(1.2, 1.41)])
                    response = GPT_response_first_round(prompt, model_name_NL2TL=model_name)
                    with open(saving_path + '/myfile' + str(i+10) + '.txt',
                              'w') as f:
                        # save your array into the file
                        f.write(response)
                    f.close()
elif domain == 'chip':
    for index in range(1):
        saving_path_test_case = experiment_result_dir + '/chip/' + model_name + '-end2end'
        if not os.path.exists(saving_path_test_case):
            os.mkdir(saving_path_test_case)
        instruction_path = experiment_result_dir + '/chip/instr_dir'
        saving_path = saving_path_test_case + '/sent' + str(index)
        if not os.path.exists(saving_path):
            os.mkdir(saving_path)
        with open(instruction_path + '/myfile_sent' + str(index+1) + '.txt', 'r') as file:
            input_instruction = file.read().split('\n\n')
        print('Length of different instructions of this kind is: ', len(input_instruction))

        for i in range(len(input_instruction)):
            if len(input_instruction[i]) > 5:
                print('input_instruction' + str(i) + ': ', input_instruction[i])

                prompt = end2end_prompt(input_instruction[i],
                                        [4.5 + random.uniform(-0.1, 0.1), 2 + random.uniform(-0.1, -0.1)],
                                        [1.15 + random.uniform(-0.1, 0.1), 1.15 + random.uniform(-0.1, 0.1)])
                response = GPT_response_first_round(prompt, model_name_NL2TL=model_name)
                with open(saving_path + '/myfile' + str(i) + '.txt',
                          'w') as f:
                    # save your array into the file
                    f.write(response)
                f.close()

                prompt = end2end_prompt(input_instruction[i],
                                        [random.uniform(-1.4 + random.uniform(-0.1, 0.1), -0.6 + random.uniform(-0.1, 0.1)), random.uniform(-0.1 + random.uniform(-0.1, 0.1), -0.6 + random.uniform(-0.1, 0.1))],
                                        [random.uniform(-0.2 + random.uniform(-0.1, 0.1), 0.2 + random.uniform(-0.1, 0.1)), random.uniform(1.2 + random.uniform(-0.1, 0.1), 1.41 + random.uniform(-0.1, 0.1))])
                response = GPT_response_first_round(prompt, model_name_NL2TL=model_name)
                with open(saving_path + '/myfile' + str(i + 10) + '.txt',
                          'w') as f:
                    # save your array into the file
                    f.write(response)
                f.close()
