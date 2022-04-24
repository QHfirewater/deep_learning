import torchvision
from torch import nn
from torch.nn import Linear
import torch
from torch.utils.data import DataLoader


dataset  = torchvision.datasets.CIFAR10('../data',train=False,download=True,transform=torchvision.transforms.ToTensor())

dataloader = DataLoader(dataset,batch_size=64)

class Tudui(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.linear1 = Linear(196608,10)
        

    def forward(self,in_put):
        out_put =self.linear1(in_put)
        return out_put


tudui = Tudui()



step = 0
print('开始循环')
for data in dataloader:
    img,target = data
    print(img.shape)
    out_put = torch.reshape(img,(1,1,1,-1))
    print(out_put.shape)
    

    out_put = tudui(out_put)
    print(out_put.shape)
    



