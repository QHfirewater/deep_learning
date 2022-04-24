import torch
import torchvision

#第一种加载方式,存在陷阱，要有原来的代码
model1 = torch.load('vgg16_method1.pth')
print('第一种加载方式',model1)


#第二种加载方式
model2 = torch.load('vgg16_method2.pth')
print('我是model2',model2)
vgg16 = torchvision.models.vgg16(pretrained=False)
vgg16.load_state_dict(model2)
print('vgg16',vgg16)