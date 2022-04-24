import torch 
from torch.nn  import L1Loss
from torch.nn  import MSELoss
from torch.nn  import CrossEntropyLoss

in_put = torch.tensor([1,2,3],dtype=torch.float)
out_put = torch.tensor([1,2,5],dtype=torch.float)

in_put = torch.reshape(in_put,(1,1,1,3))
out_put = torch.reshape(out_put,(1,1,1,3))



loss = L1Loss(reduction='sum')
result = loss(in_put,out_put)
print(result)

loss_mse = MSELoss()
result_mse = loss_mse(in_put,out_put)
print(result_mse)


x = torch.tensor([0.1,0.2,0.3])
y =torch.tensor([1])
x = torch.reshape(x,(1,3))
print(x)
loss_cross = CrossEntropyLoss()
result_coss = loss_cross(x,y)
print(result_coss)