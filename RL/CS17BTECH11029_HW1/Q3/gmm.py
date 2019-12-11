import numpy as np 
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser(description='Expectation maximization')

parser.add_argument('--k', type=int,default=2,help= 'Number of mixtures')
parser.add_argument('--d', type=int,default=1,help= 'Dimension of input')
parser.add_argument('--iterations', type=int,default=100.,help= 'Stopping threshold for pi')
parser.add_argument('--points', type=int,default=10000,help= 'number of points')
parser.add_argument('--input', type=str,default=None,help= 'Input file .npy required (n,d) shape')

args = parser.parse_args()

def multivariate_normal(x, d, mean, covariance):
    """pdf of the multivariate normal distribution."""
    x_m = x - mean
    return (1. / (np.sqrt((2 * np.pi)**d * np.linalg.det(covariance))) * 
            np.exp(-(np.linalg.solve(covariance, x_m).T.dot(x_m)) / 2))

class GMM(): 
    def __init__(self,pi,mu,sig,k,d):
    	self.k = k
    	self.pi = pi
    	self.mu = mu
    	self.sig = np.asarray([np.diag(sig[i]) for i in range(k)])

    	
    def sample(self, size=1): 
    	mixture = np.random.choice(self.k,p=self.pi,size=size) # randomly choose a mixture with probability pi_k
    	data = np.asarray([np.random.multivariate_normal(self.mu[i],self.sig[i]) for i in mixture]) # sample x from that distribution
    	return data

def mle(data,k,d):

	gamma = np.random.uniform(0,1,size=(k,data.shape[0])) # initialize posteriors
	mu = np.random.uniform(-10,10,size=(k,d)) # initiale means
	sig = np.asarray([np.diag(np.random.uniform(1,2,size=d)) for i in range(k)]) # initialze variances
	iterations = args.iterations

	while iterations>0 :
		nk = np.sum(gamma,axis=1,keepdims=True) # find N_k
		mu = np.matmul(gamma,data)/nk # update means
		for i in range(k): # update variances
			sig[i] = np.matmul(gamma[i]*(data-mu[i]).transpose(),data-mu[i])/nk[i]
		pi = nk/data.shape[0] # update probabilities pi_k

		for j in range(data.shape[0]): # update gamma
			pdfs = [pi[i]*multivariate_normal(data[j],d,mu[i],sig[i]) for i in range(k)]
			pdf_sum = np.sum(pdfs)
			for i in range(k):
				gamma[i,j] = pdfs[i]/pdf_sum
		iterations-=1

	return pi[:,0],mu,sig


if args.input is None: # if input is not provided then sample from a random mixture
	pi = np.random.randint(0,10,size=args.k)
	pi = pi/np.sum(pi,dtype=float)
	params = dict( pis = pi,
			  	   mu = np.random.uniform(-10,10,size=(args.k,args.d)),
			  	   sig = np.random.uniform(1,2,size=(args.k,args.d)))
	print(params)
	gs = GMM(params['pis'],params['mu'],params['sig'],args.k,args.d) 
	data = gs.sample(size=args.points)
	np.save('./input.npy',data)
else:
	data = np.load(args.input) # load the input file

pi,mu,sig = mle(data,args.k,args.d) # find MLE
sig = np.asarray([np.diagonal(sig[i]) for i in range(args.k)])

params_e = dict( pis = pi,
			  	   mu = mu,
			  	   sig = sig)

print(params_e)
mle_gs = GMM(pi,mu,sig,args.k,args.d) 
mle_data = mle_gs.sample(size=args.points) # generate estimated data

plt.figure(figsize=(10,10))
plt.subplot(2, 1, 1)
count, bins, ignored = plt.hist(data, 30)
plt.title('Actual data')

plt.subplot(2, 1, 2)
count, bins, ignored = plt.hist(mle_data, 30)
plt.title('Estimated data')

plt.savefig('gmm.jpg') # save plots