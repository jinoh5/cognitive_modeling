# -*- coding: utf-8 -*-
"""creating_dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eLUvC2IskqTrL4RHab8OXjzi6UTge_1v
"""

import numpy as np
import pandas as pd

def create_input_format(dataset):

  mouse_choices = np.zeros(len(dataset))
  mouse_rewards = np.zeros(len(dataset))
  mouse_reward_probabilities = np.zeros((len(dataset),2))
  mouse_ntrials = len(mouse_choices)
  mouse_session_index = []

# choices
  for i in range(len(dataset)):
    if dataset[i][4] == "l":
      mouse_choices[i]=0
    elif dataset[i][4] == "r":
      mouse_choices[i]=1

# rewards
  for i in range(len(dataset)):
    mouse_rewards[i] += dataset[i][1]

# reward probabilities
  for i in range(len(dataset)):
    mouse_reward_probabilities[i,0]=dataset[i,2]
    mouse_reward_probabilities[i,1]=dataset[i,3]

  mouse_choices = mouse_choices.astype(int)
  mouse_rewards = mouse_rewards.astype(int)

# session index
  for index in range(len(dataset)-1):
    if dataset[index][0] != dataset[index+1][0]:
      mouse_session_index.append(np.int(index))
  mouse_session_index = np.asarray(mouse_session_index)+1
  n_session = len(mouse_session_index)

  mouse_dataset = {
      'nTrials': mouse_ntrials,
      'nSession': n_session,
      'session_index': mouse_session_index,
      'choices': mouse_choices,
      'rewards': mouse_rewards 
  }

  return mouse_dataset, mouse_reward_probabilities