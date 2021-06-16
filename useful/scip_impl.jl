using JuMP,MathOptInterface;
using SCIP

# Consult https://www.scipopt.org/doc-6.0.1/html/PARAMETERS.php

# Reading the model
model = read_from_file("test_cases\\examples\\milp.mps");

# Setting Mosek as optimizer
set_optimizer(model,SCIP.Optimizer);

### Set Number of Thread used ###
set_optimizer_attribute(model, SCIP.Param("lp/threads"),16)

### Set Algorithm used ###

# Options are: 
# primal simplex 112, dual simplex - 100
# barrier - 98, ipm with crossover - 99

# The Following applies every LP problem
set_optimizer_attribute(model, SCIP.Param("lp/initalgorithm"),98);

### Set Tolerances used ###

# Primal feasibility tolerance of LP solver Def 1e-7 Min 1e-17 Max 1e-3
set_optimizer_attribute(model, SCIP.Param("numerics/lpfeastol"), 1e-6)

# Dual feasibility tolerance of LP solver Def 1e-7 Min 1e-17 Max 1e-3
set_optimizer_attribute(model, SCIP.Param("numerics/dualfeastol"), 1e-6)

# Barrier Convergence Tolerance Def 1e-10
set_optimizer_attribute(model, SCIP.Param("numerics/barrierconvtol"), 1e-8)

# Integrality Tolerance - Constraint Tolerance Def 1e-6 Min 1e-17 Max 1e-3
set_optimizer_attribute(model, SCIP.Param("numerics/feastol"), 1e-5)

# Relative Gap Def = Min 0, Max Inf
set_optimizer_attribute(model, SCIP.Param("limits/gap"), 1e-4)

# Absolute gap Def = Min 0, Max Inf
set_optimizer_attribute(model, SCIP.Param("limits/absgap"), 1e-4)

@time optimize!(model);
