"""
Concentrator connection problem
Modified: 13 Feb 2022
"""
from pulp import *
import math
import matplotlib.pyplot as plt
import time
import random
start_time = time.time()
#initialization
P = {}
# N = 5   #number of nodes
#Option 1 node generation (fixed positions)
P = {1:(0,0),2:(1,3),3:(2,1),4:(3,2),5:(4,0)}
#Option 2 random node generation
# for i in range(1,N+1):
#     x = random.randint(0, 5)
#     y = random.randint(0, 5) 
#     P[i] = (x,y)
Np = [i for i in P.keys()]  #set of all nodes
def powerset(fullset):
  listsub = list(fullset)
  subsets = []
  for i in range(2**len(listsub)):
    subset = []
    for k in range(len(listsub)):            
      if i & 1<<k:
        subset.append(listsub[k])
    subsets.append(subset)        
  return subsets
subsets = powerset(set(Np)) #power set of Np
S = [subsets[i] for i in range(len(subsets))]
S.remove([])  #non-empty subset of nodes
E = [S[i] for i in range(len(S)) if len(S[i]) == 2]  #edge set
C = {}  #C will be a dictionary whose keys are links and whose
        #values are link costs (distances)
for i in range(len(E)):
    P1 = P[E[i][0]]
    P2 = P[E[i][1]]
    tmp = math.sqrt(pow(P2[0] - P1[0],2) + pow(P2[1] - P1[1],2))
    C[(i)] = tmp
prob = LpProblem('connection_problem', LpMinimize)
x = LpVariable.dicts('x', range(len(E)), 0, 1, LpInteger)
#objective function
prob += lpSum(C[(i)]*x[i] for i in range(len(E))) 
#constraints
prob += lpSum(x[i] for i in range(len(E))) == len(Np) - 1 #N-1 edges in Tree

prob.writeLP('connection_problem.lp')
prob.solve()
print ('Status:', LpStatus[prob.status])
print ('Optimal cost:', '%.2f' % value(prob.objective))
for v in prob.variables():
    print(v.name, "=", v.varValue)
#display network layout
for i in Np:
    plt.plot(P[i][0],P[i][1], 'ro')
    plt.text(P[i][0], P[i][1]+0.1, '%d' % i)
for j in range(len(E)):
    if x[j].varValue == 1:
        Pt1 = P[E[j][0]]
        Pt2 = P[E[j][1]]
        x_values = [Pt1[0], Pt2[0]]
        y_values = [Pt1[1], Pt2[1]]
        plt.plot(x_values, y_values, 'g--')
        plt.text((Pt1[0]+Pt2[0])/2, (Pt1[1]+Pt2[1])/2, \
                 '%.2f' % C[(j)], color = 'r')
plt.grid(True)
plt.show()
#runtime
print("\n** Runtime: %.2f sec **" % (time.time() - start_time))