import numpy as np 
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Maximul Likelihood estimation')

parser.add_argument('--dist', type=str,help='distribution')
parser.add_argument('--points', type=int,default=20000,help= 'MLE estimator')

args = parser.parse_args()

class MLE:
	def __init__(self, data):
		self.data = data
		self.params = []
		self.num_points = args.points

	def estimate(self):
		pass
	def plot(self):
		pass

class Binomial(MLE):
	def estimate(self):
		p_ =  np.mean(self.data)/10
		assert p_>=0 and p_<=1 , 'Negative parameter found, positive expected'
		self.params.append(p_)

	def plot(self):
		return np.random.binomial(10,self.params[0], self.num_points)

class Poisson(MLE):
	def estimate(self):
		lambda_ =  np.mean(self.data)
		assert lambda_>0 , 'Negative parameter found, positive expected'
		self.params.append(lambda_)

	def plot(self):
		return np.random.poisson(self.params[0], self.num_points)

class Exponential(MLE):
	def estimate(self):
		theta_ =  np.mean(self.data)
		self.params.append(theta_)

	def plot(self):
		return np.random.exponential(self.params[0], self.num_points)

class Gaussian(MLE):
	def estimate(self):
		mean_ =  np.mean(self.data)
		std_ =  np.std(self.data)
		self.params.append(mean_)
		self.params.append(std_)

	def plot(self):
		return np.random.normal(self.params[0], self.params[1], self.num_points)

class Laplacian(MLE):
	def estimate(self):
		alpha_ =  np.median(self.data)
		beta_ =  np.mean(np.abs(self.data-alpha_))
		self.params.append(alpha_)
		self.params.append(beta_)

	def plot(self):
		return np.random.laplace(self.params[0], self.params[1], self.num_points)

num_points = args.points
actual_params = []
if args.dist == 'binomial':
	actual_params.append(np.random.uniform(0,1))
	data = np.random.binomial(10,actual_params[0], num_points)
	mle = Binomial(data)
elif args.dist == 'poisson':
	actual_params.append(np.random.randint(1,100))
	data = np.random.poisson(actual_params[0], num_points)
	mle = Poisson(data)
elif args.dist == 'exponential':
	actual_params.append(np.random.randint(1,100))
	data = np.random.exponential(actual_params[0], num_points)
	mle = Exponential(data)
elif args.dist == 'gaussian':
	actual_params.append(np.random.randint(1,100))
	actual_params.append(np.random.randint(1,100))
	data = np.random.normal(actual_params[0], actual_params[1], num_points)
	mle =Gaussian(data)
elif args.dist == 'laplacian':
	actual_params.append(np.random.randint(1,100))
	actual_params.append(np.random.randint(1,100))
	data = np.random.laplace(actual_params[0], actual_params[1], num_points)
	mle = Laplacian(data)

print('Actual Parameters are : ', actual_params)
mle.estimate()
print('Estimated Parameters are : ', mle.params)
mle_data = mle.plot()
plt.figure(figsize=(10,10))
plt.subplot(2, 1, 1)
count, bins, ignored = plt.hist(data, 30)
plt.title('Actual data : {}'.format(actual_params))

plt.subplot(2, 1, 2)
count, bins, ignored = plt.hist(mle_data, 30)
plt.title('Estimated data : {}'.format(mle.params))

plt.savefig('{}.jpg'.format(args.dist))