import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import streamlit as st
import construct_general_model

import sys
import math

# for measuring the efficiency/variability of the model
from sklearn.metrics import mean_absolute_error

# importing XGBoost API
from xgboost import XGBRegressor

# importing joblib to save model as package
import joblib

# importing pathlib to handle paths to csv dataset
from pathlib import Path 

file_path = Path(__file__).parent.parent.joinpath('Dataset', "processed-data-i1.csv")
base_data_i1 = pd.read_csv(file_path)

X,y = construct_general_model.obtain_X_y()

model = joblib.load('gen_1st_inn_mode.pkl')
pred_y = model.predict(X)

err = abs(y - pred_y)

## under construction