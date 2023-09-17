from env_and_optimize_single_agent import NL2action
from openai_func import *
import random
import os

# pre-define five parameters
syntactic_correct_loop = True # for syntactic check loop
semantic_correct_loop = True # for semantic check loop
domain = 'chip' # 'HouseWorld' or 'chip'
experiment_result_dir = 'path-to-the-code-directory/experiment_result' # the directory of experiment_result
model_name = 'gpt-4' # 'gpt-3' or 'gpt-4'


if domain == 'chip':
    for index in range(1):
        if syntactic_correct_loop == True and semantic_correct_loop == True:
            saving_path_test_case = experiment_result_dir + '/chip/' + model_name + '-with-syntactic-semantic'
        elif syntactic_correct_loop == True and semantic_correct_loop == False:
            saving_path_test_case = experiment_result_dir + '/chip/' + model_name + '-with-syntactic'
        elif syntactic_correct_loop == False and semantic_correct_loop == False:
            saving_path_test_case = experiment_result_dir + '/chip/' + model_name + '-without-check'

        if not os.path.exists(experiment_result_dir + '/chip/'):
            os.mkdir(experiment_result_dir + '/chip/')
        if not os.path.exists(saving_path_test_case):
            os.mkdir(saving_path_test_case)
        instruction_path = experiment_result_dir + '/chip/instr_dir'
        if not os.path.exists(instruction_path):
            os.mkdir(instruction_path)
        saving_path = saving_path_test_case + '/sent' + str(index)
        if not os.path.exists(saving_path):
            os.mkdir(saving_path)
        with open(instruction_path + '/myfile_sent' + str(index+1) + '.txt', 'r') as file:
            input_instruction = file.read().split('\n\n')
        #print(len(input_instruction))
        for item in input_instruction:
            print(item)
        with open(saving_path + '/stl_output.txt', 'a') as f_STL_output:
            for i in range(len(input_instruction)):
                ### For Chip Challenge
                if len(input_instruction[i]) > 5:
                    print('input_instruction' + str(i) + ': ', input_instruction[i])
                    try:
                        output_stl, TL_list, mark_syntactic, time_total, time_syntactic, time_semantic = NL2action(i, saving_path, input_instruction[i],
                                                                        start_position=[4.5 + random.uniform(-0.1, 0.1), 2 + random.uniform(-0.1, 0.1)],
                                                                        end_position=[1.15 + random.uniform(-0.1, 0.1), 1.15 + random.uniform(-0.1, 0.1)],
                                                                        syntactic_correct_loop=syntactic_correct_loop,
                                                                        semantic_correct_loop=semantic_correct_loop,
                                                                        model_name=model_name, # gpt-3 or gpt-4
                                                                        environment = 'env2', # env1 or env2 or env3
                                                                        domain = 'chip'
                                                                        )
                        if mark_syntactic == 1:
                            f_STL_output.write('Syntactic correct' + '\n')
                            f_STL_output.write(str(i) + '. ' + str(output_stl) + '\n\n')
                            f_STL_output.write(str(TL_list) + '\n\n')
                        if mark_syntactic == 0:
                            f_STL_output.write('Syntactic wrong' + '\n')
                            f_STL_output.write(str(i) + '. ' + str(output_stl) + '\n\n')
                            f_STL_output.write(str(TL_list) + '\n\n')
                    except:
                        pass
        f_STL_output.close()

elif domain == 'HouseWorld':
    ### For HouseWorld
    for index in range(10):
        instruction_path = experiment_result_dir + '/HouseWorld/instr_dir'
        saving_path_test_case = experiment_result_dir + '/HouseWorld/' + model_name + '-with-syntactic-semantic'
        if not os.path.exists(saving_path_test_case):
            os.mkdir(saving_path_test_case)

        saving_path = saving_path_test_case + '/sent' + str(index)
        if not os.path.exists(saving_path):
            os.mkdir(saving_path)

        with open(instruction_path + '/myfile_sent' + str(index+1) + '.txt', 'r') as file:
            input_instruction = file.read().split('\n\n')
        print('Length of different instructions of this kind is: ', len(input_instruction))
        for item in input_instruction:
            print(item)
        with open(saving_path + '/stl_output.txt', 'a') as f_STL_output:
            for i in range(len(input_instruction)):
                if len(input_instruction[i]) > 5:
                    print('input_instruction' + str(i) + ': ', input_instruction[i])
                    if index == 8:
                        try:
                            output_stl, TL_list, mark_syntactic, time_total, time_syntactic, time_semantic = NL2action(i, saving_path, input_instruction[i],
                                                                            start_position=[-1.35 + random.uniform(-0.1, 0.1), -1.1 + random.uniform(-0.1, 0.1)],
                                                                            end_position=[1.15 + random.uniform(-0.1, 0.1), 1.15 + random.uniform(-0.1, 0.1)],
                                                                            syntactic_correct_loop=syntactic_correct_loop,
                                                                            semantic_correct_loop=semantic_correct_loop,
                                                                            model_name=model_name,
                                                                            domain='HouseWorld'
                                                                            )
                            if mark_syntactic == 1:
                                f_STL_output.write('Syntactic correct' + '\n')
                                f_STL_output.write(str(i) + '. ' + str(output_stl) + '\n\n')
                                f_STL_output.write(str(TL_list) + '\n\n')
                            if mark_syntactic == 0:
                                f_STL_output.write('Syntactic wrong' + '\n')
                                f_STL_output.write(str(i) + '. ' + str(output_stl) + '\n\n')
                                f_STL_output.write(str(TL_list) + '\n\n')
                        except:
                            pass

                        try:
                            output_stl, TL_list, mark_syntactic, time_total, time_syntactic, time_semantic = NL2action(i + 10, saving_path, input_instruction[i],
                                                                            start_position=[-1.35 + random.uniform(-0.1, 0.1), -1.1 + random.uniform(-0.1, 0.1)],
                                                                            end_position=[1.15 + random.uniform(-0.1, 0.1), 1.15 + random.uniform(-0.1, 0.1)],
                                                                            syntactic_correct_loop=syntactic_correct_loop,
                                                                            semantic_correct_loop=semantic_correct_loop,
                                                                            model_name=model_name,
                                                                            domain='HouseWorld'
                                                                            )
                            if mark_syntactic == 1:
                                f_STL_output.write('Syntactic correct' + '\n')
                                f_STL_output.write(str(i + 10) + '. ' + str(output_stl) + '\n\n')
                                f_STL_output.write(str(TL_list) + '\n\n')
                            if mark_syntactic == 0:
                                f_STL_output.write('Syntactic wrong' + '\n')
                                f_STL_output.write(str(i + 10) + '. ' + str(output_stl) + '\n\n')
                                f_STL_output.write(str(TL_list) + '\n\n')
                        except:
                            pass

                    else:
                        try:
                            output_stl, TL_list, mark_syntactic, time_total, time_syntactic, time_semantic = NL2action(i, saving_path, input_instruction[i],
                                                                            start_position = [random.uniform(1.2, 1.41), random.uniform(-1.2, -1.41)],
                                                                            end_position = [random.uniform(-0.2, 0.2), random.uniform(1.2, 1.41)],
                                                                            syntactic_correct_loop = syntactic_correct_loop,
                                                                            semantic_correct_loop=semantic_correct_loop,
                                                                            model_name=model_name,
                                                                            domain='HouseWorld')
                            if mark_syntactic == 1:
                                f_STL_output.write('Syntactic correct' + '\n')
                                f_STL_output.write(str(i+10) + '. ' + str(output_stl) + '\n\n')
                                f_STL_output.write(str(TL_list) + '\n\n')
                            if mark_syntactic == 0:
                                f_STL_output.write('Syntactic wrong' + '\n')
                                f_STL_output.write(str(i+10) + '. ' + str(output_stl) + '\n\n')
                                f_STL_output.write(str(TL_list) + '\n\n')
                        except:
                            pass

                        try:
                            output_stl, TL_list, mark_syntactic, time_total, time_syntactic, time_semantic = NL2action(i+10, saving_path, input_instruction[i],
                                                                            start_position = [random.uniform(-1.4, -0.6), random.uniform(-0.1, -0.6)],
                                                                            end_position = [random.uniform(-0.2, 0.2), random.uniform(1.2, 1.41)],
                                                                            syntactic_correct_loop = syntactic_correct_loop,
                                                                            semantic_correct_loop=semantic_correct_loop,
                                                                            model_name=model_name,
                                                                            domain='HouseWorld')
                            if mark_syntactic == 1:
                                f_STL_output.write('Syntactic correct' + '\n')
                                f_STL_output.write(str(i+10) + '. ' + str(output_stl) + '\n\n')
                                f_STL_output.write(str(TL_list) + '\n\n')
                            if mark_syntactic == 0:
                                f_STL_output.write('Syntactic wrong' + '\n')
                                f_STL_output.write(str(i+10) + '. ' + str(output_stl) + '\n\n')
                                f_STL_output.write(str(TL_list) + '\n\n')
                        except:
                            pass

        f_STL_output.close()
