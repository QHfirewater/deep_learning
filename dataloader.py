from pickle import TRUE
import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

test_data = torchvision.datasets.CIFAR10('./dataset',train = False,transform=torchvision.transforms.ToTensor())
test_loader = DataLoader(dataset=test_data,batch_size=4,shuffle=True,drop_last=False)


img,target = test_data[0]
print(img.shape)


write = SummaryWriter('dataloader')
step = 0
for data in test_loader:
    imgs,targets = data
    write.add_image('test_data',imgs,step,dataformats='NCHW')
    step +=1

write.close()