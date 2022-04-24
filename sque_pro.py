import torchvision
from torch import nn
from torch.nn import Linear,Conv2d,MaxPool2d,Flatten,Sequential
import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter


class Tudui(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = Conv2d(3,32,5,padding=2)
        self.maxpool1 = MaxPool2d(2)
        self.conv2 = Conv2d(32,32,5,padding=2)
        self.maxpool2 = MaxPool2d(2)
        self.conv3 = Conv2d(32,64,5,padding=2)
        self.maxpool3 = MaxPool2d(2)
        self.flatten = Flatten()
        self.linear1 = Linear(1024,64)
        self.linear2 = Linear(64,10)

        self.model1 = Sequential(
                                    Conv2d(3,32,5,padding=2),
                                    MaxPool2d(2),
                                    Conv2d(32,32,5,padding=2),
                                    MaxPool2d(2),
                                    Conv2d(32,64,5,padding=2),
                                    MaxPool2d(2),
                                    Flatten(),
                                    Linear(1024,64),
                                    Linear(64,10))


    def forward(self,x):
        x  = self.model1(x)
        return x

tudui = Tudui()


writer = SummaryWriter('./logs_sequ')



in_put = torch.ones((64,3,32,32))
out_put  =tudui(in_put)
print(out_put.shape)


writer.add_graph(tudui,in_put)
writer.close()