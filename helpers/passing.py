import pandas as pd
import numpy as np
from scipy import stats


def clean_nan(data):
    data = data.reset_index(drop=True)

    for col in data.columns[5:]:
        data[col].fillna(np.mean(data[col]), inplace=True)
            
    return data


# __________________________________________________________________________


def prep_passing_td(prep_df):
    # Subset necessary columns ,'TD_P','Wk','Comp','Att_P','Avg_P','Rate'
    df = prep_df.loc[:,['Comp','Att_P','Yds_P','Avg_P','TD_P','Ints']]

    # Compute completion percentage
    df['Cmp_rate'] = df['Comp'] / df['Att_P']
    df = df.drop(columns=['Comp','Att_P'])

    # Normalize df since columns have differing units of measure
    # df = df.apply(stats.zscore)

    # Drop the column we want to predict
    out = df['Yds_P']
    df = df.drop(columns=['Yds_P'])

    return (df, out)


# __________________________________________________________________________


def sample_stats(num, data):
    stats = []
    sample = data.sample(frac=(num/10))

    for col in sample.columns:
        curr = sample[col]
        if 0 <= num < 3:
            stats.append(np.mean(curr) - 2*np.std(curr))
        elif 3 <= num <= 5:
            stats.append(np.mean(curr) - np.std(curr))
        elif 5 < num <= 7:
            stats.append(np.mean(curr) + np.std(curr))
        elif 8 < num <= 10:
            stats.append(np.mean(curr) + 2*np.std(curr))    
        else:
            stats.append(np.mean(curr))

    return stats


# __________________________________________________________________________


def ohe_opp(data):
    """
    One-hot-encodes Opponent and whether the game was a Win or Loss.
    """
    # oh_enc = OneHotEncoder()
    # oh_enc.fit(data[['Roof Material']])
    # dummies = pd.DataFrame(oh_enc.transform(data[['Roof Material']]).todense(),
    #                        columns=oh_enc.get_feature_names_out(),
    #                        index = data.index)
    # return data.join(dummies)