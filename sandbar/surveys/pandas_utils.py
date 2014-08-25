import numpy as np
import pandas as pd


def create_pandas_dataframe(data, columns=None, create_psuedo_column=False):    
    try:
        df = pd.DataFrame(data, columns=columns)
    except ValueError:
        if create_psuedo_column:
            pseudo_data = tuple()
            columns_len = len(columns)
            while len(pseudo_data) < columns_len:
                pseudo_data += (None,)
            df = pd.DataFrame([pseudo_data], columns=columns)
        else:
            df = pd.DataFrame([])        
    return df


# function is deprecated
def replace_none_with_nan(query_results):
    cleaned = []
    for query_result in query_results:
        date_obj, measurement = query_result
        if measurement is None:
            clean_tuple = (date_obj, np.nan)
        else:
            clean_tuple = (date_obj, measurement)
        cleaned.append(clean_tuple)
    return cleaned


def replace_df_none(element, replacement=np.nan):
    if element is None:
        new_element = replacement
    else:
        new_element = element
    return new_element


def round_series_values(element, decimal_places=2):
    """
    For element in a dataframe, try to round the value
    to two decimal places; will return the element value
    otherwise.
    """
    try:
        result = round(element, decimal_places)
    except TypeError:
        result = element
    return result


def datetime_to_date(element):
    """
    For each element in a dataframe, try to return
    a date; will return the element value otherwise.
    """
    try:
        result = element.date()
    except AttributeError:
        result = element
    return result


def convert_to_str(element):
    try:
        if np.isnan(element) or element is None:
            return_str = ''
        else:
            return_str = str(element)
    except TypeError:
        return_str = element
    return return_str


def convert_to_float(element):
    try:
        float_val = float(element)
    except(TypeError, ValueError):
        float_val = element
    return float_val


def replace_nat(element, replacement=np.nan):
    if element == pd.NaT:
        new_element = replacement
    else:
        new_element = element
    return new_element


def col_difference(series, col_x, col_y):
    x_val = series[col_x]
    y_val = series[col_y]
    is_x_float = isinstance(x_val, float)
    is_y_float = isinstance(y_val, float)
    try:
        if is_x_float is True and is_y_float is True:
            x = x_val
            y = y_val
        elif is_x_float is True and is_y_float is False:
            x = x_val
            y = 0
        elif is_x_float is False and is_y_float is True:
            x = 0
            y = y_val
        else:
            x = np.nan
            y = np.nan
        col_diff = np.nansum([x, y*(-1)])
    except TypeError:
        col_diff = np.nan
    return col_diff


def sum_two_columns(series, col_x, col_y):
    x_val = series[col_x]
    y_val = series[col_y]
    is_x_float = isinstance(x_val, float)
    is_y_float = isinstance(y_val, float)
    try:
        if is_x_float is True and is_y_float is True:
            x = x_val
            y = y_val
        elif is_x_float is True and is_y_float is False:
            x = x_val
            y = 0
        elif is_x_float is False and is_y_float is True:
            x = 0
            y = y_val
        else:
            x = np.nan
            y = np.nan
        sum_result = np.nansum([x, y])
    except TypeError:
        sum_result = np.nan
    return sum_result


def check_for_nans_and_none(values):
    nans = []
    for value in values:
        if pd.isnull(value):
            nans.append(True)
        else:
            nans.append(False)
    if any(nan for nan in nans):
        nans_exist = True
    else:
        nans_exist= False
    return nans_exist
        

def create_dygraphs_error_str(series, low, med, high):
    low_val = series[low]
    med_val = series[med]
    high_val = series[high]
    value_list = [low_val, med_val, high_val]
    nans_exist = check_for_nans_and_none(value_list)
    if nans_exist:
        err_str = None
    else:
        err_str = '{low};{med};{high}'.format(low=low_val, med=med_val, high=high_val)
    return err_str


def create_df_error_bars(data, final_col_name, columns=('date', 'val_low', 'val_med', 'val_high')):
    df = create_pandas_dataframe(data, columns, create_psuedo_column=True)
    df[final_col_name] = df.apply(create_dygraphs_error_str, axis=1, low='val_low', med='val_med', high='val_high')
    df_clean = df[['date', final_col_name]]
    df_final = df_clean[pd.notnull(df_clean['date'])]
    return df_final


def create_sep_reatt_name(sandbar_id):
    sr_name = 'Sandbar ID: {0}'.format(sandbar_id)
    return sr_name     