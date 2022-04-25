# -*- coding: utf-8 -*-
"""Pricing Ground Inc1.

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BFPnm-NvxO09dh5Xp011nAZe5Qha3ggy
"""

from google.colab import drive
drive.mount('/content/drive')

import os
path='/content/drive/MyDrive/Untitled folder (1)/gpcs301'
os.chdir(path)
print(os.listdir(path))

# Commented out IPython magic to ensure Python compatibility.
import jax as jnp
from jax import grad, jit, vmap
from jax import random
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rc
import pandas as pd
import unittest
import scipy 
from scipy.stats import norm

# %matplotlib inline

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

train['SalePrice'].describe()

plt.figure(figsize=(20,8))
sns.distplot(train['SalePrice'],fit_kws={'color':'red','label':'norm'})
plt.ylabel('')
plt.legend()
plt.show()

# Let's select the columns of the train set with numerical data
df_train_num = train.select_dtypes(exclude=["object"])
df_train_num.head()

pd.options.display.float_format = "{:,.2f}".format

corr_matrix = df_train_num.corr()

corr_matrix[(corr_matrix < 0.3) & (corr_matrix > -0.3)] = 0

df_num_corr = df_train_num.corr()["SalePrice"][:-1]
high_features_list = df_num_corr[abs(
    df_num_corr) >= 0.5].sort_values(ascending=False)
print(
    f"{len(high_features_list)} strongly correlated values with SalePrice:\n{high_features_list}\n")

var = 'OverallQual'
data = pd.concat([train['SalePrice'], train[var]], axis=1)
data.plot.scatter(x=var, y='SalePrice', ylim=(0,800000));

var = 'GrLivArea'
data = pd.concat([train['SalePrice'], train[var]], axis=1)
data.plot.scatter(x=var, y='SalePrice', ylim=(0,800000));

var = 'YearRemodAdd'
data = pd.concat([train['SalePrice'], train[var]], axis=1)
data.plot.scatter(x=var, y='SalePrice', ylim=(0,800000));

low_features_list = df_num_corr[(abs(df_num_corr) < 0.5) & (
    abs(df_num_corr) >= 0.3)].sort_values(ascending=False)
print(
    f"{len(low_features_list)} slightly correlated values with SalePrice:\n{low_features_list}")

var = 'OpenPorchSF'
data = pd.concat([train['SalePrice'], train[var]], axis=1)
data.plot.scatter(x=var, y='SalePrice', ylim=(0,800000));

var = '2ndFlrSF'
data = pd.concat([train['SalePrice'], train[var]], axis=1)
data.plot.scatter(x=var, y='SalePrice', ylim=(0,800000));

X = train.drop('SalePrice', axis=1)
y =train.SalePrice
X.columns

features_with_na=train.isnull().sum().sort_values(ascending=False)
percentage=(train.isnull().sum()/train.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([features_with_na, percentage], axis=1, keys=['Total', 'Percent'])
missing_data.head(10)

train_id = train['Id']
test_id = test['Id']

# drop them from dataset beacuse we don't need them in the model
train.drop('Id', axis=1, inplace=True)
test.drop('Id', axis=1, inplace=True)
# concatente train and test data do do our preprocessing in both of them
ntrain = train.shape[0]
ntest = test.shape[0]

y_train= train['SalePrice']
train.drop(['SalePrice'], axis=1, inplace=True)
all_data = pd.concat((train, test), ignore_index=True)
print("all_data size is : {}".format(all_data.shape))

#drop columns that have a lot of null values and will not affect our model
all_data.drop(['Alley', 'PoolQC', 'Fence', 'MiscFeature', 'FireplaceQu'], axis=1, inplace=True)

all_data.shape