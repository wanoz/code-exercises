# This module is made to aid data analysis by providing commonly used functions
# for inspecting and analysing a dataset. 
# 
# It may be helpful for:
# - Inspecting a set of data points for its distribution characterstic
# - Inspecting a set of data points for unique labels and their counts
# - Outputing transformed feature data via common feature engineering methods
# - Outputing transformed target label data as binary for One Vs All classification tasks

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.decomposition import PCA

# ===============================
# === Inspection and analysis ===

# Get dataframe containing information about the unique labels within the dataset column/array. 
def check_unique(df, target_heading):
    target_heading_desc = target_heading + ' - unique labels'
    target_heading_no = '(' + str(df[target_heading].nunique()) + ')'
    df_unique = pd.DataFrame({target_heading_desc + ' ' + str(target_heading_no) : df[target_heading].value_counts().index.values, 'Label count' : np.asarray(df[target_heading].value_counts())})
    return df_unique

# ==========================
# === Feature extraction ===

# Get dataframe that transforms/encodes discrete numbered features (e.g. 0 or 1, or 2, 10, 15) into continuous set of numbers
# Note: this adds some degree of randomisation of data, and applying encode based on the average of other samples (with exclusion
# of the active data point)
# Such feature engineering method may be useful with certain classifiers.
def get_continuous_mean(df, feature_heading, random_scaling=0.01):
    feature_series = df[feature_heading]
    feature_series_mean = [((sum(feature_series) - val)/(len(feature_series) - 1)) for val in feature_series]
    random_factor = np.random.rand(len(feature_series_mean))*random_scaling + 1
    feature_series_mean = np.multiply(np.asarray(feature_series_mean), random_factor).tolist()
    df_continuous_mean = pd.DataFrame({feature_heading : feature_series, feature_heading + '_mean_encoding' : feature_series_mean})
    return df_continuous_mean

# Apply sklearn scalers and output plots
def check_stats_scalers(df, feature_heading):
    # Set scaled data headers
    original_heading = feature_heading + '_original'
    std_scaled_heading = feature_heading + '_standard_scaled'
    minmax_scaled_heading = feature_heading + '_minmax_scaled'
    robust_scaled_heading = feature_heading + '_robust_scaled'
    
    # Reshape the 1D input data into "transposed" column-wise array for use with sklearn scaler functions
    feature_series = df[feature_heading]
    feature_array = feature_series.values.reshape(-1, 1)
    
    # Fit data to scaler functions and get the scaled data after transformation
    std_scaler = StandardScaler()
    minmax_scaler = MinMaxScaler()
    robust_scaler = RobustScaler()
    std_scaled_array = std_scaler.fit_transform(feature_array)
    minmax_scaled_array = minmax_scaler.fit_transform(feature_array)
    robust_scaled_array = robust_scaler.fit_transform(feature_array)
    
    # Append the scaled data to a custom dataframe
    df_new = pd.DataFrame({original_heading : feature_series})
    df_new[std_scaled_heading] = std_scaled_array
    df_new[minmax_scaled_heading] = minmax_scaled_array
    df_new[robust_scaled_heading] = robust_scaled_array
    
    # Visualise original and scaled data distributions
    original_data = pd.Series(feature_series, name=original_heading)
    std_scaled_data = pd.Series(df_new[std_scaled_heading], name=std_scaled_heading)
    minmax_scaled_data = pd.Series(df_new[minmax_scaled_heading], name=minmax_scaled_heading)
    robust_scaled_data = pd.Series(df_new[robust_scaled_heading], name=robust_scaled_heading)
    
    fig, ax = plt.subplots(2, 2, figsize=(15,11))
    sns.kdeplot(original_data, ax=ax[0][0], shade=True, color='b')
    sns.kdeplot(std_scaled_data, ax=ax[0][1], shade=True, color='y')
    sns.kdeplot(minmax_scaled_data, ax=ax[1][0], shade=True, color='y')
    sns.kdeplot(robust_scaled_data, ax=ax[1][1], shade=True, color='y')
    return df_new

# Apply math operation scaling and output plots
def check_math_scalers(df, feature_heading):
    # Set scaled data headers
    original_heading = feature_heading + '_original'
    log_scaled_heading = feature_heading + '_log_scaled'
    sqrt_scaled_heading = feature_heading + '_sqrt_scaled'
    tanh_scaled_heading = feature_heading + '_tanh_scaled'
    
    # Reshape the 1D input data into "transposed" column-wise array for use with sklearn scaler functions
    feature_series = df[feature_heading]
    
    # Fit data to scaler functions and get the scaled data after transformation
    if np.min(feature_series.values) < 0:
        feature_array = feature_series.values - np.min(feature_series.values)*(1.000001)
    elif np.min(feature_series.values) == 0:
        feature_array = feature_series.values + 0.000001
    else:
        feature_array = feature_series.values
    log_scaled_array = np.log(feature_array)
    sqrt_scaled_array = np.sqrt(feature_array)
    tanh_scaled_array = np.tanh(feature_series)
    
    # Append the scaled data to a custom dataframe
    df_new = pd.DataFrame({original_heading : feature_series})
    df_new[log_scaled_heading] = log_scaled_array
    df_new[sqrt_scaled_heading] = sqrt_scaled_array
    df_new[tanh_scaled_heading] = tanh_scaled_array
    
    # Visualise original and scaled data distributions
    original_data = pd.Series(feature_series, name=original_heading)
    log_scaled_data = pd.Series(df_new[log_scaled_heading], name=log_scaled_heading)
    sqrt_scaled_data = pd.Series(df_new[sqrt_scaled_heading], name=sqrt_scaled_heading)
    tanh_scaled_data = pd.Series(df_new[tanh_scaled_heading], name=tanh_scaled_heading)
    
    fig, ax = plt.subplots(2, 2, figsize=(15,11))
    sns.kdeplot(original_data, ax=ax[0][0], shade=True, color='b')
    sns.kdeplot(log_scaled_data, ax=ax[0][1], shade=True, color='y')
    sns.kdeplot(sqrt_scaled_data, ax=ax[1][0], shade=True, color='y')
    sns.kdeplot(tanh_scaled_data, ax=ax[1][1], shade=True, color='y')
    return df_new

# Perform PCA and output scatter plot
def check_pca_scatter(df, scaler='standard', components=2, target_label=None):
    # Apply scaler to data
    if scaler == 'standard':
        scaler = StandardScaler()
        scaler.fit(df)
    elif scaler == 'minmax':
        scaler = MinMaxScaler()
        scaler.fit(df)
    else:
        scaler = RobustScaler()
        scaler.fit(df)
    
    # Fit data to PCA transformation
    df_pca = scaler.transform(df)

    # Get the top 2 principal components
    pca = PCA(n_components=int(components))
    pca.fit(df_pca)
    x_pca = pca.transform(df_pca)

     # Set PCA components as per input
    if components == 2:
        column_headers = ['1st principal component', '2nd principal component']
    elif components == 3:
        column_headers = ['1st principal component', '2nd principal component', '3rd principal component']
    elif components == 4:
        column_headers = ['1st principal component', '2nd principal component', '3rd principal component', '4th principal component']
    else:
        print('Warning: number of components argument entered is less than 2 or greater than 4. Thus, components outputs have been downscaled to 4 components.')
        column_headers = ['1st principal component', '2nd principal component', '3rd principal component', '4th principal component']

    df_x_pca = pd.DataFrame(data=x_pca, columns=column_headers)
    df_x_pca = pd.concat([df_x_pca, df[target_label]], axis=1)

    # Plot the PCA scatter plot
    g_pca_scatter = sns.lmplot(data=df_x_pca, x='1st principal component', y='2nd principal component', hue=target_label, fit_reg=False, palette='plasma', size=7, aspect=1.5)

    return df_x_pca
    
# Perform PCA and output heatmap
def check_pca_heatmap(df, scaler='standard', components=2, annot=False):
    # Apply scaler to data
    if scaler == 'standard':
        scaler = StandardScaler()
        scaler.fit(df)
    elif scaler == 'minmax':
        scaler = MinMaxScaler()
        scaler.fit(df)
    else:
        scaler = RobustScaler()
        scaler.fit(df)
    
    # Fit data to PCA transformation
    df_pca = scaler.transform(df)

    # Get the top 2 principal components
    pca = PCA(n_components=int(components))
    pca.fit(df_pca)

    # Set PCA components as per input
    if components == 2:
        column_headers = ['1st principal component', '2nd principal component']
    elif components == 3:
        column_headers = ['1st principal component', '2nd principal component', '3rd principal component']
    elif components == 4:
        column_headers = ['1st principal component', '2nd principal component', '3rd principal component', '4th principal component']
    else:
        print('Warning: number of components argument entered is less than 2 or greater than 4. Thus, components outputs have been downscaled to 4 components.')
        column_headers = ['1st principal component', '2nd principal component', '3rd principal component', '4th principal component']

    # Plot the PCA heatmap
    feature_headings = df.columns.values.tolist()
    df_comp = pd.DataFrame(pca.components_, columns=feature_headings)
    df_comp = df_comp.set_index([column_headers])
    plt.figure(figsize=(15, 7))
    g_pca_heatmap = sns.heatmap(data=df_comp, annot=annot, cmap='plasma')

    return df_comp