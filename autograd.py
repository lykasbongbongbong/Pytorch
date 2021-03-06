# -*- coding: utf-8 -*-
"""autograd.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LORLiEJEeDb0Dtm18f_olnZxRNWQsZTW

#Autograd:
"""

import torch 
import math

dtype = torch.float
device = torch.device("cuda:0")

#create tensor to hold input and outputs
#the default requires_grad = False: means that for these tensor, there won't be gradient computations
x = torch.linspace(-math.pi, math.pi, 2000, device=device, dtype=dtype)
y = torch.sin(x)

#create random tensor for weights
# 4 weights: y = a + b x + c x^2 + d x^3
# Note: we have to set requires_grad = True since we want to compute gradients w.r.t these tensors during backward pass
a = torch.randn((), device=device, dtype=dtype, requires_grad=True)
b = torch.randn((), device=device, dtype=dtype, requires_grad=True)
c = torch.randn((), device=device, dtype=dtype, requires_grad=True)
d = torch.randn((), device=device, dtype=dtype, requires_grad=True)

learning_rate = 1e-6
for t in range(2000):
  #forward prop:
  y_pred = a + b*x + c*x**2 + d*x**3

  #compute loss:
  loss = (y_pred - y).pow(2).sum()
  if t % 100 == 99:
    print(t, loss.item())
  
  #backward: use autograd to compute the backward pass. 
  #this call will compute the gradient of loss w.r.t. all tensors with requires_grad = True
  #so a.grad, b.grad, c.grad, d.grad will be tensors holding the gradient of the loss w.r.t. a,b,c,d
  loss.backward()

  # Manually update weights using gradient descent. Wrap in torch.no_grad()
  # because weights have requires_grad=True, but we don't need to track this
  # in autograd.
  with torch.no_grad():
      a -= learning_rate * a.grad
      b -= learning_rate * b.grad
      c -= learning_rate * c.grad
      d -= learning_rate * d.grad

      # Manually zero the gradients after updating weights
      a.grad = None
      b.grad = None
      c.grad = None
      d.grad = None
    

print(f'Result: y = {a.item()} + {b.item()} x + {c.item()} x^2 + {d.item()} x^3')