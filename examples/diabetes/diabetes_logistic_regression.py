# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from ztlearn.utils import *
from ztlearn.dl.optimizers import register_opt
from ztlearn.ml.regression import LogisticRegression

#-------------------------------------------------------------#
#            Diabetes Dataset Features                        #
#-------------------------------------------------------------#
# 1.Pregnancies, 2.Glucose, 3.BloodPressure, 4.SkinThickness, #
# 5.DiabetesPedigreeFunction, 6.Age, 7.Insulin, 8.BMI,        #
#-------------------------------------------------------------#
# Outcome                                                     #
#-------------------------------------------------------------#

dataset = pd.read_csv('../data/diabetes/pima-indians-diabetes.csv', sep = ',').values
input_data = z_score(dataset[:, 0:8]) # ----- all the features
# input_data = z_score(dataset[:, 5:6]) # ----- one of the features
input_label = dataset[:, 8]

train_data, test_data, train_label, test_label = train_test_split(input_data,
                                                                  input_label,
                                                                  test_size = 0.2,
                                                                  random_seed = 2)

opt = register_opt(optimizer_name = 'adam', momentum = 0.01, learning_rate = 0.01)
model = LogisticRegression(epochs = 10000, optimizer = opt)

fit_stats = model.fit(train_data, train_label)
# fit_stats = model.fit_NR(train_data, train_label) # --- Newton-Raphson Method

print_results(model.predict(test_data), np.round(test_label).astype(int))

plot_metric('Accuracy vs Loss',
                                len(fit_stats["train_loss"]),
                                fit_stats['train_acc'],
                                fit_stats['train_loss'],
                                legend = ['acc', 'loss'])

'''

# if you used only one feature
plot_regression_results(train_data, train_label,
                                                 test_data,
                                                 test_label,
                                                 input_data,
                                                 model.predict(input_data),
                                                 float(fit_stats['train_loss'][-1] * 100),
                                                 'Logistic Regression',
                                                 'Age',
                                                 'Outcome')

'''
