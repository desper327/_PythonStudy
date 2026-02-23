import numpy as np

a=np.arange(15)
print(a)
print(a.shape)

b=a.reshape(3,5)
print(b)
print(b.shape)

c=np.array([2,4])
print(c)
print(c.shape)

d=np.arange(60).reshape(5,4,3)
print(d)
print(d.shape)

print('__'*30)

b=b.T
print(b)
print(b.shape)
b=b[:,None,:]
print(b)
print(b.shape)

e=b*d
print(e)
print(e.shape)