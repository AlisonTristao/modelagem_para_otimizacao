import gurobipy as gb
from gurobipy import GRB

# model 
model = gb.Model("myModel")

# variables
facilities = {"F1", "F2", "F3", "F4", "F5"}
customer = {"C1", "C2", "C3", "C4", "C5", "C6", "C7"}

LOCATION = {"F1": 400, "F2": 500, "F3": 300, "F4": 600, "F5": 450}
CAPACITY = {"F1": 120, "F2": 150, "F3": 100, "F4": 200, "F5": 180}
DEMAND   = {"C1": 50, "C2": 40, "C3": 70, "C4": 30, "C5": 60, "C6": 45, "C7": 55}

# cost 
FACILITY = {("F1", "C1"): 4, ("F1", "C2"): 5, ("F1", "C3"): 6, ("F1", "C4"): 7, ("F1", "C5"): 8, ("F1", "C6"): 9, ("F1", "C7"): 10,
            ("F2", "C1"): 6, ("F2", "C2"): 4, ("F2", "C3"): 3, ("F2", "C4"): 5, ("F2", "C5"): 7, ("F2", "C6"): 9, ("F2", "C7"): 8,
            ("F3", "C1"): 9, ("F3", "C2"): 8, ("F3", "C3"): 7, ("F3", "C4"): 6, ("F3", "C5"): 5, ("F3", "C6"): 4, ("F3", "C7"): 3, 
            ("F4", "C1"): 5, ("F4", "C2"): 7, ("F4", "C3"): 6, ("F4", "C4"): 4, ("F4", "C5"): 3, ("F4", "C6"): 5, ("F4", "C7"): 7,
            ("F5", "C1"): 7, ("F5", "C2"): 6, ("F5", "C3"): 5, ("F5", "C4"): 4, ("F5", "C5"): 6, ("F5", "C6"): 7, ("F5", "C7"): 5} 

# variable decision
y = {}
for i in facilities:
    y[i] = model.addVar(vtype=GRB.BINARY, name=f"y_{i}")

x = {}
for i in facilities:
    for j in customer:
        x[(i, j)] = model.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}_{j}")

obj = gb.quicksum(LOCATION[i] * y[i] for i in facilities) + gb.quicksum(FACILITY[(i, j)] * x[(i, j)] for i in facilities for j in customer)
model.setObjective(obj, GRB.MINIMIZE)

# constraint
for j in customer:
    model.addConstr(
        gb.quicksum(x[(i, j)] for i in facilities) == DEMAND[j],
        name=f"suply_demand_{facilities}"
    )

for i in facilities:
    model.addConstr(
        gb.quicksum(x[(i, facilities)] for facilities in customer) <= CAPACITY[i] * y[i],
        name=f"capacity_limit_{i}"
    )

# optimize
model.optimize() 

print()

# print the solution
for i in facilities:
    if y[i].x > 0:
        print(f"build {i}")

print()

for i in facilities:
    for j in customer:
        if x[(i, j)].x > 0:
            print(f"ship {x[(i, j)].x} unitits from {i} to {j}")

print()

# calculate total cust
build_cust = sum(y[i].x * LOCATION[i] for i in facilities)
transport_cust = sum(x[(i, j)].x * FACILITY[(i, j)] for i in facilities for j in customer)
total_custo = build_cust + transport_cust

print("total cust = R$", total_custo)
print("build cust = R$", build_cust)
print("transport cust = R$", transport_cust)