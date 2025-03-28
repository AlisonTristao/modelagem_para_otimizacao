import gurobipy as gp
from gurobipy import GRB

model = gp.Model("transportproblem")

# Define sets
warehouses = ["A", "B", "C"]
stores = [1, 2, 3, 4]

# Define parameters
supply = {"A": 150, "B": 200, "C": 250}
demand = {1: 100, 2: 150, 3: 200, 4: 150}

# Shipping costs
costs = {
    ("A", 1): 10, ("A", 2): 12, ("A", 3): 8, ("A", 4): 11,
    ("B", 1): 13, ("B", 2): 7, ("B", 3): 14, ("B", 4): 8,
    ("C", 1): 9, ("C", 2): 14, ("C", 3): 10, ("C", 4): 12
}

# Create decision variables
shipments = {}
for i in warehouses:
    for j in stores:
        shipments[(i, j)] = model.addVar(vtype=GRB.CONTINUOUS, name=f"Ship_{i}_{j}")

'''envios = model.addVars(warehouses, stores, vtype=GRB.CONTINUOUS, name="envios")
model.update()
envios'''

# Set objective function - minimize total transportation cost
obj = gp.quicksum(costs[(i, j)] * shipments[(i, j)] for i in warehouses for j in stores)
model.setObjective(obj, GRB.MINIMIZE)

# Add supply constraints
for i in warehouses:
    model.addConstr(
        gp.quicksum(shipments[(i, j)] for j in stores) <= supply[i],
        name=f"Supply_{i}"
    )

# Add demand constraints
for j in stores:
    model.addConstr(
        gp.quicksum(shipments[(i, j)] for i in warehouses) == demand[j],
        name=f"Demand_{j}"
    )

# Solve the model
model.optimize()

# Check if optimal solution was found
if model.status == GRB.OPTIMAL:
    print(f"Optimal total transportation cost: ${model.objVal:.2f}")
    
    # Print optimal shipping plan
    print("\nOptimal Shipping Plan:")
    print("-" * 50)
    print(f"{'From':<10}{'To':<10}{'Units':<10}{'Cost/Unit':<10}{'Total Cost':<10}")
    print("-" * 50)
    
    total_units = 0
    for i in warehouses:
        for j in stores:
            if shipments[(i, j)].x > 0.001:  # Small tolerance to handle floating-point errors
                units = shipments[(i, j)].x
                unit_cost = costs[(i, j)]
                total_cost = units * unit_cost
                total_units += units
                print(f"{i:<10}{j:<10}{units:<10.1f}${unit_cost:<9.2f}${total_cost:<9.2f}")
    
    print("-" * 50)
    print(f"Total units shipped: {total_units}")
    
    # Print warehouse utilization
    print("\nWarehouse Utilization:")
    for i in warehouses:
        used = sum(shipments[(i, j)].x for j in stores)
        utilization = (used / supply[i]) * 100
        print(f"Warehouse {i}: {used:.1f}/{supply[i]} units ({utilization:.1f}%)")
        
    # Print shadow prices for demand constraints
    print("\nMarginal Value of Additional Demand:")
    for j in stores:
        constr_name = f"Demand_{j}"
        constr = model.getConstrByName(constr_name)
        print(f"Store {j}: ${constr.Pi:.2f} per additional unit")
        
else:
    print(f"Optimization was not successful. Status code: {model.status}")