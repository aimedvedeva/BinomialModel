import numpy as np
import math

def get_stock_prices(N, S0, u, d):
	stock_prices = np.zeros([N+1, N+1])
	for i in range(N+1):
		for j in range(N+1):
			stock_prices[j, i] = S0*(u**(i-j))*(d**j)
	return stock_prices

def get_leaves_option_values(stock_prices, N, K, is_call):
	option_values = np.zeros([N+1, N+1])
	if is_call:
		option_values[:, N] = np.maximum(np.zeros(N+1), (stock_prices[:, N] - K))
	else:
		option_values[:, N] = np.maximum(np.zeros(N+1), (K - stock_prices[:, N]))
	return option_values

def get_option_values(option_values, stock_prices, N, K, r, dt, qu, qd, is_euro_option, is_call):
	for i in np.arange(N-1, -1, -1):
		for j in range(0, i+1):
			if is_euro_option:
				option_values[j, i] = math.exp(-r*dt) * (qu*option_values[j, i+1]+qd*option_values[j+1, i+1])
			else:
				if is_call:
					option_values[j, i] = np.maximum(math.exp(-r*dt) * (qu*option_values[j, i+1]+qd*option_values[j+1, i+1]), stock_prices[j, i] - K)
				else:
					option_values[j, i] = np.maximum(math.exp(-r*dt) * (qu*option_values[j, i+1]+qd*option_values[j+1, i+1]), K - stock_prices[j, i])
	return option_values

def build_binomial_tree(N, u, d, qu, qd, dt, S0, r, K, is_call, is_euro_option):
	stock_prices = get_stock_prices(N, S0, u, d)
	option_values = get_leaves_option_values(stock_prices, N, K, is_call)
	return get_option_values(option_values, stock_prices, N, K, r, dt, qu, qd, is_call, is_euro_option)

def get_delta(option_values, S0, u, d):
    return  (option_values[0,1] -  option_values[1,1]) / (S0*u - S0*d)

def get_vega(N, u, d, qu, qd, dt, S0, r, K, is_call, is_euro_option, new_sigma, sigma):
    # build a tree with new sigma
    new_u = math.exp(new_sigma*math.sqrt(dt))
    new_d = 1./new_u                          
    new_qu = (math.exp(r*dt)-new_d)/(new_u-new_d)
    new_qd = 1-new_qu
    new_option_values = build_binomial_tree(N, new_u, new_d, new_qu, new_qd, dt, S0, r, K, is_call, is_euro_option)
    new_genuine_value = new_option_values[0,0]
    
    #build a tree with old sigma
    option_values = build_binomial_tree(N, u, d, qu, qd, dt, S0, r, K, is_call, is_euro_option)
    genuine_value = option_values[0,0]
    
    return (new_genuine_value - genuine_value) / (new_sigma - sigma)

def get_gamma(option_values, S0, u, d):
    h = 0.5*(S0*u*u - S0*d*d)
    return (((option_values[0,2]-option_values[1,2])/(S0*u*u-S0))-((option_values[1,2]-option_values[2,2])/(S0-S0*d*d)))/h

