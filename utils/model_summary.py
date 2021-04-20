import torch
from torchsummary import summary

model = torch.load('model\\best_policy_value_net.pth')
summary(model, input_size=(6, 9, 9))
