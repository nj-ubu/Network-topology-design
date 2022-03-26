"""
Minimum Spanning Tree: Kruskal algorithm

The code (Kruskal algorithm) is contributed/originated by Neelam Yadav
Link: https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/

Modified for topology design problem: 17 Mar 2022
"""
import math
import matplotlib.pyplot as plt
import time
import random
from collections import defaultdict
start_time = time.time()
# Class to represent a graph
class Graph:

	def __init__(self, vertices):
		self.V = vertices # No. of vertices
		self.graph = [] # default dictionary
		# to store graph

	# function to add an edge to graph
	def addEdge(self, u, v, w):
		self.graph.append([u, v, w])

	# A utility function to find set of an element i
	# (uses path compression technique)
	def find(self, parent, i):
		if parent[i] == i:
			return i
		return self.find(parent, parent[i])

	# A function that does union of two sets of x and y
	# (uses union by rank)
	def union(self, parent, rank, x, y):
		xroot = self.find(parent, x)
		yroot = self.find(parent, y)

		# Attach smaller rank tree under root of
		# high rank tree (Union by Rank)
		if rank[xroot] < rank[yroot]:
			parent[xroot] = yroot
		elif rank[xroot] > rank[yroot]:
			parent[yroot] = xroot

		# If ranks are same, then make one as root
		# and increment its rank by one
		else:
			parent[yroot] = xroot
			rank[xroot] += 1

	# The main function to construct MST using Kruskal's
		# algorithm
	def KruskalMST(self):

		result = [] # This will store the resultant MST
		
		# An index variable, used for sorted edges
		i = 0
		
		# An index variable, used for result[]
		e = 0

		# Step 1: Sort all the edges in
		# non-decreasing order of their
		# weight. If we are not allowed to change the
		# given graph, we can create a copy of graph
		self.graph = sorted(self.graph,
							key=lambda item: item[2])

		parent = []
		rank = []

		# Create V subsets with single elements
		for node in range(self.V):
			parent.append(node)
			rank.append(0)

		# Number of edges to be taken is equal to V-1
		while e < self.V - 1:

			# Step 2: Pick the smallest edge and increment
			# the index for next iteration
			u, v, w = self.graph[i]
			i = i + 1
			x = self.find(parent, u)
			y = self.find(parent, v)

			# If including this edge does't
			# cause cycle, include it in result
			# and increment the indexof result
			# for next edge
			if x != y:
				e = e + 1
				result.append([u, v, w])
				self.union(parent, rank, x, y)
			# Else discard the edge

		minimumCost = 0
		print ("Edges in the constructed MST")
		for u, v, weight in result:
			minimumCost += weight
			print("%d -- %d == %.2f" % (u, v, weight))
		print("MST cost: %.2f" % minimumCost)
        
#initialization
P = {}
# N = 5   #number of nodes
#Option 1 node generation (fixed positions)
P = {0:(0,0),1:(1,3),2:(2,1),3:(3,2),4:(4,0)}
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

# Driver code
g = Graph(len(Np))
for i in range(len(E)):
    g.addEdge(E[i][0], E[i][1], C[i])

# Function call
g.KruskalMST()

# display network layout/map
for i in Np:
    plt.plot(P[i][0],P[i][1], 'ro')
    plt.text(P[i][0], P[i][1]+0.1, '%d' % i)
plt.grid(True)
plt.show()
# Add\plot active edges from the above algorithm

#runtime
print("\n** Runtime: %.2f sec **" % (time.time() - start_time))