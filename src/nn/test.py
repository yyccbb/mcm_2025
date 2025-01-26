import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import src.util.dataloader as dl

arr_1 = np.array([[1, 11, 111], [2, 22, 222], [1, 11, 111], [2, 22, 222]])
# print(arr_1.shape)

arr_2 = np.reshape(arr_1, (2, 2, 3), order='F')
# print(arr_2[:, 0 , :])

arr_3 = np.array([1, 2, 3, 1, 2, 3])
arr_4 = arr_3.reshape((3, 2), order='F')
print(arr_4)