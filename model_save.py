import torch
import torchvision

vgg16 = torchvision.models.vgg16(pretrained=False)


#保存方法1,模型结构加模型参数
torch.save(vgg16,'vgg16_method1.pth')


#保存方法2，仅模型参数
torch.save(vgg16.state_dict(),'vgg16_method2.pth')