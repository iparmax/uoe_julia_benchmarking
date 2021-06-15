using JuMP,MathOptInterface;
using Gurobi;

# Consult for more parameters https://www.gurobi.com/documentation/8.1/refman/refman.html

# Reading the model
#model = read_from_file("test_cases\\examples\\lp.mps");
model = read_from_file("test_cases\\examples\\milp.mps");

# Setting Gurobi as optimizer
set_optimizer(model,Gurobi.Optimizer);

### Set Number of Thread used ###

# Through MOI for Gurobi,Xpress,CPLEX
MOI.set(model, MOI.NumberOfThreads(), 16)

### Set Algorithm used ###

# Options are: 
# -1=automatic, 0=primal simplex, 
# 1=dual simplex, 2=barrier,
# 3=concurrent, 4=deterministic concurrent,
# 5=deterministic concurrent simplex.

# The Following applies for the root of B&B and single LP
set_optimizer_attribute(model, "Method", 0)

# For the LP relaxations of B&B - Parameters same as above
set_optimizer_attribute(model, "NodeMethod", 0)

### Set Tolerances used ###

# Primal/ Dual feasibility tolerance - Max 1e-2 Min 1e-9 Def 1e-6
set_optimizer_attribute(model, "FeasibilityTol", 1e-6)
set_optimizer_attribute(model, "OptimalityTol", 1e-6)

# Barrier convergence tolerance - Max 1 Min 0 Def 1e-8
set_optimizer_attribute(model, "BarConvTol", 1e-8)

# Integer Feasibility Tolerance - Max 1e-1 Min 1e-9 Def 1e-5
set_optimizer_attribute(model, "IntFeasTol", 1e-5)

# Relative Gap Limits - Max Inf Min 0 Def 1e-4
set_optimizer_attribute(model, "MipGap", 1e-4)

# Absolute Gap Limits - Max Inf Min 0 Def 1e-10
set_optimizer_attribute(model, "MipGapAbs", 1e-10)

@time optimize!(model);
