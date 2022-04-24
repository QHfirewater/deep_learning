import torchvision
from torch import nn
from torch.nn import Linear,Conv2d,MaxPool2d,Flatten,Sequential,CrossEntropyLoss
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

dataset  = torchvision.datasets.CIFAR10('../data',train=False,download=True,transform=torchvision.transforms.ToTensor())

dataloader = DataLoader(dataset,batch_size=1)

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
loss = CrossEntropyLoss()
for data in dataloader:
    img,target = data
    out_puts = tudui(img)
    result_loss  = loss(out_puts,target)
    print(result_loss)
