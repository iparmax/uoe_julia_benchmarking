using JuMP,MathOptInterface;
using Mosek,MosekTools;

# Consult https://docs.mosek.com/9.2/rmosek/cont-optimizers.html

# Reading the model
#model = read_from_file("test_cases\\examples\\lp.mps");
model = read_from_file("test_cases\\examples\\milp.mps");

# Setting Mosek as optimizer
set_optimizer(model,Mosek.Optimizer);

### Set Number of Thread used ###

# Mosek can't alternate between threads after a session starts
set_optimizer_attribute(model, "MSK_IPAR_NUM_THREADS",1)

### Set Algorithm used ###

# Options are: 
# 0 Conic, 1 Dual Simplex,
# 2 Any,3 Any Simplex, 4 Barrier
# 5 Mixed Integer Opt, 6 Primal Simplex

# The Following applies for the root of B&B and single LP
set_optimizer_attribute(model, "MSK_IPAR_OPTIMIZER",2)

# Algorithm on the non root nodes - Parameters same as above
set_optimizer_attribute(model, "MSK_IPAR_MIO_NODE_OPTIMIZER",1)
set_optimizer_attribute(model, "MSK_IPAR_MIO_NODE_OPTIMIZER",1)

### Set Tolerances used ###

# Primal/ Dual feasibility tolerance for Simplex Only - Def 1e-6 Min 1e-9 Max Inf
set_optimizer_attribute(model, "MSK_DPAR_BASIS_TOL_X", 1e-9)
set_optimizer_attribute(model, "MSK_DPAR_BASIS_TOL_S", 1e-9)

# Primal/ Dual feasibility tolerance for Interior Point Method Only - Default 1e-8 Min 0 Max 1
set_optimizer_attribute(model, "MSK_DPAR_INTPNT_TOL_PFEAS", 1e-6)
set_optimizer_attribute(model, "MSK_DPAR_INTPNT_TOL_DFEAS", 1e-6)

# Barrier convergence tolerance - Def 1e-8 Min 1e-14 Max Inf
set_optimizer_attribute(model, "MSK_DPAR_INTPNT_TOL_REL_GAP", 1e-8)

# Integer Feasibility Tolerance - Max Inf Min 1e-9 Def 1e-5
set_optimizer_attribute(model, "MSK_DPAR_MIO_TOL_ABS_RELAX_INT", 1e-5)

# Relative Gap Limits - Max Inf Min 0 Def 1e-4
set_optimizer_attribute(model, "MSK_DPAR_MIO_TOL_REL_GAP", 1e-4)

# Absolute Gap Limits - Max Inf Min 0 Def 0.0
set_optimizer_attribute(model, "MSK_DPAR_MIO_TOL_ABS_GAP", 0.0)

@time optimize!(model);
