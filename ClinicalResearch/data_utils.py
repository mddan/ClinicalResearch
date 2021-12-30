import re
import pandas as pd
from IPython.display import clear_output


def get_dx_cols(df):
    '''
    This function retrieves DX (diagnosis) column names from a given dataset
    '''
    cols_all = df.columns
    rdx = re.compile(".*DX\d")
    cols_dx = list(filter(rdx.match, cols_all))
    return cols_dx


def get_pr_cols(df):
    '''
    This function retrieves PR (procedure) column names from a given dataset
    '''
    cols_all = df.columns
    rpr = re.compile(".*PR\d")
    cols_pr = list(filter(rpr.match, cols_all))
    return cols_pr


def filter_chunk_by_dx(df, dx_icds):
    '''
    This function isolates rows from a df chunk based on the input of DX ICD codes provided to the function
    '''
    extract_list = []
    cols_dx = get_dx_cols(df)
    for i in cols_dx:
        extract = df.loc[df[i].isin(dx_icds)]
        extract_list.append(extract)
    extract_concat_dedup = pd.concat(extract_list).drop_duplicates()
    return extract_concat_dedup


def filter_chunk_by_pr(df, pr_icds):
    '''
    This function isolates rows from a df chunk based on the input of PR ICD codes provided to the function
    '''
    extract_list = []
    cols_pr = get_pr_cols(df)
    for i in cols_pr:
        extract = df.loc[df[i].isin(pr_icds)]
        extract_list.append(extract)
    extract_concat_dedup = pd.concat(extract_list).drop_duplicates()
    return extract_concat_dedup


def filter_NIS_year_by_dx(nis_df, dx_icds):
    '''
    This function isolates rows from a full year df based on the input of DX ICD codes provided to the function
    '''
    dfs = []  # holds data chunks
    for chunk in nis_df:
        chunk_filtered = filter_chunk_by_dx(chunk, dx_icds)
        dfs.append(chunk_filtered)
        clear_output(wait=True)
        print(f"Filtered {len(dfs)*100000} rows...")
        if len(dfs) == 3:
            break
    print(f"Finished filtering, now concatening all chunks...")
    data = pd.concat(dfs)
    print(f"Finished concatening!")
    return data


def filter_NIS_year_by_pr(nis_df, pr_icds):
    '''
    This function isolates rows from a full year df based on the input of PR ICD codes provided to the function
    '''
    dfs = []  # holds data chunks
    for chunk in nis_df:
        chunk_filtered = filter_chunk_by_pr(chunk, pr_icds)
        dfs.append(chunk_filtered)
        clear_output(wait=True)
        print(f"Filtered {len(dfs)*100000} rows...")


#        if len(dfs) == 3:
#            break
    print(f"Finished filtering, now concatening all chunks...")
    data = pd.concat(dfs)
    print(f"Finished concatening!")
    return data
