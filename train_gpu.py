
from csv import writer
from torch import  nn
import torch 
import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
import time

#下载数据
data_train = torchvision.datasets.CIFAR10(root = r'./data',train = True,transform=torchvision.transforms.ToTensor(),download=True)
data_test = torchvision.datasets.CIFAR10(root = r'./data',train = False,transform=torchvision.transforms.ToTensor(),download=True)

test_data_size = len(data_test)

#加载数据
data_train = DataLoader(data_train,batch_size=64)
data_test = DataLoader(data_test,batch_size=64)

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


#创建网络模型
tudui = Tudui()
tudui = tudui.cuda()  #条用GPU

#创建损失函数
loss_fn = nn.CrossEntropyLoss()
loss_fn = loss_fn.cuda()  #调用GPU

#定义一个优化器
learning_rate = 1e-2
opt = torch.optim.SGD(tudui.parameters(),lr = learning_rate)

#设置训练网络一些参数
total_train_step= 0  #记录训练的次数
total_test_step = 0  #记录测试次数

epoch = 10   #设置训练的轮数

#添加tensorboard
writer = SummaryWriter('./log_train')

#开始训练模型
start_time = time.time()
for i in range(epoch):
    print('-----------第{}轮训练开始了--------------'.format(i+1))

    tudui.train()
    for data in data_train:
        img,target = data
        img = img.cuda()
        target = target.cuda()
        #模型预测
        out_put = tudui(img)

        #优化器优化模型
        loss = loss_fn(out_put,target)
        opt.zero_grad()
        loss.backward()
        opt.step()

        total_train_step +=1

        if total_train_step %100 ==0:
            print('训练次数为：{}，loss值为：{}'.format(total_train_step,loss.item()))
            writer.add_scalar('train_loss',loss.item(),total_train_step)

    #测试步骤开始
    tudui.eval()
    total_test_loss = 0
    total_accuary = 0
    with torch.no_grad():
        for data in data_test:
            img,target = data
            img = img.cuda()
            target = target.cuda()
            out_put = tudui(img)
            loss = loss_fn(out_put,target)

            total_test_loss += loss.item()

            accuary = (out_put.argmax(1) == target).sum()
            total_accuary += accuary
            accuracy_rate = total_accuary/test_data_size


    total_test_step += 1
    print('整体测试集上的loss:{}'.format(total_test_loss))
    print('整体测试集上的真确率是{}'.format(accuracy_rate))
    writer.add_scalar('test_loss',total_test_loss,total_test_step)
    writer.add_scalar('test_accuracy',accuracy_rate,total_test_step)

#模型保存
torch.save(tudui.state_dict(),'tudui.pth')
print('模型已保存')
end_time = time.time()
print('一共用时{}'.format(str(end_time-start_time)))

if __name__ == '__main__':
    pass 
    # tudui = Tudui()
    # in_put = torch.ones((64,3,32,32))
    # out_put = tudui(in_put)
    # print(out_put.shape)

