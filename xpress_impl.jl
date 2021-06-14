using JuMP,MathOptInterface;
using Xpress;

# Consult https://www.fico.com/fico-xpress-optimization/docs/latest/solver/optimizer/HTML/GUID-3BEAAE64-B07F-302C-B880-A11C2C4AF4F6.html

#model = read_from_file("air05.mps.gz");
model = read_from_file("25fv47.mps");
set_optimizer(model,Xpress.Optimizer);

### Set Number of Thread used ###

# Min 0 (Automatic) Max 16 (My PC)
# set_optimizer_attribute(model, "Threads", 16) # Possibly obsolete
MOI.set(model, MOI.NumberOfThreads(), 16)

### Set Algorithm used ###

# 1 Automatic, 2 Dual Simplex,
# 3 Primal Simplex, 4 Barrier
# The Following applies for the LP and B&B
set_optimizer_attribute(model, "DEFAULTALG", 4)

### Set Tolearnces used ###

# Primal/ Dual feasibility tolerance - Max NaN Min NaN Def 1e-6
set_optimizer_attribute(model, "FEASTOL", 1e-6)
set_optimizer_attribute(model, "OPTIMALITYTOL", 1e-6)


# Barrier convergence tolerance - Def Nan (Automatic 0)
set_optimizer_attribute(model, "BARGAPSTOP", 1e-8)

# Integer Feasibility Tolerance - Max NaN Min NaN Def 5E-06
set_optimizer_attribute(model, "MIPTOL", 5.0E-06)

# Relative Gap Limits - Max NaN Min NaN Def 1e-4
set_optimizer_attribute(model, "MIPRELSTOP", 1e-4)
#
# Absolute Gap Limits - Max NaN Min NaN Def 0.0
set_optimizer_attribute(model, "MIPABSSTOP", 0.0)

@time optimize!(model);
