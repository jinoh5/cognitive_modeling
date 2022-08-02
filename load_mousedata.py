# -*- coding: utf-8 -*-
"""mousedata_loading.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K0uFqYFAfLpqeKFK79S9B8WeGTdCW09W
"""

import pandas as pd
import numpy as np

def load_mousedata(str):
  mouse = pd.read_csv(str)
  mousedata = mouse.to_numpy()
  mouse_session_index = []
  even_data = np.zeros((0,5))
  odd_data = np.zeros((0,5))

  # session index
  for index in range(len(mousedata)-1):
    if mousedata[index][0] != mousedata[index+1][0]:
      mouse_session_index.append(np.int(index))
  mouse_session_index = np.asarray(mouse_session_index)+1
  session_num_list = range(len(mouse_session_index))
  n_session = len(mouse_session_index)
  # print(n_session)
  # print(mouse_session_index)

  # divide up the data according to the mouse_session_index
  for index in range(n_session):
    if index == 0: #very first index 
      even_data = np.vstack((even_data, mousedata[:mouse_session_index[session_num_list[index]]]))
    elif (index % 2 != 0):
      odd_data = np.vstack((odd_data, mousedata[mouse_session_index[session_num_list[index-1]]:mouse_session_index[session_num_list[index]]]))
      if index == session_num_list[-1]: #just for the very last index 
        odd_data = np.vstack((odd_data, mousedata[mouse_session_index[session_num_list[index]]:]))
    elif (index % 2 == 0):
      even_data = np.vstack((even_data, mousedata[mouse_session_index[session_num_list[index-1]]:mouse_session_index[session_num_list[index]]]))
      if index == session_num_list[-1]: #just for the very last index
        even_data = np.vstack((even_data, mousedata[mouse_session_index[session_num_list[index]]:]))

  return mousedata, even_data, odd_data