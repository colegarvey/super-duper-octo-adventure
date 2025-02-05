import pandas as pd
import numpy as np
from scipy import stats


def prep_passing_td(prep_df):
    # Subset necessary columns
    df = prep_df.loc[:,['Wk','Comp','Att_P','Yds_P','Avg_P','TD_P','Rate']]

    # Compute completion percentage
    df['Cmp_rate'] = df['Comp'] / df['Att_P']
    df = df.drop(columns=['Comp','Att_P'])

    # Normalize df since columns have differing units of measure
    df = df.apply(stats.zscore)

    # Drop the column we want to predict
    out = df['TD_P']
    df = df.drop(columns=['TD_P'])

    return (df, out)