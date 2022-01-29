import math
from BM import build_binomial_tree
from BM import get_delta
from BM import get_vega
from BM import get_gamma

#Вход:
#S0             initial stock price
#K              strike price
#r              risk free interest rate per year
#T              length of option in years
#sigma          volatility of the stock
#is_call        is it a call option
#is_euro_option is it an european option 
#N              number of binomial iterations, N+1 - number of nodes in the tree    
S0 = 50          
K = 50             
r = 0.1           
T = 0.4167           
sigma = 0.4         
is_call = False    
is_euro_option = False
N = 50              

dt = T/float(N) 
u = math.exp(sigma*math.sqrt(dt))  #factor change of upstate
d = 1./u                           #factor change of downstate
qu = (math.exp(r*dt)-d)/(u-d)      #risk free upstate probability
qd = 1-qu                          #risk free downstate probability

option_values = build_binomial_tree(N, u, d, qu, qd, dt, S0, r, K, is_call, is_euro_option)
genuine_value = option_values[0,0]
print('option value=',genuine_value)

delta = get_delta(option_values, S0, u, d)
print('delta=',delta)

new_sigma = 0.5
vega = get_vega(N, u, d, qu, qd, dt, S0, r, K, is_call, is_euro_option, new_sigma, sigma)
print('vega=',vega)

gamma = get_gamma(option_values, S0, u, d)
print('gamma=',gamma)
