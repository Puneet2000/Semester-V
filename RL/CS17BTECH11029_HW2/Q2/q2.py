import h5py
import numpy as np
from model import *
import argparse
parser = argparse.ArgumentParser(description='Multi-layer perceptron')

parser.add_argument('--layers', nargs='+', type=int,default=[784,512,256,128,256,512,784])
parser.add_argument('--epochs', type=int,default=2000)
parser.add_argument('--batch_size', type=int,default=256)
parser.add_argument('--resume', type=int,default=-1)
args = parser.parse_args()
print(args)
def lr(epoch): # learnin rate scheduler
	if epoch in range(0,500):
		return 0.01
	elif epoch in range(500,1000):
		return 0.001
	else:
		return 0.0001
MNIST_data = h5py.File("../mnist.hdf5", 'r') # load data

x_train = np.float32(MNIST_data['x_train'][:])
print(x_train.shape)
x_test  = np.float32(MNIST_data['x_train'][:256])
MNIST_data.close()

test = x_test.reshape(-1,28,28,1)*255. # test images
save_image(16,16,test,'./original.png')

batch_size=args.batch_size
epochs=args.epochs
model = Model([784,512,256,128,256,512,784])
if args.resume >=0: # load pretrained model
	ckpt = np.load('./weights/{}.npy'.format(args.resume),allow_pickle=True).item()
	model.weights = ckpt['weights']
	model.biases = ckpt['biases']
for i in range(epochs):
	avg_loss = 0.
	for j in range(0,len(x_train),batch_size): # sample batch
		batch =  x_train[j:j+batch_size,:].transpose() if j+batch_size <= len(x_train) else x_train[j:,:].transpose()
		loss = model.update(batch,batch,lr(i))
		avg_loss += loss

	x_test_r = model.predict(x_test.transpose()).transpose()
	test_r = x_test_r.reshape(-1,28,28,1)*255.
	save_image(16,16,test_r,'./reconstructed.png') # reconstruct image forn evaluation
	print('Epoch {}, Loss : {:3f}'.format(i,avg_loss/len(x_train)))
	if i%50 ==0 or i == epochs-1: # save weights
		np.save('./weights/{}.npy'.format(i),{'weights': model.weights, 'biases': model.biases})