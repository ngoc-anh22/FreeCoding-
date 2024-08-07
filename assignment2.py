# -*- coding: utf-8 -*-
"""Assignment2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15aP_KxowiLzah2e4XkOa2GHZTJLFz8b2
"""

!pip install torch==1.11.0+cu102 torchvision==0.12.0+cu102 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu102

import torch
import torch.nn as nn
from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader

dataset = datasets.MNIST(root ='./ data ', train = True, download = True,
                         transform = ToTensor())
trainset, valset = torch.utils.data.random_split(dataset, [0.8,0.2])
testset = datasets.MNIST(root ='./ data ', train = False, download = True,
                         transform = ToTensor())

"""Building Multilayer Perceptron model"""

class MLP (nn.Module):
  def __init__(self, hiddenLayerSize):
    super(MLP, self).__init__()
    self.inputLayerSize = 784
    self.hiddenLayerSize = hiddenLayerSize
    self.outputLayerSize = 10
    self.reLU = nn.ReLU()

    self.layer1 = nn.Linear(self.inputLayerSize, self.hiddenLayerSize)
    self.layer2 = nn.Linear(self.hiddenLayerSize, self.hiddenLayerSize)
    self.outputLayer = nn.Linear(self.hiddenLayerSize, self.outputLayerSize)

  def forward(self, x):
    x = x.view(-1,self.inputLayerSize)
    x = self.reLU(self.layer1(x))
    x = self.reLU(self.layer2(x))
    x = self.outputLayer(x)
    return x

"""Data Loader"""

batch_size = 64
train_loader = DataLoader(trainset, batch_size = batch_size, shuffle = True)
val_loader = DataLoader(valset, batch_size = batch_size, shuffle = False)
test_loader = DataLoader(testset, batch_size = batch_size, shuffle = False)

"""Model and loss function"""

hiddenLayerSize = 256
model = MLP(hiddenLayerSize)
lossFunction = nn.CrossEntropyLoss()

"""Optimizer"""

learning_rate = 0.01
optimizer = torch.optim.SGD(model.parameters(), learning_rate)

"""Training and validation"""

def train (train_loader, model, lossFunction, optimizer):
  model.train()
  train_size = len(dataset)
  train_loss = 0
  train_correct = 0
  for batch, (X,y) in enumerate(train_loader):
    pred = model(X)
    loss = lossFunction(pred, y)
    train_loss += loss.item()
    train_correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    if batch % 200 == 0:
      lossItem = loss.item()
      current = (batch + 1) * len(X)
      print(f"loss: {loss:>3f}  [{current:5d}/{train_size:>5d}]")

  train_loss /= len(train_loader)
  train_correct /= len(train_loader.dataset)
  print(f"Train: Accuracy: {(100*train_correct):>0.1f}%, Avg loss: {train_loss:>6f} \n")

def val (val_loader,model, lossFunction):
  model.eval()
  val_loss = 0
  val_correct = 0

  with torch.no_grad():
    for X, y in val_loader:
      val_pred = model(X)
      val_loss += lossFunction(val_pred, y).item()
      val_correct += (val_pred.argmax(1) == y).type(torch.float).sum().item()

  val_loss /= len(val_loader)
  val_correct /= len(val_loader.dataset)
  print(f"Validation: Accuracy: {(100*val_correct):>0.1f}%, Avg loss: {val_loss:>6f} \n")

"""Testing"""

def test (test_loader,model, lossFunction):
  model.eval()
  test_loss = 0
  test_correct = 0

  with torch.no_grad():
    for X, y in test_loader:
      pred = model(X)
      test_loss += lossFunction(pred, y).item()
      test_correct += (pred.argmax(1) == y).type(torch.float).sum().item()

  test_loss /= len(test_loader)
  test_correct /= len(test_loader.dataset)
  print(f"Test: Accuracy: {(100*test_correct):>0.1f}%, Avg loss: {test_loss:>6f} \n")

"""Main"""

epochs = 20
for epoch in range (epochs):
  print(f"With epoch {epoch}: ")
  train(train_loader, model, lossFunction, optimizer)
  val(val_loader, model, lossFunction)
print("Finish training!")
test(test_loader, model, lossFunction)