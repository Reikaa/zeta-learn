# -*- coding: utf-8 -*-

import numpy as np
from sklearn import datasets

from ztlearn.utils import *
from ztlearn.dl.optimizers import register_opt
from ztlearn.ml.regression import ElasticNetRegression
from ztlearn.dl.objectives import ObjectiveFunction as objective

data = datasets.load_boston()
# print(data['DESCR'])

# take the boston data
boston_data = data['data']
input_data = z_score(boston_data[:,[5]]) # work with only one of the features: RM
input_label = data['target']

train_data, test_data, train_label, test_label = train_test_split(input_data,
                                                                  input_label,
                                                                  test_size = 0.3)

opt = register_opt(optimizer_name = 'sgd', momentum = 0.01, learning_rate = 0.001)

model = ElasticNetRegression(degree = 3,
                                         epochs = 100,
                                         optimizer = opt,
                                         penalty = 'elastic',
                                         penalty_weight = 0.01,
                                         l1_ratio = 0.5)

fit_stats = model.fit(train_data, train_label)

targets = np.expand_dims(test_label, axis = 1)
predictions = np.expand_dims(model.predict(test_data), axis = 1)

mse = objective('mean_squared_error').forward(predictions, targets)
print('Mean Squared Error: {:.2f}'.format(mse))

plot_metric('Accuracy vs Loss',
                                len(fit_stats['train_loss']),
                                fit_stats['train_acc'],
                                fit_stats['train_loss'],
                                legend = ['acc', 'loss'])

plot_regression_results(train_data, train_label,
                                                 test_data,
                                                 test_label,
                                                 input_data,
                                                 model.predict(input_data),
                                                 mse,
                                                'Elastic Regression',
                                                'Median House Price',
                                                'Average Number of Rooms')
