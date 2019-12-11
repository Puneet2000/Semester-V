from model import *
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Multi-layer perceptron')

parser.add_argument('--layers', nargs='+', type=int)
parser.add_argument('--func', type=str,default='xor')
parser.add_argument('--epochs', type=int,default=1000)
parser.add_argument('--batch_size', type=int,default=256)
parser.add_argument('--threshold', type=float,default=0.5)
parser.add_argument('--noise', action='store_true')
args = parser.parse_args()
print(args)

data = []
labels = []
for i in range(np.power(2,args.layers[0])): # generate data and labels
	x = [float(j) for j in np.binary_repr(i,width=args.layers[0])]
	if args.func == 'xor': # odd ones
		label = float(x.count(1.)%2 == 1)
	elif args.func == 'and': # all ones
		label = float(sum(x)==args.layers[0])
	elif args.func == 'or': # at least one 1.
		label = float(1. in x)
	data.append(np.asarray(x))
	labels.append(label)

orig_data  = np.asarray(data)
orig_labels = np.asarray(labels).reshape(-1,1)

if args.noise: # add nosie
	for i in range(np.power(2,args.layers[0])):
		data[i] += np.random.normal(0.,0.01**0.5,data[i].shape)
		labels[i] += np.random.normal(0.,0.01**0.5)

data = np.asarray(data)
labels = np.asarray(labels).reshape(-1,1)
print(data,labels)

model = Model(args.layers)
for i in range(args.epochs):
	avg_loss = 0.
	for j in range(0,len(data),args.batch_size): # extract batch
		batch =  data[j:j+args.batch_size,:].transpose() if j+args.batch_size <= len(data) else data[j:,:].transpose()
		label =  labels[j:j+args.batch_size,:].transpose() if j+args.batch_size <= len(labels) else labels[j:,:].transpose()
		loss = model.update(batch,label,0.1)
		avg_loss += loss
	print('Epoch {},Loss : {:3f}'.format(i,avg_loss/len(data)))

prob = model.predict(orig_data.transpose()).transpose() # print accuracy
predict = prob>=args.threshold
correct = (predict==orig_labels).sum()
print('Accuracy : ',100.*correct/labels.shape[0])