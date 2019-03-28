# -*- coding: utf-8 -*-
"""
cifar10-tutorial stolen from: https://github.com/pytorch/tutorials/blob/master/beginner_source/blitz/cifar10_tutorial.py

Training a Classifier
=====================

For this tutorial, we will use the CIFAR10 dataset.
It has the classes: ‘airplane’, ‘automobile’, ‘bird’, ‘cat’, ‘deer’,
‘dog’, ‘frog’, ‘horse’, ‘ship’, ‘truck’. The images in CIFAR-10 are of
size 3x32x32, i.e. 3-channel color images of 32x32 pixels in size.

"""

import os
import sys
cwd = os.getcwd()
sys.path.append(cwd)

import torch.nn as nn
import torch.optim as optim
from resmonres.monitor_system_parameters import MonitorSysParams
from pytorch_image_classifier_example.some_methods import train_neural_network, evaluate_model, load_data
import torch
from pytorch_image_classifier_example.neural_nets import SuperCoolNeuralNetwork


trainloader,testloader,classes = load_data(cwd)

# show_images(trainloader,classes)
net = SuperCoolNeuralNetwork()


criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)


########################################################################
# 4. Train the network
# ^^^^^^^^^^^^^^^^^^^^
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print('using: %s'%device)

with MonitorSysParams(log_path='.'):
    train_neural_network(trainloader,net,criterion,optimizer,device)
    evaluate_model(net,testloader,classes)