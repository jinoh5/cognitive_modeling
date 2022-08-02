import numpy as np
import pandas as pd

def show_bias_graph(fraction):
    mouse_name = ['AL038','AL039','AL040','AL041', 'AL042', 'AL049','AL050','AL053','AL054','AL055','AL056','AL058','AL059', 'mean']
    column = ['Choice Bias']
    bias_df = pd.DataFrame(fraction, mouse_name, column)
    bias_df_new = pd.melt(bias_df, id_vars =[], value_vars = bias_df.columns, ignore_index=False)
    bias_df_new.reset_index(level=0, inplace=True)
    bias_df_new.columns = ["Mouse ID", "Choice Bias", "Fraction of Choosing Right (%)"]
    bias_df_new['is_avg'] = bias_df_new['Mouse ID'] == 'mean'

    return bias_df_new

def show_mouse_agent_bias_graph(fraction_right):
    data_names = ['mouse', 'syn1', 'syn2','syn3','syn4','syn5']
    column = ['Bias']
    bias_df = pd.DataFrame(fraction_right, data_names, column)
    bias_df_new = pd.melt(bias_df, id_vars =[], value_vars = bias_df.columns, ignore_index=False)
    bias_df_new.reset_index(level=0, inplace=True)
    bias_df_new.columns = ["data_names", "Bias", "Fraction of Choosing Right (%)"]
    bias_df_new['is_mouse'] = bias_df_new['data_names'] == 'mouse'

    return bias_df_new