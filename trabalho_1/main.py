import numpy as np

# Small test cases
# Test Case 1: Simple example from the problem statement
test_case_1 = {
    "n": 5,
    "budget": 10,
    "energy": [3, 5, 1, 7, 4],
    "cost": [2, 3, 1, 5, 4]
}

# Test Case 2: All houses have same energy and cost
test_case_2 = {
    "n": 6,
    "budget": 9,
    "energy": [3, 3, 3, 3, 3, 3],
    "cost": [2, 2, 2, 2, 2, 2]
}

# Test Case 3: Budget only allows one expensive house
test_case_3 = {
    "n": 4,
    "budget": 10,
    "energy": [2, 20, 3, 15],
    "cost": [1, 10, 2, 9]
}

# Test Case 4: Houses with varying cost-to-energy ratios
test_case_4 = {
    "n": 7,
    "budget": 15,
    "energy": [4, 8, 10, 2, 6, 5, 9],
    "cost": [5, 3, 7, 1, 5, 3, 6]
}

# Test Case 5: Exactly adjacent high-value houses (forces a choice)
test_case_5 = {
    "n": 3,
    "budget": 20,
    "energy": [5, 15, 5],
    "cost": [5, 10, 5]
}

# Larger test cases
import random

# Seed for reproducibility
random.seed(42)

# Test Case 6: Medium neighborhood (20 houses)
n_6 = 20
test_case_6 = {
    "n": n_6,
    "budget": 50,
    "energy": [random.randint(5, 15) for _ in range(n_6)],
    "cost": [random.randint(3, 8) for _ in range(n_6)]
}

# Test Case 7: Large neighborhood (50 houses)
n_7 = 50
test_case_7 = {
    "n": n_7,
    "budget": 100,
    "energy": [random.randint(10, 30) for _ in range(n_7)],
    "cost": [random.randint(5, 15) for _ in range(n_7)]
}

# Test Case 8: Pattern of alternating high/low energy houses
n_8 = 30
energy_8 = []
for i in range(n_8):
    if i % 2 == 0:
        energy_8.append(20) # High energy on even houses
    else:
        energy_8.append(5)  # Low energy on odd houses

test_case_8 = {
    "n": n_8,
    "budget": 80,
    "energy": energy_8,
    "cost": [random.randint(5, 10) for _ in range(n_8)]
}

# Test Case 9: Decreasing energy/cost ratio
n_9 = 25
energy_9 = [30 - i for i in range(n_9)] # Decreasing energy
cost_9 = [5 + i//2 for i in range(n_9)] # Increasing cost

test_case_9 = {
    "n": n_9,
    "budget": 70,
    "energy": energy_9,
    "cost": cost_9
}

# Test Case 10: Very tight budget constraint
n_10 = 40
test_case_10 = {
    "n": n_10,
    "budget": 30, # Very tight budget
    "energy": [random.randint(5, 25) for _ in range(n_10)],
    "cost": [random.randint(5, 10) for _ in range(n_10)]
}

# Test Case 11: Large scale challenge (100 houses with complex patterns)
n_11 = 100
# Create a pattern with clusters of high-energy houses separated by low-energy houses
energy_11 = []
for i in range(n_11):
    if (i % 7 == 0) or (i % 7 == 1) or (i % 7 == 2):
        energy_11.append(random.randint(20, 30)) # High energy cluster
    else:
        energy_11.append(random.randint(5, 15))  # Low energy houses

cost_11 = []
for i in range(n_11):
    if i < n_11 // 3:  # First third: higher energy = higher cost
        cost_factor = energy_11[i] / 30
        cost_11.append(int(5 + cost_factor * 15))
    elif i < 2 * (n_11 // 3):  # Middle third: random costs
        cost_11.append(random.randint(5, 20))
    else:  # Last third: higher energy = lower cost
        cost_factor = 1 - (energy_11[i] / 30)
        cost_11.append(int(5 + cost_factor * 15))

test_case_11 = {
    "n": n_11,
    "budget": 200,
    "energy": energy_11,
    "cost": cost_11
}

def calculate_optimal_values(teste_case):
    # gama matrix n x budget
    # +1 for 0 budget - index coincide with the rest budget
    gama_matrix = np.zeros((teste_case["n"], teste_case["budget"] + 1), dtype=np.int32)
    n = teste_case["n"]

    for i in range(n):
        # energy and cost of the i-th item
        energy = teste_case["energy"][i] 
        cost = teste_case["cost"][i]

        # fill the gama matrix
        for j in range(teste_case["budget"] + 1):
            # if the budget is less than the cost of the i-th item
            if j < cost:
                value = 0
        
            else:
                value = energy 
                rest = j - cost
                # get the best value of the previous items
                if i > 1:
                    value += gama_matrix[i-2][rest]

            gama_matrix[i][j] = max(value, gama_matrix[i-1][j])

    return gama_matrix

def get_result_of_gama_matrix(case, gama, budget=-1, item=-1):
    # initial budget
    budget = case["budget"]
    item = []

    for i in range(case["n"]-1, -1, -1):
        # if the last item was add
        if item and item[-1] == i + 1:
            continue
        
        # verify the optimal of the rest budget
        rest = budget - case["cost"][i]
        optimal_rest = gama[i-2][rest] if i > 1 else 0
        optimal_local = gama[i][budget]

        # if the optimal of the rest budget is equal to the optimal of the local
        if optimal_local - case["energy"][i] == optimal_rest:
            budget -= case["cost"][i]
            item.append(i)

    return np.sort(np.array(item))

case = test_case_11
gama = calculate_optimal_values(case)
items = get_result_of_gama_matrix(case, gama)

print(gama)
print(items, gama[-1][-1])