# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 15:18:48 2020

@author: yeapym
"""

from itertools import product
from math import sqrt
from ortools.linear_solver import pywraplp

# import gurobipy as gp
# from gurobipy import GRB

# tested with Gurobi v9.0.0 and Python 3.7.0

#%% Parameter initialization
file = open("./data/problem_1.txt")
input_data = file.read()
# print(input_data)
file.close()
# parse the input
lines = input_data.split('\n')

parts = lines[0].split()
num_facilities = int(parts[0])
num_customers = int(parts[1])

facilities = []
setup_cost = []
cap_faci = []
for i in range(1, num_facilities+1):
    parts = lines[i].split()
    setup_cost.append(float(parts[0]))
    cap_faci.append(int(parts[1]))
    facilities.append([float(parts[2]), float(parts[3])])

customers = []
dem_cust = []
for i in range(num_facilities+1, num_facilities+1+num_customers):
    parts = lines[i].split()
    dem_cust.append(int(parts[0]))
    customers.append([float(parts[1]), float(parts[2])])
    
cost_per_mile = 1

# This function determines the Euclidean distance between a facility and customer sites.

def compute_distance(loc1, loc2):
    dx = loc1[0] - loc2[0]
    dy = loc1[1] - loc2[1]
    return sqrt(dx*dx + dy*dy)

# Compute key parameters of MIP model formulation
cartesian_prod = list(product(range(num_customers), range(num_facilities)))

# Compute shipping costs
cost = {}
for c, f in cartesian_prod:
    cost[(c,f)] = cost_per_mile*compute_distance(customers[c], facilities[f])

# # MIP  model formulation
#%% OR-Tools initialization
solver = pywraplp.Solver.CreateSolver('SCIP')
solver.SetTimeLimit(500*1000)
infinity = solver.infinity()

#%% Decision variables
# Decide which facility should open
xw = {}
for i in range(num_facilities):
    xw[i] = solver.IntVar(0, 1, 'xw[%d]' % i)

# Decide which customer the facility is to serve
ycw = {}
for i, j in cartesian_prod:
    ycw[(i, j)] = solver.IntVar(0, 1, 'ycw[(%d,%d)]' % (i,j))

#%% Objective
# Minimize the cost of opening the facilities and shipping cost
total_cost = solver.Sum([xw[w]*setup_cost[w] for w in range(num_facilities)]) + solver.Sum(ycw[c,w]*cost[c,w] for c in range(num_customers) for w in range(num_facilities))
solver.Minimize(total_cost)

#%% Constraints
# The number of customer served should be within the facility's capacity
for w in range(num_facilities):
    solver.Add(solver.Sum([ycw[(c,w)]*dem_cust[c] for c in range(num_customers)]) <= xw[w]*cap_faci[w])

# All customers must have ONE facility 
for c in range(num_customers):
    solver.Add(solver.Sum([ycw[(c,w)] for w in range(num_facilities)]) == 1)

#%% Solve
print('Number of variables = %d' % solver.NumVariables())
print('Number of constraints = %d' % solver.NumConstraints())    
status = solver.Solve()
assert solver.VerifySolution(1e-5, True)
if status in [0, 1]:
    if status == 0:
        print('Optimum solution is found.')
    else:
        print('Feasibile solution is found.')
    print('Objective value =', solver.Objective().Value())
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
    print('Problem solved in %d iterations' % solver.iterations())
    solution = {}
    for w in range(num_facilities):
        solution[w] = []
        for c in range(num_customers):
            if ycw[(c,w)].solution_value() >= 1e-4:
                solution[w].append(c)
    
    # print("Build at location:")
    # # cust = 1
    # for i in range(num_facilities):
    #     if not solution[i]:
    #         continue
    #     else:
    #         print('Facility', i, 'serves custormers')
    #         print([j+1 for j in solution[i]])
            
