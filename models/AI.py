"""
The AI class will decide the player's elo.
"""
import torch
import torch.nn as nn
import os.path
import Model

import Constants


def train():
    x_data = torch.load(os.path.join(Constants.ROOT_DIR, 'data/X.pt'))
    y_data = torch.load(os.path.join(Constants.ROOT_DIR, 'data/Y.pt'))

    device = torch.device('cuda')

    x = x_data[0:14400].float()
    y = y_data[0:14400].float()

    x = x[:, None, :]

    model = Model.get_model_cnn()

    model = model.float()
    model.to(device)

    loss_func = nn.MSELoss(reduction='sum')
    learning_rate = 1e-3
    epochs = 2000
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    batch_size = 128

    # train_loader = torch.utils.data.DataLoader(x, batch_size=batch_size, shuffle=True, num_workers=1)

    for epoch in range(epochs):
        permutation = torch.randperm(x.size()[0])
        for i in range(0, x.size()[0], batch_size):
            indices = permutation[i:i + batch_size]
            batch_x, batch_y = x[indices], y[indices]
            y_pred = model(batch_x.cuda())
            loss = loss_func(y_pred, batch_y.cuda())
            if epoch % 100 == 0:
                print(epoch, loss.item())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    torch.save(model.state_dict(), 'slow_cnn_20k_model.pt')


train()
