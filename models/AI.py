"""
The AI class will decide the player's elo.
"""
import math

import numpy as np
import torch
import torch.nn as nn
import os.path
import Model

import Constants
import time
import csv
import torchvision
import torchvision.transforms as transforms
from torch.utils.tensorboard import SummaryWriter


def split_train_test(x1, x2, y, train_percentage=0.8):
    indices = np.asarray(range(len(x1)))
    np.random.shuffle(indices)
    split = math.floor(len(x1) * train_percentage)
    train_indices, test_indices = indices[:split], indices[split:]
    with open('indices.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(train_indices)
        writer.writerow(test_indices)

    return x1[train_indices], x2[train_indices], y[train_indices], \
           x1[test_indices], x2[test_indices], y[test_indices]


def train(model, Xin1, Xin2, Y, learning_rate=1e-3, epochs=2000, batch_size=128):
    device = torch.device('cuda')

    Xin1 = Xin1[:, None, :]

    model = model.float()
    model.to(device)

    loss_func = nn.MSELoss(reduction='sum')
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # train_loader = torch.utils.data.DataLoader(x, batch_size=batch_size, shuffle=True, num_workers=1)
    print_every = 10
    t = time.perf_counter_ns()
    for epoch in range(epochs):
        permutation = torch.randperm(Xin1.size()[0])
        for i in range(0, Xin1.size()[0], batch_size):
            indices = permutation[i:i + batch_size]
            batch_x, batch_x2, batch_y = Xin1[indices], Xin2[indices], Y[indices]
            y_hat = model(batch_x.cuda(), batch_x2.cuda())
            loss = loss_func(y_hat, batch_y.cuda())
            if epoch % print_every == 0 and i == 0:
                print(f'epoch = {epoch}, loss = {loss.item()}')
                tb = (time.perf_counter_ns() - t) / print_every / 1e9 / 3600
                t = time.perf_counter_ns()
                print(f'time between epochs = {tb} hrs')
                print(f'estimated time left = {tb * (epochs - epoch)} hrs')
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    torch.save(model.state_dict(), 'board_and_eval_model.pt')


def test(model, weights_file, X, X2, Y):
    device = torch.device('cuda')
    model.load_state_dict(torch.load(weights_file))
    model.eval()
    model.to(device)
    num_to_test = len(X)
    predictions = np.empty((num_to_test, 2))
    actual = np.empty((num_to_test, 2))
    divs_white = np.empty(num_to_test)
    divs_black = np.empty(num_to_test)
    for i in range(num_to_test):
        x = X[i, :].float()
        x = x[None, None, :]
        x2 = X2[i].float()
        x2 = x2[None, :, :]
        y_hat = model(x.cuda(), x2.cuda()).detach().numpy()[0]
        if i == 0:
            tb = SummaryWriter()
            tb.add_graph(model, [x.cuda(), x2.cuda()])
            tb.close()
        print(y_hat)
        y_actual = Y[i].float().detach().numpy()
        div_white = y_hat[0] - y_actual[0]
        div_black = y_hat[1] - y_actual[1]
        predictions[i] = y_hat
        actual[i] = y_actual
        divs_white[i] = div_white
        divs_black[i] = div_black
        print(
            f'prediction = {y_hat}, actual = {y_actual}, '
            f'div white = {div_white}, div black = {div_black}'
        )
    str_res = f'\nstatistics: \nstd white = {np.std(divs_white)}, std black = {np.std(divs_black)} \n' \
              f'mean white = {np.mean(divs_white)}, mean black = {np.mean(divs_black)} \n' \
              f'max white = {np.max(divs_white)}, max black = {np.max(divs_black)} \n' \
              f'min white = {np.min(divs_white)}, min black = {np.min(divs_black)}'
    with open('results.txt', 'w') as res:
        res.write(str_res)
    print(str_res)


def train_dataloader_model(model, train_loader, learning_rate=1e-3, epochs=2000, batch_size=128):
    device = ("cuda" if torch.cuda.is_available() else cpu)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.MSELoss(reduction='sum')

    tb = SummaryWriter()

    for epoch in range(epochs):

        total_loss = 0
        total_correct = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            preds = model(inputs)

            loss = criterion(preds, labels)
            total_loss += loss.item()
            total_correct += get_num_correct(preds, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        tb.add_scalar("Loss", total_loss, epoch)
        tb.add_scalar("Correct", total_correct, epoch)
        tb.add_scalar("Accuracy", total_correct / len(train_set), epoch)

        tb.add_histogram("conv1.bias", model.conv1.bias, epoch)
        tb.add_histogram("conv1.weight", model.conv1.weight, epoch)
        tb.add_histogram("conv2.bias", model.conv2.bias, epoch)
        tb.add_histogram("conv2.weight", model.conv2.weight, epoch)

        tb.add_hparams(
            {"lr": learning_rate, "bsize": batch_size, "shuffle": shuffle},
            {
                "accuracy": total_correct / len(train_set),
                "loss": total_loss,
            },
        )

        print("epoch:", epoch, "total_correct:", total_correct, "loss:", total_loss)

    tb.close()


def get_num_correct(preds, labels):
    return preds.argmax(dim=1).eq(labels).sum().item()


# x_data = torch.load(os.path.join(Constants.ROOT_DIR, 'data/X.pt')).float()
# y_data = torch.load(os.path.join(Constants.ROOT_DIR, 'data/Y.pt')).float()
# x2_data = torch.load(os.path.join(Constants.ROOT_DIR, 'data/X2.pt')).float()
#
# train_x, train_x2, train_y, test_x, test_x2, test_y = split_train_test(x_data, x2_data, y_data)
#
# ai_model = Model.GameEvalInput()
#
# test(ai_model, 'slow_cnn_20k_model.pt', test_x, test_x2, test_y)
print(torch.__version__)
train_set = torchvision.datasets.FashionMNIST(root="./data",
                                              train=True,
                                              download=True,
                                              transform=transforms.ToTensor())
train_loader = torch.utils.data.DataLoader(train_set,batch_size = 100, shuffle = True)
# train_dataloader_model()

tb = SummaryWriter()
model = Model.CNN()
images, labels = next(iter(train_loader))
grid = torchvision.utils.make_grid(images)
tb.add_image("images", grid)
tb.add_graph(model, images)
tb.close()