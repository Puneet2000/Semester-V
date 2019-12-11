# package/model
import numpy as np
import itertools
import cv2

class Model:
	def __init__(self,nodes=[2,2,1]):
		self.nodes = nodes
		self.len = len(self.nodes)
		self.weights = [np.random.randn(self.nodes[i],self.nodes[i-1]) for i in range(1,self.len)]
		self.biases = [np.random.rand(i, 1) for i in self.nodes[1:]]
		self.activation = lambda x: 1/(1+np.exp(-x))
		self.d_activation = lambda x: x*(1-x)
		

	def printL(self,x):
		for i in range(len(x)):
			print(x[i].shape)

	def forward(self,x):
		self.outputs = [x]
		for i in range(self.len-1):
			self.outputs.append(self.activation(np.dot(self.weights[i],self.outputs[-1]) + self.biases[i]))
		return self.outputs[-1]

	def backward(self,x,y):
		out = self.forward(x)
		# self.printL(self.outputs)
		loss = (1./(2)) * np.sum((out - y) ** 2)
		self.errors = [0]*(self.len-1)
		self.errors[-1] = (self.outputs[-1]-y)*self.d_activation(self.outputs[-1])
		for i in range(len(self.errors) - 2, -1, -1):
			self.errors[i] = (np.dot(np.transpose(self.weights[i+1]),self.errors[i+1]))*self.d_activation(self.outputs[i+1]) 
		return loss

	def update(self,x,y,lr):
		loss = self.backward(x,y)
		self.errors = [0] + self.errors
		for i in range(1,self.len):
			# self.outputs[i-1] = self.outputs[i-1].reshape(self.outputs[i-1].shape[0],1)
			# self.errors[i] = self.errors[i].reshape(self.errors[i].shape[0],1)
			grads = np.dot(self.errors[i], self.outputs[i-1].transpose()) 
			self.weights[i-1] -= lr*grads
			self.biases[i-1] -= lr*np.expand_dims(self.errors[i].mean(axis=1), 1)
		return loss

	def predict(self,batch):
		return self.forward(batch)

class SparseAE (Model):
	def __init__(self,nodes,p=0.1):
		super(self,SparseAE).__init__(nodes)
		self.p = p
		self.bt_index = len(nodes)/2
		
	def backward(self,x,y):
		out = self.forward(x)
		bt_out = self.outputs[self.bt_index]
		prob = np.mean(bt_out,axis=0)
		loss = (1./(2)) * np.sum((out - y) ** 2)
		sp_loss = np.sum(self.p*np.log(self.p/prob) + (1-self.p)*np.log((1-self.p)/(1-prob)))*x.shape[1]
		self.errors = [0]*(self.len-1)
		self.errors[-1] = (self.outputs[-1]-y)*self.d_activation(self.outputs[-1])
		for i in range(len(self.errors) - 2, -1, -1):
			self.errors[i] = (np.dot(np.transpose(self.weights[i+1]),self.errors[i+1]))*self.d_activation(self.outputs[i+1]) 
		return loss,sp_loss


def save_image(w,h,imgs,f):
    n = w*h

    if len(imgs) != n:
        raise ValueError('Number of images ({}) does not match '
                         'matrix size {}x{}'.format(w, h, len(img)))


    img_h, img_w, img_c = imgs[0].shape

    imgmatrix = np.zeros((img_h * h ,
                          img_w * w ,
                          img_c),
                         np.uint8)

    imgmatrix.fill(255)    

    positions = itertools.product(range(w), range(h))
    for (x_i, y_i), img in itertools.izip(positions, imgs):
        x = x_i * (img_w)
        y = y_i * (img_h)
        imgmatrix[y:y+img_h, x:x+img_w, :] = img

    cv2.imwrite(f, imgmatrix) 







