"""
Concentrator location problem
Modified: 13 Feb 2022
"""
from pulp import *
import math
import matplotlib.pyplot as plt
import time
import random
start_time = time.time()
#initialization
# N = 5   #number of nodes
# roi_x = 10; #region of interest (wide)
# roi_y = 10; #region of interest (high)
beta = 10   #cost of establishing node i as a concentrator
K = 3       #concentrator capacity
P = {}
#Add (lat, long) to (x, y) here!!!
#option 1 node generation (fixed positions)
P = {1:(0,0),2:(1,3),3:(2,1),4:(3,2),5:(4,0)}
#option 2 random node generation
# for i in range(0,N):
#     x = random.randint(0, roi_x)
#     y = random.randint(0, roi_y) 
#     P[i] = (x,y) 
Np = [i for i in P.keys()]  #set of all nodes
D = {}  #D will be a dictionary whose keys are links and whose
        #values are distances, i.e. alpha ij
B = {}  #A will be a dictionary whose keys are nodes and whose
        #values are establishing costs, i.e. beta i
for i in Np:
    B[i] = beta
    for j in Np:
        tmp = math.sqrt(pow(P[i][0] - P[j][0],2) + \
                        pow(P[i][1] - P[j][1],2))
        D[(i,j)] = tmp #node separation distance
prob = LpProblem('location_problem', LpMinimize)
x = LpVariable.dicts('x', (Np, Np), 0, 1, LpInteger)
y = LpVariable.dicts('y', (Np), 0, 1, LpInteger)
#objective function
prob += lpSum(D[(i,j)]*x[i][j] for i in Np for j in Np) + \
    lpSum(B[i]*y[i] for i in Np) 
#constraints
for i in Np:
    prob += lpSum(x[i][j] for j in Np) == 1
for j in Np:
    prob += lpSum(x[i][j] for i in Np) <= K*y[j]
prob.writeLP('location_problem.lp')
prob.solve()
print ('Status:', LpStatus[prob.status])
print ('Optimal cost:', '%.2f' % value(prob.objective))
for v in prob.variables():
    print(v.name, "=", v.varValue)
#display network layout
for i in Np:
    if y[i].varValue == 1:
        plt.plot(P[i][0],P[i][1], 'ro')
    else:
        plt.plot(P[i][0],P[i][1], 'bo')
    plt.text(P[i][0], P[i][1]+0.1, '%d' % i)
    for j in Np:
        if x[i][j].varValue == 1:
            x_values = [P[i][0], P[j][0]]
            y_values = [P[i][1], P[j][1]]
            plt.plot(x_values, y_values, 'g--')
plt.grid(True)
plt.show()
#Add another network display here!!!
#runtime
print("\n** Runtime: %.2f sec **" % (time.time() - start_time))