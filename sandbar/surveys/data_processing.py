import pandas as pd
from .pandas_utils import convert_to_float, sum_two_columns

def handle_sep_reatt_calc_area(dataframe, sr_ids, final_col_name):
    df0 = dataframe.applymap(convert_to_float) # initial dataframe with values converted to floats
    col_names = ['date']
    df_list = []
    for sr_id in sr_ids:
        df_sr_id = df0[df0['sr_id'] == sr_id]
        col_name = 'Sandbar ID: {0}'.format(sr_id)
        df_sr_id[col_name] = df0[final_col_name]
        df_list.append(df_sr_id)
        col_names.append(col_name)
    df_list_len = len(df_list)
    if df_list_len == 1:        df_sr = df_list[0]
    elif df_list_len == 2:
        df_sr = pd.merge(df_list[0], df_list[1], how='outer', on='date')
    else:
        raise Exception('I do not think a sandbar bar can have more than two separation/reattachments')
    sr_sum_name = 'SR {0} Total'.format(final_col_name)
    col_names.append(sr_sum_name)
    if df_list_len == 1:
        df_sr[sr_sum_name] = df_sr[final_col_name]
    elif df_list_len > 1:
        final_col_name_x = '{name}_{suffix}'.format(name=final_col_name, suffix='x')
        final_col_name_y = '{name}_{suffix}'.format(name=final_col_name, suffix='y')
        df_sr[sr_sum_name] = df_sr.apply(sum_two_columns, axis=1, col_x=final_col_name_x, col_y=final_col_name_y)
    else:
        raise Exception ("I don't know what's going on...")
    df_final = df_sr[col_names]
    return df_final

"""
def handle_sep_reatt_calc_volume(dataframe, sr_ids, final_col_name):
    df0 = dataframe.applymap(convert_to_float)
    col_names = ['date']
    df_list = []
    for sr_id in sr_ids:
        df_sr = df0[] 
""" 