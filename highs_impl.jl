using JuMP,MathOptInterface;
using HiGHS

# ONLY LP - MOSTLY SIMPLEX
# Consult https://www.maths.ed.ac.uk/hall/HiGHS/HighsOptions.set

# Reading the model
model = read_from_file("test_cases\\examples\\lp.mps");

# Setting CPLEX as optimizer
set_optimizer(model,HiGHS.Optimizer);

### Set Number of Thread used ### ! It's not working as expected
set_optimizer_attribute(model, "highs_min_threads", 2)
set_optimizer_attribute(model, "highs_max_threads", 2)

### Set Algorithm used ###

# Options are: 
# "simplex","choose" or "ipm"

# The Following applies for an LP problem
set_optimizer_attribute(model, "solver", "choose")

### Set Tolearances used ###

# Primal/ Dual feasibility tolerance - Max Inf Min 1e-10 Def 1e-7
set_optimizer_attribute(model, "primal_feasibility_tolerance", 1e-6)
set_optimizer_attribute(model, "dual_feasibility_tolerance", 1e-6)

@time optimize!(model);
