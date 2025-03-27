import gurobipy as gp
from gurobipy import GRB

# Create a new model
model = gp.Model("aula_1")

# Create variables
tables = model.addVar(vtype=GRB.CONTINUOUS, name="tables")
chairs = model.addVar(vtype=GRB.CONTINUOUS, name="chairs")

# update
model.update()

# Set objective
model.setObjective(70*tables + 50*chairs, GRB.MAXIMIZE)

# Add constraint
model.addConstr(4 * tables + 3 * chairs <= 240, "CarpentryTime")
model.addConstr(2 * tables + 1 * chairs <= 100, "FinishingTime")
model.addConstr(tables >= 0, "NonNegativityTables")
model.addConstr(chairs >= 0, "NonNegativityChairs")

# solve the model
model.optimize()

print("Optimal solution")
print("Tables: ", tables.x)
print("Chairs: ", chairs.x)
print("Optimal value: ", model.objVal)

# Sensitivity analysis
for constr in model.getConstrs():
    if constr.Sense == '<':  # Only for less-than constraints
        print(f"{constr.ConstrName}: Shadow price = {constr.Pi:.2f}")