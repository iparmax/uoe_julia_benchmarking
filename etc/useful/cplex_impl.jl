using JuMP,MathOptInterface;
using CPLEX;

# Consult https://www.ibm.com/docs/en/icos/12.9.0?topic=cplex-list-parameters 
# JuMP takes parameters as input from the C API

# Reading the model
#model = read_from_file("test_cases\\examples\\lp.mps");
model = read_from_file("test_cases\\examples\\milp.mps");

# Setting CPLEX as optimizer
set_optimizer(model,CPLEX.Optimizer);

### Set Number of Thread used ###

# Through MOI for Gurobi,Xpress,CPLEX
MOI.set(model, MOI.NumberOfThreads(), 16)

### Set Algorithm used ###

# Options are: 
# 0 Automatic, 1 Primal Simplex. 2 Dual Simplex
# 3 Network simplex, 4 Barrier,
# 5 Sifting, 6 Concurrent

# The Following applies for the root of B&B and single LP
set_optimizer_attribute(model, "CPXPARAM_LPMethod", 1)

# For the subproblems of MIP after LP Relaxation and the Initial Node
# Parameters Same as above (0-5)
set_optimizer_attribute(model, "CPXPARAM_MIP_Strategy_SubAlgorithm", 1)
set_optimizer_attribute(model, "CPXPARAM_MIP_Strategy_StartAlgorithm", 1)

### Set Tolerances used ###

# Primal/ Dual feasibility tolerance - Max 1e-1 Min 1e-9 Def 1e-6
set_optimizer_attribute(model, "CPXPARAM_Simplex_Tolerances_Feasibility", 1e-6)
set_optimizer_attribute(model, "CPXPARAM_Simplex_Tolerances_Optimality", 1e-6)

# Barrier convergence tolerance - Max Inf Min 1e-12 Def 1e-8
set_optimizer_attribute(model, "CPXPARAM_Barrier_ConvergeTol", 1e-8)

# Integer Feasibility Tolerance - Max 0.5 Min 0 Def 1e-5
set_optimizer_attribute(model, "CPXPARAM_MIP_Tolerances_Integrality", 1e-05)

# Relative Gap Limits - Max Inf Min 0 Def 1e-4
set_optimizer_attribute(model, "CPXPARAM_MIP_Tolerances_MIPGap", 1e-4)

# Absolute Gap Limits - Max Inf Min 0 Def 1e-6
set_optimizer_attribute(model, "CPXPARAM_MIP_Tolerances_AbsMIPGap", 1e-06)

@time optimize!(model);

