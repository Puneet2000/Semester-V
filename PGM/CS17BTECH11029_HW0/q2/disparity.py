import numpy as np 
import scipy.misc as misc
from PIL import Image
img1 = np.asarray(Image.open('HW0-left-gray.png').convert('L')).astype(np.float64)
img2 = np.asarray(Image.open('HW0-right-gray.png').convert('L')).astype(np.float64)

# intialize variables
h,w = img1.shape[0], img1.shape[1]
sigma = 1.
gamma = 2.
delta = 10.
beliefs = np.zeros((h,w,10))

# define neighbours
def neighbours(i,j):
	raw = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
	return [ (a,b) for (a,b) in raw if (0<=a and a<w and 0<=b and b<h) ]

def neighbours_(i1,j1,i2,j2):
	n1 =  neighbours(i1,j1)
	n2 = neighbours(i2,j2)

	return [a for a in n1 if a not in n2]

#initialize messages
msg = {}
for i in range(h):
	for j in range(w):
		for i2,j2 in neighbours(i,j):
			msg[(i,j,i2,j2)] = np.random.uniform(-1,1,10)

# datacost function
def datacost(i,j,d):
	diff = (img1[i,j] - img2[min(i+d,w-1),j])**2
	return np.exp(-diff/(2*sigma*sigma))

def smoothcost(ds,dt):
	q = min((ds-dt)**2, delta**2)
	return np.exp(-q/(2*gamma*gamma))

def normalize():
	for i in msg:
		msg[i] = msg[i]/(np.sum(msg[i]) + 1e-10)

# one LBF iteration
def lbf():
	normalize()
	for i1 in range(h):
		for j1 in range(w):
			for (i2,j2) in neighbours(i1,j1):
				for l in range(10):
					msg[(i1,j1,i2,j2)][l] = 0.
					for l_ in range(10):
						cost  = datacost(i1,j1,l_)*smoothcost(l,l_)
						for (a,b) in neighbours_(i1,j1,i2,j2):
							cost *= msg[(a,b,i1,j1)][l_]
						msg[(i1,j1,i2,j2)][l] += cost


# find beliefs
def update_belief():
	for i in range(h):
		for j in range(w):
			for l in range(10):
				beliefs[i,j,l] = datacost(i,j,l)
				for (a,b) in neighbours(i,j):
					beliefs[i,j,l] *= msg[a,b,i,j][l]

# Run the code
for iter in range(100):
	lbf()
	update_belief()
	dimg = 28.33*np.argmax(beliefs,axis=2)
	print(dimg)
	# dimg = np.zeros((256,256))
	dimg = Image.fromarray(dimg).convert('L')
	dimg.save('output.png')
