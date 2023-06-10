# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import numpy as np
import copy
import ast
import re
import math

openai_api_key_name = 'sk-...'  # Register at https://beta.openai.com/ to get your API key

def GPT_response_GPT_3(original_sent):
    openai.api_key = openai_api_key_name
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=original_sent,
      temperature=0.0,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response['choices'][0]['text'][1:]


def GPT_response_first_round(user_prompt_1, model_name_NL2TL = 'gpt-4'):
  if model_name_NL2TL == 'gpt-4':
    openai.api_key = openai_api_key_name
    try:
      result = openai.ChatCompletion.create(
        model=model_name_NL2TL,
        messages=[
              {"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": user_prompt_1}
          ]
      )
    except:
      result = openai.ChatCompletion.create(
        model=model_name_NL2TL,
        messages=[
              {"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": user_prompt_1}
          ]
      )
    return result.choices[0]['message']['content']
  elif model_name_NL2TL == 'gpt-3':
    openai.api_key = openai_api_key_name
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=user_prompt_1,
      temperature=0.0,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response['choices'][0]['text'][1:]

def GPT_response_second_round(user_prompt_1, assistent_feed, user_prompt_2, model_name_NL2TL = 'gpt-4'):
  if model_name_NL2TL == 'gpt-4':
    openai.api_key = openai_api_key_name
    try:
      result = openai.ChatCompletion.create(
        model=model_name_NL2TL,
        messages=[
              {"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": user_prompt_1},
              {"role": "assistant", "content": assistent_feed},
              {"role": "user", "content": user_prompt_2}
          ]
      )
    except:
      result = openai.ChatCompletion.create(
        model=model_name_NL2TL,
        messages=[
              {"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": user_prompt_1},
              {"role": "assistant", "content": assistent_feed},
              {"role": "user", "content": user_prompt_2}
          ]
      )
    return result.choices[0]['message']['content']

  elif model_name_NL2TL == 'gpt-3':
    openai.api_key = openai_api_key_name
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=user_prompt_1 + '\nGPT-3 response:\n' + assistent_feed + '\nHuman feedback:\n' + user_prompt_2,
      temperature=0.0,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response['choices'][0]['text'][1:]


def GPT_NL2TL(lifted_NL, model_name_NL2TL = 'gpt-4'):
  NL2TL_prompt="Try to transform the following natural languages into signal temporal logics, the operators in the signal temporal logic are: negation, imply, and, equal, until, globally, finally, or . The time specification are integers larger or equal to 0, and use 'infinite' as the endless time.\nThe examples are as following:\nnatural language: If ( prop_2 ) is equivalent to ( prop_3 ) and also ( prop_4 ) , then the above scenario is equivalent to ( prop_1 ) .\nSTL: ( ( ( prop_2 equal prop_3 ) and prop_4 ) equal prop_1 )\n\nnatural language: For each time instant in the coming 145 to 584 time units either ( prop_1 ) or ( prop_2 ) should be detected , or else ( prop_3 ) .\nSTL: ( ( globally [145,584] ( prop_1 or prop_2 ) ) or prop_3 )\n\nnatural language: It is required that at a certain point within the next 317 to 767 time units the scenario in which ( prop_3 ) is equivalent to the scenario in which ( prop_2 ) happens , and only then ( prop_1 ) .\nSTL: ( ( finally [317,767] ( prop_3 equal prop_2 ) ) imply prop_1 )\n\nnatural language: In case that at some point ( prop_4 ) or ( prop_2 ) or ( prop_3 ) is detected and continued until then at some other point ( prop_1 ) should be detected as well .\nSTL: ( ( ( prop_4 or prop_2 ) or prop_3 ) until prop_1 )\n\nnatural language: ( prop_2 ) should happen and hold until at a certain time point during the 417 to 741 time units the scenario that ( prop_3 ) should happen then ( prop_1 ) , or else ( prop_4 ) .\nSTL: ( ( ( prop_2 until [417,741] prop_3 ) imply prop_1 ) or prop_4 )\n\nnatural language: For each time instant in the next 184 to 440 time units if it is not the case that ( prop_1 ) or ( prop_3 ) then ( prop_2 ) .\nSTL: ( ( globally [184,440] ( negation ( prop_1 or prop_3 ) ) ) imply prop_2 )\n\nnatural language: In case that ( prop_3 ) continues to happen until at some point during the first 391 to 525 time units that ( prop_2 ) happens , as well as ( prop_1 ) , and ( prop_4 ) then .\nSTL: ( ( ( prop_3 until [391,525] prop_2 ) and prop_1 ) and prop_4 )\n\nnatural language: If finally that ( prop_1 ) is not detected then ( prop_2 ) , then ( prop_3 ) .\nSTL: ( ( ( finally ( negation prop_1 ) ) imply prop_2 ) imply prop_3 )\n\nnatural language: It is not the case that ( prop_1 ) if and only if ( prop_2 ) is true , the above scenario will hold until ( prop_3 ) will be detected at some time point during the next 394 to 530 time units .\nSTL: ( ( negation ( prop_1 equal prop_2 ) ) until [394,530] prop_3 )\n\nnatural language:  If at some point ( prop_1 ) or ( prop_3 ) then ( prop_4 ) happens and this scenario will hold until at some other point during the 193 to 266 time units ( prop_2 ) is detected .\nSTL: ( ( ( prop_1 or prop_3 ) imply prop_4 ) until [193,266] prop_2 )\n\nnatural language:  It is not the case that ( prop_1 ) happens and continues to happen until at some point during the 77 to 432 time units ( prop_2 ) is detected , and ( prop_3 ) .\nSTL: ( ( negation ( prop_1 until [77,432] prop_2 ) ) and prop_3 )\n\nnatural language: ( prop_3 ) happens until a time in the next 5 to 12 units that ( prop_4 ) does not happen .\nSTL: ( prop_3 until [5,12] ( negation prop_4 ) )\n\nnatural language: The time that ( prop_3 ) happens is when ( prop_1 ) happens , and vice versa .\nSTL: ( prop_3 equal prop_1 )\n\nnatural language: It is required that both ( prop_2 ) and ( prop_4 ) happen at the same time, or else ( prop_3 ) happens and continues until ( prop_1 ) happens.\nSTL:  ( ( prop_2 and prop_4 ) or ( prop_3 until prop_1 ) )\n\nnatural language: ( prop_3 ) happens and continues until at some point during the 500 to 903 time units ( prop_1 ) happens , and in the same time ( prop_2 ) does not happen .\nSTL:  ( ( prop_3 until [500,903] prop_1 ) and ( negation prop_2 ) )\n\nnatural language: For each time instant in the next 107 to 513 time units ( prop_1 ) is true , or else ( prop_3 ) happens and ( prop_2 ) happens at the same time.\nSTL:  ( ( globally [107,513] prop_1 ) or ( prop_3 and prop_2 ) )\n\nnatural language: ( prop_1 ) or ( prop_2 ) happens and continues until at some point during the 142 to 365 time units ( prop_4 ) happens and ( prop_3 ) happens at the same time .\nSTL:  ( ( prop_1 or prop_2 ) until [142,365] ( prop_4 and prop_3 ) )\n\nnatural language: It is always the case that everytime when ( prop_1 ) and ( prop_2 ) then all of the following conditions hold : for each time point during the subsequent 4 to 47 time units ( prop_3 ) .\nSTL:  globally ( ( prop_1 and prop_2 ) imply ( globally [4,47] prop_3 ) )\n\nnatural language: at some time ( prop_1 ) and when possible ( prop_2 )\nSTL:  finally ( prop_1 and finally prop_2 )\n\nnatural language: at some time ( prop_1 ) and never ( prop_2 )\nSTL:  ( finally prop_1 ) and ( globally ( negation prop_2 ) )\n\nnatural language: when possible ( prop_1 ) and at some time ( prop_2 )\nSTL:  finally ( prop_1 and ( finally prop_2 ) )\n\nnatural language: never ( prop_1 ) or whenever ( prop_2 )\nSTL:  ( globally ( ( negation prop_1 ) ) or ( finally prop_2 ) )\n\nnatural language: when possible ( prop_1 ) and don't ( prop_2 )\nSTL:  finally ( prop_1 and ( negation prop_2 ) )\n\nnatural language: ( prop_1 ) or at any time ( prop_2 )\nSTL:  ( prop_1 or ( finally prop_2 ) )\n\nnatural language: Globally , if ( prop_1 ) then the following condition is true : at the same time the event that ( prop_2 ) ought to be detected and ( prop_3 ) .\nSTL:  globally ( prop_1 imply ( prop_2 and prop_3 ) )\n\nnatural language: at some time ( prop_1 ) or ( prop_2 )\nSTL:  finally ( prop_1 or prop_2 )\n\nnatural language: ( prop_1 ) and at some time ( prop_2 )\nSTL:  ( prop_1 and ( finally prop_2 ) )\n\nnatural language: whenever ( prop_1 ) and at any time ( prop_2 )\nSTL:  ( ( finally prop_1 ) and ( finally prop_2 ) )\n\nnatural language: whenever ( prop_1 ) or forever ( prop_2 )\nSTL:  ( ( finally prop_1 ) or ( globally prop_2 ) )\n\nnatural language: At the random time between 0 to 30 (prop_1) for 5 seconds, and at the random time between 0 to 30 (prop_2) for 5 seconds, and at the random time between 0 to 30 (prop_3) for 5 seconds.\nSTL: ( ( ( finally [0,30] ( globally [0,5] prop_1 ) ) and ( finally [0,30] ( globally [0,5] prop_2 ) ) ) and ( finally [0,30] ( globally [0,5] prop_3 ) ) )\n\nnatural language: At sometime between 1 to 25 stay at prop_1 for five seconds and always stay away from the prop_2 and prop_3 during 0 to 30 seconds.\nSTL: ( ( finally [1,25] ( globally [0,5] prop_1 ) ) and ( globally [0,30] ( negation prop_2 and negation prop_3 ) ) )\n\nnatural language: Always (prop_1) if not (prop_2).\nSTL: ( ( negation prop_2 ) imply ( globally prop_1 ) )\n\nnatural language: Always (prop_1) only if not (prop_2).\nSTL: ( (globally prop_1 ) imply ( negation prop_2 ) )\n\nnatural language: Avoid (prop_1) until (prop_2) lasts for 20 steps.\nSTL: ( ( negation prop_1 ) until ( globally [0, 20] prop_2 ) )\n\nnatural language: Wait till (prop_1) is complete, then, (prop_2) for next 20 units.\nSTL: ( ( finally prop_1 ) imply ( globally [0, 20] prop_2 ) )\n\nnatural language: ( prop_1 ) won't happen only if ( prop_2 )\nSTL: ( ( negation prop_1 ) imply prop_2 )\n\nnatural language: only under the case of ( prop_2 ), will ( prop_1 ) not happen\nSTL: ( ( negation prop_1 ) imply prop_2 )\n\nnatural language: ( prop_1 ) always follows with ( prop_2 ).\nSTL: ( globally ( prop_1 imply ( finally prop_2 ) ) )\n\nnatural language: Maintain ( prop_1 ) until ( prop_2 ) is satisfied.\nSTL: globally ( prop_1 until prop_2 )\n\nnatural language: Go to ( prop_1 ) and always avoid both ( prop_2 ) and ( prop_3 ).\nSTL: ( ( finally prop_1 ) and globally ( ( negation prop_2 ) and ( negation prop_3 ) ) )\n\nnatural language: If ( prop_1 ) happens before ( prop_3 ) then start ( prop_2 ) and cancel ( prop_4 ) anytime within 0 to 10 timesteps.\nSTL: globally ( ( prop_1 and ( finally prop_3 ) ) imply ( prop_2 and ( finally [0,10] ( negation prop_4 ) ) ) )\n\nnatural language: For time steps between 0 and 20, until (prop_1) and (prop_2) is true, don’t start ( prop_3 ).\nSTL: ( globally [0,20] ( ( negation prop_3 ) until ( prop_1 and prop_2 ) ) )\n\nnatural language: If prop_1 and prop_2 and not prop_3 or prop_4, then prop_5 happens after 10 timesteps.\nSTL: ( ( prop_1 and prop_2 ) and ( negation ( prop_3 or prop_4 ) ) ) imply ( finally [10,infinite] prop_5 )\n\nnatural language: prop_1 for the first 5 timesteps then prop_2 thereafter.\nSTL: ( ( globally [0,5] prop_1 ) and ( globally [5,infinite] prop_2 ) )\n\nnatural language: prop_1 and prop_2 and prop_3 and prop_4 and prop_5\nSTL: ( ( ( ( prop_1 and prop_2 ) and prop_3 ) and prop_4 ) and prop_5 )\n\nnatural language: prop_1 and prop_2 and prop_3\nSTL: ( ( prop_1 and prop_2 ) and prop_3 )\n\nnatural language: "

  if model_name_NL2TL == 'gpt-4':
    openai.api_key = openai_api_key_name
    result = openai.ChatCompletion.create(
      model=model_name_NL2TL,
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": NL2TL_prompt + lifted_NL + '\nSTL: '}
        ]
    )
    return result.choices[0]['message']['content']
  elif model_name_NL2TL == 'gpt-3':
    openai.api_key = openai_api_key_name
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=NL2TL_prompt + lifted_NL + '\nSTL: ',
      temperature=0.0,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response['choices'][0]['text'][1:]

def GPT_NL2TL_preorder(lifted_NL, model_name_NL2TL = 'gpt-4'):
  NL2TL_prompt="Try to transform the following natural languages into signal temporal logics, the operators in the signal temporal logic are: negation, imply, and, equal, until, globally, finally, or .\nThe signal temporal logics are prefix expressions. The examples are as following:\nnatural language: If ( prop_3 ) then implies ( prop_4 ), this condition should continue to happen until at some point within the next 450 to 942 time units , after that ( prop_2 ) , or ( prop_1 ) .\nSTL:  ['or', 'until [450,942]', 'imply', 'prop_3', 'prop_4', 'prop_2', 'prop_1']\n\nnatural language: The time that ( prop_3 ) happens is when ( prop_1 ) happens , and vice versa .\nSTL:  ['equal', 'prop_3', 'prop_1']\n\nnatural language: ( prop_1 ) or ( prop_2 ) happens and continues until at some point during the 142 to 365 time units ( prop_4 ) happens and ( prop_3 ) happens at the same time .\nSTL:  ['until [142,365]', 'or', 'prop_1', 'prop_2', 'and', 'prop_4', 'prop_3']\n\nnatural language: ( prop_1 ) should not happen and ( prop_2 ) should happen at the same time , and the above scenario is equivalent to the case that at some point during the 230 to 280 time units ( prop_3 ) happens .\nSTL:  ['equal', 'and', 'negation', 'prop_1', 'prop_2', 'finally [230,280]', 'prop_3']\n\nnatural language: In the following 10 time steps , the ( prop_1 ) should always happen , and in the meantime , ( prop_2 ) should happen at least once .\nSTL:  ['and', 'globally [0,10]', 'prop_1', 'finally', 'prop_2']\n\nnatural language: ( prop_1 ) should not happen if ( prop_2 ) does not happen , and ( prop_3 ) should also be true all the time .\nSTL:  ['and', 'imply', 'negation', 'prop_2', 'negation', 'prop_1', 'globally', 'prop_3']\n\nnatural language: If ( prop_1 ) and ( prop_2 ), then ( prop_3 ) until ( prop_4 ) does not happen , and ( prop_5 ) until ( prop_6 ) does not happen .\nSTL:  ['and', 'imply', 'and', 'prop_1', 'prop_2', 'until', 'prop_3', 'negation', 'prop_4', 'until', 'prop_5', 'negation', 'prop_6']\n\nnatural language: For each time instant in the next 0 to 120 units, do ( prop_1 ) if ( prop_2 ) , and if possible, ( prop_4 ) .\nSTL:  ['and', 'globally [0,120]', 'imply', 'prop_2', 'prop_1', 'prop_4']\n\nnatural language: In the next 0 to 5 time units , do the ( prop_1 ) , but in the next 3 to 4 time units , ( prop_2 ) should not happen .\nSTL:  ['and', 'globally [0,5]', 'prop_1', 'globally [3,4]', 'negation', 'prop_2']\n\nnatural language: While (prop_1) , do (prop_2) , and when (prop_3) , stop (prop_2) .\nSTL: ['and', 'imply', 'prop_1', 'prop_2', 'imply', 'prop_3', 'negation', 'prop_2']\n\nnatural language: If (prop_1) happens, then some time after the next 300 time steps (prop_2) should happen.\nSTL:  ['imply', 'prop_1', 'finally [300, infinite]', 'prop_2']\n\nnatural language: If (prop_1) happens, then for all time afterward (prop_2) holds and if, in addition, if (prop_3) occurs, then (prop_4) eventually occurs in the next 10 time units.\nSTL:  ['imply', 'prop_1', 'and', 'globally', 'prop_2', 'imply', 'prop_3', 'finally [0, 10]', 'prop_4']\n\nnatural language: If (prop_1), don't (prop_2), instead keep (prop_3) until (prop_4).\nSTL: ['imply', 'prop_1', 'and', 'negation', 'prop_2', 'until', 'prop_3', 'prop_4']\n\nnatural language: If (prop_4), then make sure any of the following happens: (prop_1), (prop_2) or (prop_3).\nSTL:  ['imply', 'prop_4', 'or', 'or', 'prop_1', 'prop_2', 'prop_3']\n\nnatural language: Always make (prop_1) happen in the next 999 time units if (prop_2) in the next 500 time instants.\nSTL:  ['imply', 'finally [0, 500]', 'prop_2', 'finally [0, 999]', 'prop_1']\n\nnatural language: If (prop_1) happens, then keep (prop_2) to be true until (prop_3) in the next 300 time units, otherwise, if (prop_4) then (prop_2) and if (prop_5) then (prop_6).\nSTL:  ['imply', 'prop_1', 'or', 'until [0, 300]', 'prop_2', 'prop_3', 'and', 'imply', 'prop_4', 'prop_2', 'imply', 'prop_5', 'prop_6']\n\nnatural language: Stay (prop_1) for 354 timesteps, and if (prop_2) happens, then first keep (prop_3) and then let (prop_4) happen at some point during 521 to 996 time steps.\nSTL: ['and', 'globally [0, 354]', 'prop_1', 'imply', 'prop_2', 'and', 'globally [0, 521]', 'prop_3', 'finally [521, 996]', 'prop_4']\n\nnatural language: Manage to achieve (prop_1) in the next 1000 time steps, and if (prop_2) happens in this process, keep (prop_3) until (prop_4) for 500 time units.\nSTL: ['and', 'finally [0, 1000]', 'prop_1', 'imply', 'prop_2', 'until [0, 500]', 'prop_3', 'prop_4']\n\nnatural language: As long as (prop_1), make sure to maintain (prop_2) .\nSTL:  ['imply', 'prop_1', 'prop_2']\n\nnatural language: Do (prop_1) until (prop_3), but once (prop_4) occurs then immediately (prop_2) .\nSTL:  ['and', 'until', 'prop_3', 'prop_1', 'imply', 'prop_4', 'prop_2']\n\nnatural language: If you do (prop_1) and observe (prop_2), then you should not do (prop_3) .\nSTL:  ['imply', 'and', 'prop_1', 'prop_2', 'negation', 'prop_3']\n\nnatural language: The time that ( prop_3 ) happens is when ( prop_1 ) happens , and vice versa .\nSTL: ['equal', 'prop_1', 'prop_2']\n\nnatural language: It is required that both ( prop_2 ) and ( prop_4 ) happen at the same time, or else ( prop_3 ) happens and continues until ( prop_1 ) happens.\nSTL:  ['or', 'and', 'prop_2', 'prop_4', 'until', 'prop_3', 'prop_1']\n\nnatural language: ( prop_3 ) happens and continues until at some point during the 500 to 903 time units ( prop_1 ) happens , and in the same time ( prop_2 ) does not happen .\nSTL:  ['and', 'until [500,903]', 'prop_3', 'prop_1', 'negation', 'prop_2']\n\nnatural language: For each time instant in the next 107 to 513 time units ( prop_1 ) is true , or else ( prop_3 ) happens and ( prop_2 ) happens at the same time.\nSTL: ['or', 'globally [107, 513]', 'prop_1', 'and', 'prop_3', 'prop_2']\n\nnatural language: ( prop_1 ) or ( prop_2 ) happens and continues until at some point during the 142 to 365 time units ( prop_4 ) happens and ( prop_3 ) happens at the same time .\nSTL:  ['until [142,365]', 'or', 'prop_1', 'prop_2', 'and', 'prop_4', 'prop_3']\n\nnatural language: It is always the case that everytime when ( prop_1 ) and ( prop_2 ) then all of the following conditions hold : for each time point during the subsequent 4 to 47 time units ( prop_3 ) .\nSTL:  ['imply', 'and', 'prop_1', 'prop_2', 'globally [4,47]', 'prop_3']\n\nnatural language: at some time ( prop_1 ) and when possible ( prop_2 )\nSTL:  ['and', 'prop_1', 'finally', 'prop_2']\n\nnatural language: at some time ( prop_1 ) and never ( prop_2 )\nSTL:  ['and', 'finally', 'prop_1', 'globally', 'negation', 'prop_2']\n\nnatural language: when possible ( prop_1 ) and at some time ( prop_2 )\nSTL:  ['finally', 'and', 'prop_1', 'finally', 'prop_2']\n\nnatural language: never ( prop_1 ) or whenever ( prop_2 )\nSTL:  ['or', 'globally', 'negation', 'prop_1', 'finally', 'prop_2']\n\nnatural language: when possible ( prop_1 ) and don't ( prop_2 )\nSTL:  ['finally', 'and', 'prop_1', 'negation', 'prop_2']\n\nnatural language: ( prop_1 ) or at any time ( prop_2 )\nSTL:  ['or', 'prop_1', 'finally', 'prop_2']\n\nnatural language: Globally , if ( prop_1 ) then the following condition is true : at the same time the event that ( prop_2 ) ought to be detected and ( prop_3 ) .\nSTL:  ['globally', 'imply', 'prop_1', 'and', 'prop_2', 'prop_3']\n\nnatural language: at some time ( prop_1 ) or ( prop_2 )\nSTL:  ['finally', 'or', 'prop_1', 'prop_2']\n\nnatural language: ( prop_1 ) and at some time ( prop_2 )\nSTL:  ['and', 'prop_1', 'finally', 'prop_2']\n\nnatural language: whenever ( prop_1 ) and at any time ( prop_2 )\nSTL:  ['and', 'finally', 'prop_1', 'finally', 'prop_2']\n\nnatural language: whenever ( prop_1 ) or forever ( prop_2 )\nSTL: ['or', 'finally', 'prop_1', 'globally', 'prop_2']\n\nnatural language: At the random time between 0 to 30 (prop_1) for 5 seconds, and at the random time between 0 to 30 (prop_2) for 5 seconds, and at the random time between 0 to 30 (prop_3) for 5 seconds.\nSTL:  ['and', 'and', 'finally [0,30]', 'globally [0,5]', 'prop_1', 'finally [0,30]', 'globally [0,5]', 'prop_2', 'finally [0,30]', 'globally [0,5]', 'prop_3']\n\nnatural language: At sometime between 1 to 25 stay at prop_1 for five seconds and always stay away from the prop_2 and prop_3 during 0 to 30 seconds.\nSTL:  ['and', 'finally [1,25]', 'globally [0,5]', 'prop_1', 'globally [0,30]', 'and', 'negation', 'prop_2', 'negation', 'prop_3']\n\nnatural language: Always (prop_1) if not (prop_2).\nSTL:  ['imply', 'negation', 'prop_2', 'globally', 'prop_1']\n\nnatural language: Always (prop_1) only if not (prop_2).\nSTL:  ['imply', 'globally', 'prop_1', 'negation', 'prop_2']\n\nnatural language: Avoid (prop_1) until (prop_2) lasts for 20 steps.\nSTL:  ['until', 'negation', 'prop_1', 'globally [0, 20]', 'prop_2']\n\nnatural language: Wait till (prop_1) is complete, then, (prop_2) for next 20 units.\nSTL:  ['imply', 'finally', 'prop_1', 'globally [0, 20]', 'prop_2']\n\nnatural language: ( prop_1 ) won't happen only if ( prop_2 )\nSTL:  ['imply', 'negation', 'prop_1', 'prop_2']\n\nnatural language: only under the case of ( prop_2 ), will ( prop_1 ) not happen\nSTL:  ['imply', 'negation', 'prop_1', 'prop_2']\n\nnatural language: ( prop_1 ) always follows with ( prop_2 ).\nSTL:  ['globally', 'imply', 'prop_1', 'finally', 'prop_2']\n\nnatural language: Maintain ( prop_1 ) until ( prop_2 ) is satisfied.\nSTL:  ['globally', 'until', 'prop_1', 'prop_2']\n\nnatural language: Go to ( prop_1 ) and always avoid both ( prop_2 ) and ( prop_3 ).\nSTL:  ['and', 'finally', 'prop_1', 'globally', 'and', 'negation', 'prop_2', 'negation', 'prop_3']\n\nnatural language: If ( prop_1 ) happens before ( prop_3 ) then start ( prop_2 ) and cancel ( prop_4 ) anytime within 0 to 10 timesteps.\nSTL:  ['globally', 'imply', 'and', 'prop_1', 'finally', 'prop_3', 'and', 'prop_2', 'finally', 'negation', 'prop_4']\n\nnatural language: For time steps between 0 and 20, until (prop_1) and (prop_2) is true, don’t start ( prop_3 ).\nSTL:  ['globally [0,20]', 'until', 'negation', 'prop_3', 'and', 'prop_1', 'prop_2']\n\nnatural language: If prop_1 and prop_2 and not prop_3 or prop_4, then prop_5 happens after 10 timesteps.\nSTL:  ['imply', 'and', 'and', 'prop_1', 'prop_2', 'negation', 'or', 'prop_3', 'prop_4', 'finally [10,infinite]', 'prop_5']\n\nnatural language: prop_1 for the first 5 timesteps then prop_2 thereafter.\nSTL:  ['and', 'globally [0,5]', 'prop_1', 'globally [5,infinite]', 'prop_2']\n\nnatural language: prop_1 and prop_2 and prop_3 and prop_4 and prop_5\nSTL:  ['and', 'and', 'and', 'and', 'prop_1', 'prop_2', 'prop_3', 'prop_4', 'prop_5']\n\nnatural language: prop_1, then prop_2 and stay there for 5 seconds, remember always prop_3.\nSTL: ['and',  'finally', 'prop_1', 'and', 'finally', 'globally [0,5]', 'prop_2', 'globally', 'prop_3']\n\nnatural language: "

  if model_name_NL2TL == 'gpt-4':
    openai.api_key = openai_api_key_name
    try:
      result = openai.ChatCompletion.create(
        model=model_name_NL2TL,
        messages=[
              {"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": NL2TL_prompt + lifted_NL + '\nSTL: '}
          ]
      )
    except:
      result = openai.ChatCompletion.create(
        model=model_name_NL2TL,
        messages=[
              {"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": NL2TL_prompt + lifted_NL + '\nSTL: '}
          ]
      )
    return result.choices[0]['message']['content']
  elif model_name_NL2TL == 'gpt-3':
    openai.api_key = openai_api_key_name
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=NL2TL_prompt + lifted_NL + '\nSTL: ',
      temperature=0.0,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response['choices'][0]['text'][1:]

def parse_string(input_string):
  # Split the string into sentence and properties part
  parts = re.split('\s*:\s*', input_string, 1)

  try:
    # Get the sentence part
    sentence = parts[1].split('.', 1)[0].strip() + '.'

    # Get the properties part
    properties = parts[1].split('.', 1)[1].strip()
  except:
    # Get the sentence part
    sentence = parts[1].split('\n')[0].strip()

    # Get the properties part
    properties = parts[1].split('\n')[1].strip()

  # Remove white spaces and split properties by ';'
  property_list = re.split('\s*;\s*', properties)

  # Remove the last empty element if it exists
  if property_list[-1] == '':
    property_list = property_list[:-1]

  # Prepare property dictionary
  prop_dict = {}
  for prop in property_list:
    # Split property by ':'
    key_value = re.split('\s*:\s*', prop)

    # Remove the first and the last characters (which are quotes) from the key
    key = key_value[0][1:-1]

    # Remove the first and the last characters (which are brackets and quotes) from the values
    # and split the values by ',' but considering 'finally [0,10]' as a single entity
    values = re.findall(r"'[^']*'|\"[^\"]*\"", key_value[1])
    values = [v[1:-1] for v in values]

    # Assign values to corresponding key in the dictionary
    prop_dict[key] = values

  return sentence, prop_dict


def AP_dict_func(AP_specify):
  AP_dict = {}
  for item in AP_specify:
    action_list = item.split(' : ')[1][1:-1].split(', ')
    if len(action_list) < 1:
      print('Error! action len in ' + item.split(' : ')[0] + ' is zero!')
    else:
      for index in range(len(action_list)):
        if index == 0:
          action_TL = action_list[index]
        else:
          action_TL = '( ' + action_TL + ' and ' + action_list[index] + ' )'

    AP_dict[item.split(' : ')[0]] = action_TL
  return AP_dict

def AP_dict_func_preorder(AP_specify):
  AP_dict = {}
  for item in AP_specify:
    item_process = item.split(' : ')
    if len(item_process) != 2:
      item_process = item.split(': ')
    action_list = item_process[1][1:-1].split(', ')
    action_list = [item[1:-1] for item in action_list]
    if len(action_list) < 1:
      print('Error! action len in ' + item.split(' : ')[0] + ' is zero!')
    else:
      if len(item_process) == 2:
        AP_dict[item.split(' : ')[0][1:-1]] = action_list
      else:
        AP_dict[item.split(': ')[0][1:-1]] = action_list
  return AP_dict

def is_unary_operator(token):
  return token in ('negation', 'globally', 'finally') or token.split(' ')[0] in ('globally', 'finally', 'negation')

def is_operator(token):
  return token in ('and', 'imply', 'equal', 'or', 'until', 'negation', 'globally', 'finally') \
         or token.split(' ')[0] in ('globally', 'finally', 'until')

def check_syntactic_correct(converted_list):
  count = 0
  for item in converted_list:
    if is_operator(item):
      if is_unary_operator(item):
        pass
      else:
        count -= 1
    elif item[:4] == 'prop' or item[:5] == 'enter' or item[:4] == 'not_':
      count += 1
    else:
      return item
  if count == 1:
    return 'correct'
  else:
    return count

def check_syntactic_correct_inverse_order(converted_list_input):
  converted_list = copy.deepcopy(converted_list_input)
  converted_list.reverse()
  count = 0
  for item in converted_list:
    if is_operator(item):
      if is_unary_operator(item):
        pass
      else:
        count -= 1
        if count == 0:
          return 'error'
    elif item[:4] == 'prop' or item[:5] == 'enter' or item[:4] == 'not_':
      count += 1
      if count == 0:
        return 'error'
    else:
      return 'error'
  if count == 1:
    return 'correct'
  else:
    return 'error'

def AP_dict_syntactic_correct_check(AP_dict):
  for prop_tag, prop_list in AP_dict.items():
    if check_syntactic_correct(prop_list) != 'correct':
      return False
  return True

def func_syntactic_correct_loop(model_name, user_prompt_1, AP_and_lifted_NL):
  lifted_NL, AP_dict = parse_string(AP_and_lifted_NL)
  for i in range(5):
    if AP_dict_syntactic_correct_check(AP_dict) == False:
      print('\nSyntactic loop' + str(i + 1) + ':\n')
      if model_name == 'gpt-3':
        user_prompt_syntactic_correct = user_prompt_1 + '\nGPT-3 response:\n' + AP_and_lifted_NL + '\nHuman feedback: '
        for prop_tag, prop_list in AP_dict.items():
          if check_syntactic_correct(prop_list) != 'correct' and type(check_syntactic_correct(prop_list)) == int:
            if check_syntactic_correct(prop_list) > 1:
              user_prompt_syntactic_correct += 'Your predicted ' + prop_tag + ' lacks ' + str(check_syntactic_correct(prop_list) - 1) + ' operators with two leaves, the correct syntactic format should be like '\
              + str(['and']*(check_syntactic_correct(prop_list) - 1) + prop_list) + '. '
            elif check_syntactic_correct(prop_list) < 1:
              user_prompt_syntactic_correct += 'Your predicted ' + prop_tag + ' has ' + str(1 - check_syntactic_correct(prop_list)) + ' more operators with two leaves, the correct syntactic format should be like '\
              + str(prop_list[abs(check_syntactic_correct(prop_list)-1):]) + '. '

        user_prompt_syntactic_correct += 'Please correct your answer with the same format as the previous output.\nOutput: '
        AP_and_lifted_NL = GPT_response_GPT_3(user_prompt_syntactic_correct)
        lifted_NL, AP_dict = parse_string(AP_and_lifted_NL)

        for prop_tag, prop_list in AP_dict.items():
          print(prop_tag + ': ' + str(prop_list))
      elif model_name == 'gpt-4':
        assistent_feed = copy.deepcopy(AP_and_lifted_NL)
        user_prompt_2 = ''
        for prop_tag, prop_list in AP_dict.items():
          if check_syntactic_correct(prop_list) != 'correct' and type(check_syntactic_correct(prop_list)) == int:
            if check_syntactic_correct(prop_list) > 1:
              user_prompt_2 += 'Your predicted ' + prop_tag + ' lacks ' + str(check_syntactic_correct(prop_list) - 1) + ' operators with two leaves, the correct syntactic format should be like '\
              + str(['and']*(check_syntactic_correct(prop_list) - 1) + prop_list) + '. '
            elif check_syntactic_correct(prop_list) < 1:
              user_prompt_2 += 'Your predicted ' + prop_tag + ' has ' + str(1 - check_syntactic_correct(prop_list)) + ' more operators with two leaves, the correct syntactic format should be like '\
              + str(prop_list[abs(check_syntactic_correct(prop_list)-1):]) + '. '

        user_prompt_2 += 'Please correct your answer.\nOutput: '
        AP_and_lifted_NL = GPT_response_second_round(user_prompt_1, assistent_feed, user_prompt_2)
        lifted_NL, AP_dict = parse_string(AP_and_lifted_NL)

        for prop_tag, prop_list in AP_dict.items():
          print(prop_tag + ': ' + str(prop_list))
    else:
      return AP_and_lifted_NL, i+1
  return AP_and_lifted_NL, i+1

def trajectory_len_cal(PWLs):
  trajectory_len = 0
  for i in range(len(PWLs)):
      PWL = PWLs[i]
      position_list = [[P[0][0], P[0][1]] for P in PWL]
      for i in range(len(position_list)-1):
        trajectory_len += np.sqrt((position_list[i][0]-position_list[i+1][0])**2 + (position_list[i][1]-position_list[i+1][1])**2)

  return trajectory_len


def state_check(PWL_x_y_t, tag_and_shape):
  for color, block_array in tag_and_shape.items():
    B_item = []
    for block_item_list in block_array:
      block_item = block_item_list[:-1]
      block_item_func_str = block_item_list[-1]
      if PWL_x_y_t[0] > -block_item[0] and PWL_x_y_t[0] < block_item[1] and PWL_x_y_t[1] > -block_item[2] and PWL_x_y_t[
        1] < block_item[3]:
        return color, block_item_func_str, block_item
  return 'white', 'road', None


def interpolate_list(data, divide_path_time_ratio):
  # Ensure divide_path_time_ratio is a power of 2
  if (divide_path_time_ratio & (divide_path_time_ratio - 1)) != 0 or divide_path_time_ratio == 0:
    raise ValueError("divide_path_time_ratio must be a power of 2.")

  # Copy the original data
  new_data = list(data)

  # Loop for log2(divide_path_time_ratio) times
  for _ in range(int(math.log2(divide_path_time_ratio))):
    # Temporary list to store new data
    temp_data = []
    for i in range(len(new_data) - 1):
      # Calculate mid-point and add it to the temporary list
      mid_point = [(new_data[i][j] + new_data[i + 1][j]) / 2 for j in range(len(new_data[i]))]
      temp_data.append(new_data[i])
      temp_data.append(mid_point)
    temp_data.append(new_data[-1])
    # Update new_data
    new_data = list(temp_data)
  return new_data


def judge_trajectory_output_state(tag_and_shape, PWL, divide_path_time_ratio=1):
  state_time_list = []
  if len(PWL) > 3:
    PWL_new = interpolate_list(PWL, divide_path_time_ratio)
    for item in PWL_new:
      color, block_item_func_str, block_item = state_check(item, tag_and_shape)
      if block_item is not None:
        state_time_list.append([color, block_item_func_str, str(item[-1])])
      else:
        state_time_list.append(['white', 'road', str(item[-1])])
        # pass
  elif len(PWL) == 3:
    print('The STL is semantically impractical to plan out a trajectory.')
    pass
  #except:
  #  print('The STL is syntactically impractical to plan out a trajectory.')
  return state_time_list


def abbreviate_list_state_check(lst):
  result = []
  temp_group = []

  for i in range(len(lst)):
    if temp_group and (lst[i][:2] != temp_group[0][:2]):
      # Append the first and last element of the temp_group to the result list, if they're different
      if temp_group[0] != temp_group[-1]:
        result.append(temp_group[0])
        result.append(temp_group[-1])
      else:
        result.append(temp_group[0])
      # Clear the temp_group
      temp_group = []
    # Append the current element to the temp_group
    temp_group.append(lst[i])

  # Append the first and last element of the last group, if they're different
  if temp_group:
    if temp_group[0] != temp_group[-1]:
      result.append(temp_group[0])
      result.append(temp_group[-1])
    else:
      result.append(temp_group[0])

  return result


def extract_list_for_semantic_check_LLM_response(s):
  match = re.search(r'STL:\s*\[(.*?)\]', s)
  if match:
    # Splitting the matched group by comma and stripping leading/trailing whitespaces
    extracted_list = [item.strip().strip("'") for item in match.group(1).split(',')]
    return extracted_list
  else:
    return []

def filter_negation_imply(input_stl_original):
  input_stl = copy.deepcopy(input_stl_original)
  # filter imply operation
  for index_negation in range(len(input_stl) - 1, -1, -1):
    if input_stl[index_negation] == 'imply':
      input_stl.pop(index_negation)
      input_stl.insert(index_negation, 'or')
      input_stl.insert(index_negation + 1, 'negation')
  # filter negation operation
  for index_negation in range(len(input_stl) - 1, -1, -1):
    if input_stl[index_negation] == 'negation' and input_stl[index_negation + 1][:5] == 'enter':
      phi = 'not_' + input_stl[index_negation + 1]
      input_stl.pop(index_negation + 1)
      input_stl.pop(index_negation)
      input_stl.insert(index_negation, phi)
    elif input_stl[index_negation] == 'negation' and input_stl[index_negation + 1][:9] == 'not_enter':
      phi = input_stl[index_negation + 1][4:]
      input_stl.pop(index_negation + 1)
      input_stl.pop(index_negation)
      input_stl.insert(index_negation, phi)

  if 'negation' in input_stl:
    for index_negation in range(len(input_stl) - 2):
      if input_stl[index_negation] == 'negation' and (
              input_stl[index_negation + 1] == 'and' or input_stl[index_negation + 1] == 'or'):
        count_operator = 0
        for operator_index in range(index_negation, len(input_stl)):
          if input_stl[operator_index] == 'and':
            input_stl[operator_index] = 'or'
            count_operator += 1
          elif input_stl[operator_index] == 'or':
            input_stl[operator_index] = 'and'
            count_operator += 1
          elif input_stl[operator_index][:5] == 'enter':
            phi = 'not_' + input_stl[operator_index]
            input_stl[operator_index] = phi
            count_operator -= 1
            if count_operator == -1:
              break
          elif input_stl[operator_index][:9] == 'not_enter':
            phi = input_stl[operator_index][4:]
            input_stl[operator_index] = phi
            count_operator -= 1
            if count_operator == -1:
              break
        input_stl.pop(index_negation)
  return input_stl