from pulp import *
import pandas as pd
import mapper
import csv

# Get system metadata
all_paths, low_level_auths = mapper.calc_system_metadata('system_graph.csv', 'rebac_policy.txt')

# Get the dict comprising only the non-permitted access requests and their relationship patterns
non_permitted_paths = {k:v for k, v in all_paths.items() if k not in low_level_auths}
other_values = set().union(*(non_permitted_paths.values()))

# Calculate the permit subsets used for the first sub-optimization
cover1 = {'permits': list(low_level_auths)}
cover1.update({'u1': list(all_paths[k] - other_values for k in low_level_auths)})
# print(cover1, "\n")

# Calculate non-permitted patterns covered by permits
cover1ToU2 = {'permits': list(low_level_auths)}
cover1ToU2.update({'u2': list(all_paths[k].intersection(other_values) for k in low_level_auths)})
# print(cover1ToU2, "\n")

# Calculate the deny subsets
cover2 = {'denies': list(non_permitted_paths.keys())}
cover2.update({'u2': list(non_permitted_paths.values())})
# print(cover2, len(cover2['denies']), len(cover2['u2']), "\n")

# Calculate universes for optimization problems
u1 = set().union(*cover1['u1'])
# print(u1, "\n")

u2 = set().union(*cover1ToU2['u2'])
# print(u2, "\n")

# Convert to DataFrames
df1 = pd.DataFrame(cover1)
df2 = pd.DataFrame(cover2)
df3 = pd.DataFrame(cover1ToU2)

# Create the optimization problem
prob = LpProblem("MinLLACBC", LpMinimize)

# Create variables
xp = LpVariable.dicts("p", df1.index, cat='Binary')
xd = LpVariable.dicts("d", df2.index, cat='Binary')
z = LpVariable.dicts("u2", u2, cat='Binary')

# Print number of variables
print('Number of variables = ', len(xp) + len(xd) + len(z))

# Objective function
# Primary objective: Minimize total number of denies
# Secondary objective: Minimize total number of permits (with lower weight)
prob += lpSum(xd[j] for j in df2.index) + 0.01 * lpSum(xp[i] for i in df1.index)

# Coverage constraints for permits
# Every pattern in u1 should be covered by exactly 1 permit request
for rel_patt in u1:
    prob += lpSum(xp[i] for i in df1.index if rel_patt in df1.loc[i, 'u1']) == 1

# Determine what elements in u2 to consider based on selected permit requests
for rel_patt in u2:
    # z >= x_i for all i
    for i in df3.index:
        if rel_patt in df3.loc[i, 'u2']:
            prob += z[rel_patt] >= xp[i]
    # z <= sum(x)
    prob += z[rel_patt] <= lpSum(xp[i] for i in df3.index if rel_patt in df3.loc[i, 'u2'])

# Coverage constraints for denies
# Every chosen pattern in u2 should be covered by at least 1 deny request
for rel_patt in u2:
    prob += lpSum(xd[j] for j in df2.index if rel_patt in df2.loc[j, 'u2']) >= z[rel_patt]

# Print number of constraints
print('Number of constraints =', len(prob.constraints))

# Solve using HiGHS solver
status = prob.solve(solver=HiGHS(timeLimit=3600)) # Remove msg=0 to show the compute logs

# Store the results
A_min = [('User', 'Resource', 'Decision')]

# Print solution
if LpStatus[status] == 'Optimal':
    print('Solution:')
    print('Objective value =', value(prob.objective))
    
    # Get permits
    for i in df1.index:
        if value(xp[i]) > 0.5:  # Using 0.5 threshold for binary variables
            print(df1.loc[i, 'permits'])
            A_min.append((*df1.loc[i, 'permits'], 'Permit'))
    
    # Get denies
    for j in df2.index:
        if value(xd[j]) > 0.5:  # Using 0.5 threshold for binary variables
            print(df2.loc[j, 'denies'])
            A_min.append((*df2.loc[j, 'denies'], 'Deny'))
else:
    print('The problem does not have an optimal solution.')

# Write results to CSV
# print(A_min)
with open('min_low_level_auths.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(A_min)