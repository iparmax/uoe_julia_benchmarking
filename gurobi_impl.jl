using JuMP,MathOptInterface;
using Gurobi;

# Consult https://www.gurobi.com/documentation/8.1/refman/refman.html

model = read_from_file("air05.mps.gz");
#model = read_from_file("25fv47.mps");
set_optimizer(model,Gurobi.Optimizer);

### Set Number of Thread used ###

# Min 0 (Automatic) Max 16 (My PC)
# set_optimizer_attribute(model, "Threads", 16) # Possibly obsolete
MOI.set(model, MOI.NumberOfThreads(), 16)

### Set Algorithm used ###

# -1 Automatic, 0 Primal Simplex. 1 Dual Simplex
#  2 Barrier, 3 Concurrent,
# 4 deterministic concurrent, 5 deterministic concurrent simplex
# More Info https://www.gurobi.com/documentation/8.1/refman/method.html#parameter:Method
# The Following applies for the root of B&B and single LP

set_optimizer_attribute(model, "Method", 0)

# For the LP relaxations of B&B
# Parameters Same as above (-1 to 2)
set_optimizer_attribute(model, "NodeMethod", 0)

### Set Tolearnces used ###

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
