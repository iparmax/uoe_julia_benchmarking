using JuMP,MathOptInterface;
using Clp

# ONLY LP - ONLY SIMPLEX
# Consult https://github.com/jump-dev/Clp.jl

# Reading the model
model = read_from_file("test_cases\\examples\\lp.mps");

# Setting CPLEX as optimizer
set_optimizer(model,Clp.Optimizer);

### Set Number of Thread used ###
# Not Supported #

### Set Algorithm used ###

# Options are: 
# dual simplex (0), primal simplex (1), 

# The Following applies for an LP problem
set_optimizer_attribute(model, "SolveType", 0)

### Set Tolerances used ###

# Primal/ Dual feasibility tolerance - Def 1e-7
set_optimizer_attribute(model, "PrimalTolerance", 1e-6)
set_optimizer_attribute(model, "DualTolerance", 1e-6)

@time optimize!(model);
