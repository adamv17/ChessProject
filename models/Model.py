import os

import torch
from torch import nn
from torchviz import make_dot
import torch.nn.functional as F

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
        self.evl = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=200, kernel_size=20),
            nn.ReLU(inplace=True),
            nn.Flatten(),
            nn.Linear(in_features=6200, out_features=50),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=50, out_features=50),
            nn.ReLU(inplace=True),
        )
        self.game = nn.Sequential(
            nn.Linear(in_features=64, out_features=512),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=512, out_features=128),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=128, out_features=128),
            nn.ReLU(inplace=True)
        )
        self.fc_combine = nn.Sequential(
            nn.Linear(in_features=6450, out_features=100),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=100, out_features=2),
        )
        # nn.Softmax()

    def forward(self, input1, input2):
        e = self.evl(input1)
        g = self.game(input2)
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


# def visualize():
#     model = get_model_cnn()
#     model.eval()
#     x_data = torch.load(os.path.join(Constants.ROOT_DIR, 'data/X.pt')).float()
#     x = x_data[14401:18000].float()
#     x = x[:, None, :]
#     y = model(x)
#     make_dot(y.mean(), params=dict(list(model.named_parameters()))).render('learning_torchviz', format='png')
#     # default `log_dir` is "runs" - we'll be more specific here
#     writer = SummaryWriter('runs')
#     writer.add_graph(model, x)
#     writer.close()

# only for testing tensorboard
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5)
        self.conv2 = nn.Conv2d(in_channels=6, out_channels=12, kernel_size=5)

        self.fc1 = nn.Linear(in_features=12*4*4, out_features=120)
        self.fc2 = nn.Linear(in_features=120, out_features=60)
        self.out = nn.Linear(in_features=60, out_features=10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, kernel_size = 2, stride = 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, kernel_size = 2, stride = 2)
        x = torch.flatten(x,start_dim = 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.out(x)

        return x