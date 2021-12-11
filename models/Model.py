import os

import torch
from torch import nn
from torchviz import make_dot
from torch.utils.tensorboard import SummaryWriter

import Constants


def get_model_cnn():
    model = nn.Sequential(
        nn.Conv1d(in_channels=1, out_channels=200, kernel_size=20),
        nn.ReLU(),
        nn.Flatten(),
        nn.Linear(in_features=6200, out_features=50),
        nn.ReLU(),
        nn.Linear(in_features=50, out_features=50),
        nn.ReLU(),
        nn.Linear(in_features=50, out_features=2)
    )
    return model


class GameEvalInput(nn.Module):
    def __init__(self):
        super().__init__()
        self.game = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=400, kernel_size=10),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=5, stride=2),
            nn.Conv1d(in_channels=400, out_channels=500, kernel_size=10),
            nn.ReLU(),
            nn.Linear(in_features=500, out_features=50),
            nn.ReLU()
        )
        self.eval = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=200, kernel_size=20),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(in_features=6200, out_features=50),
            nn.ReLU(),
            nn.Linear(in_features=50, out_features=50),
            nn.ReLU(),
        )
        self.fc_combine = nn.Sequential(
            nn.Linear(in_features=50, out_features=30),
            nn.ReLU(),
            nn.Linear(in_features=30, out_features=2)
        )

    def forward(self, input1, input2):
        g = self.game(input1)
        e = self.eval(input2)
        combined = torch.cat((g.view(g.size(0), -1),
                              e.view(e.size(0), -1)), dim=1)
        out = self.fc_combine(combined)
        return out


def get_model_dense():
    model = nn.Sequential(
        nn.Linear(in_features=50, out_features=50),
        nn.ReLU(),
        nn.Linear(in_features=50, out_features=50),
        nn.ReLU(),
        nn.Linear(in_features=50, out_features=50),
        nn.ReLU(),
        nn.Linear(in_features=50, out_features=2)
    )
    return model


def visualize():
    model = get_model_cnn()
    model.eval()
    x_data = torch.load(os.path.join(Constants.ROOT_DIR, 'data/X.pt')).float()
    x = x_data[14401:18000].float()
    x = x[:, None, :]
    y = model(x)
    make_dot(y.mean(), params=dict(list(model.named_parameters()))).render('learning_torchviz', format='png')
    # default `log_dir` is "runs" - we'll be more specific here
    writer = SummaryWriter('runs')
    writer.add_graph(model, x)
    writer.close()
