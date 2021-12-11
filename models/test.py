import os.path

import numpy as np
import torch
from torch import nn
import Model

import Constants

x_data = torch.load(os.path.join(Constants.ROOT_DIR, 'data/X.pt'))
y_data = torch.load(os.path.join(Constants.ROOT_DIR, 'data/Y.pt'))

model = Model.get_model_cnn()
model.load_state_dict(torch.load('slow_cnn_20k_model.pt'))
model.eval()
num_to_test = 18000 - 14401
predictions = np.empty((num_to_test, 2))
actual = np.empty((num_to_test, 2))
divs_white = np.empty(num_to_test)
divs_black = np.empty(num_to_test)
for index in range(14401, 18000):
    x = x_data[index].float()
    x = x[None, None, :]
    pred = model(x).detach().numpy()[0]
    print(pred)
    y_actual = y_data[index].float().detach().numpy()
    div_white = pred[0] - y_actual[0]
    div_black = pred[1] - y_actual[1]
    i = index - 14401
    predictions[i] = pred
    actual[i] = y_actual
    divs_white[i] = div_white
    divs_black[i] = div_black
    print(
        f'prediction = {pred}, actual = {y_actual}, '
        f'div white = {div_white}, div black = {div_black}'
    )

print(
    f'\nstatistics: \nstd white = {np.std(divs_white)}, std black = {np.std(divs_black)} \n'
    f'mean white = {np.mean(divs_white)}, mean black = {np.mean(divs_black)} \n'
    f'max white = {np.max(divs_white)}, max black = {np.max(divs_black)} \n'
    f'min white = {np.min(divs_white)}, min black = {np.min(divs_black)}'
)
