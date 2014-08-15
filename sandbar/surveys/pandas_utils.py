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


def round_series_values(element, decimal_places=2):
    try:
        result = round(element, decimal_places)
    except TypeError:
        result = element
    return result

def datetime_to_date(element):
    try:
        result = element.date()
    except AttributeError:
        result = element
    return result
        