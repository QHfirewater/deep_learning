from matplotlib import image
import torch
import torchvision
from PIL import Image
from torch import   nn  

image_path = r'C:\Users\honor\Desktop\微信截图_20220314165526.png'
imge = Image.open(image_path)
imge = imge.convert('RGB')
print(imge)

transform = torchvision.transforms.Compose([torchvision.transforms.Resize((32,32)),torchvision.transforms.ToTensor()])
imge = transform(imge)
print(imge.shape)

#定义网络模型
class Tudui(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3,32,5,1,2),
            nn.MaxPool2d(2),
            nn.Conv2d(32,32,5,1,2),
            nn.MaxPool2d(2),
            nn.Conv2d(32,64,5,1,2),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(64*4*4,64),
            nn.Linear(64,10)
        )
    

    def forward(self,x):
        x = self.model(x)
        return x 

model = torch.load(r'D:\software\notebook\数据分析学习\练习案例\tudui.pth',map_location='cuda')
tudui = Tudui()
tudui.load_state_dict(model)
print(tudui)
imge = torch.reshape(imge,(1,3,32,32))
tudui.eval()
print(imge.shape)
with torch.no_grad():
    output = tudui(image)
print(output)
print(output.argmax(1))