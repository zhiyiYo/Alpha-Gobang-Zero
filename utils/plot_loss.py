import numpy as np
import matplotlib.pyplot as plt
import json

plt.style.use(['matlab'])

with open('..\\log\\train_losses.json', encoding='utf-8') as f:
    loss = [i[1] for i in json.load(f)]
print(len(loss))
fig = plt.figure('误差曲线')
plt.plot(loss)
plt.title('loss curve')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()
