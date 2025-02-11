import pandas as pd
import numpy as np
from scipy import stats


def clean_nan(data):
    data = data.reset_index(drop=True)

    for col in data.columns[5:]:
        data[col].fillna(np.mean(data[col]), inplace=True)
            
    return data


# __________________________________________________________________________


def prep_yds(data):
    # Subset necessary columns
    df = data.loc[:,['Comp','Att_P','Yds_P','Avg_P','TD_P','Ints']]

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


def prep_td(data):
    # Subset necessary columns
    df = data.loc[:,['Comp','Att_P','Avg_P','TD_P','Ints','Sck']]

    # Compute completion percentage
    # df['Cmp_rate'] = df['Comp'] / df['Att_P']
    # df = df.drop(columns=['Comp','Att_P'])

    # Drop the column we want to predict
    out = df['TD_P']
    df = df.drop(columns=['TD_P'])

    return (df, out)


# __________________________________________________________________________


# def prep_result(data):
#     # Subset necessary columns
#     df = data.loc[:,['Comp','Att_P','Avg_P','TD_P','Ints','Sck']]

#     # Compute completion percentage
#     # df['Cmp_rate'] = df['Comp'] / df['Att_P']
#     # df = df.drop(columns=['Comp','Att_P'])

#     # Drop the column we want to predict
#     out = df['TD_P']
#     df = df.drop(columns=['TD_P'])

#     return (df, out)

# __________________________________________________________________________


def sample_stats(data,state):
    stats = []
    sample = data.sample(frac=0.33, random_state=state)

    p = np.random.random()

    for col in sample.columns:
        curr = sample[col]

        if p < 0.5:
            stats.append(np.mean(curr) - np.std(curr))
        elif p < 1:
            stats.append(np.mean(curr) + np.std(curr))
        else:
            stats.append(np.mean(curr))

    return stats


# __________________________________________________________________________


# def ohe_opp(data):
#     """
#     One-hot-encodes Opponent and whether the game was a Win or Loss.
#     """
    # oh_enc = OneHotEncoder()
    # oh_enc.fit(data[['Roof Material']])
    # dummies = pd.DataFrame(oh_enc.transform(data[['Roof Material']]).todense(),
    #                        columns=oh_enc.get_feature_names_out(),
    #                        index = data.index)
    # return data.join(dummies)





# deg_results = []

# for degree in range(6):
#     poly_model = PolynomialFeatures(degree=degree)

#     X_train_poly = poly_model.fit_transform(X_train)
#     X_test_poly = poly_model.transform(X_test)

#     tst_model = LinearRegression()
#     tst_model.fit(X_train_poly, y_train)
    
#     # Compute model stats
#     y_hat = tst_model.predict(X_test_poly)
#     r_sq = r2_score(y_test, y_hat)
#     rmse = np.sqrt(mean_squared_error(y_test, y_hat))

#     deg_results.append((degree, r_sq, rmse))


# degrees, r2_scores, rmse_scores = zip(*deg_results)

# plt.figure(figsize=(10, 5))

# plt.subplot(1, 2, 1)
# plt.plot(degrees, r2_scores, marker='o')
# plt.xlabel('Polynomial Degree')
# plt.ylabel('R-squared')
# plt.title('R-squared vs. Polynomial Degree')

# plt.subplot(1, 2, 2)
# plt.plot(degrees, rmse_scores, marker='o', color='orange')
# plt.xlabel('Polynomial Degree')
# plt.ylabel('RMSE')
# plt.title('RMSE vs. Polynomial Degree')

# plt.tight_layout()
# plt.show()


# poly_model = PolynomialFeatures(degree=2)
# X_train_poly = poly_model.fit_transform(X_train)
# X_test_poly = poly_model.transform(X_test)

# pm1 = LinearRegression()
# pm1.fit(X_train_poly, y_train)

# tst_pred = pm1.predict(X_test_poly)
# r2 = r2_score(y_test, tst_pred)
# rmse = np.sqrt(mean_squared_error(y_test, tst_pred))
# print(f"  R-squared: {r2}")
# print(f"  RMSE: {rmse}")


# plt.figure(figsize=(8, 6))
# plt.scatter(y_test, tst_pred)
# plt.xlabel("Passing Yds")
# plt.ylabel("Predicted Passing Yds")