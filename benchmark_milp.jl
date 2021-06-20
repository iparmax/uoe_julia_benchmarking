using JuMP,MathOptInterface;
using Mosek, MosekTools;
using CPLEX;
using Gurobi;
using Xpress;
using SCIP
using CSV,DataFrames;

### Barrier Solvers to be tested ### 
# Listed Alphabetically
# 1. FICO Xpress
# 2. GuRoBi
# 3. IBM CPLEX
# 4. Mosek
# 5. SCIP

# List of Barrier Solvers
barrier_optimizers = Dict("FICO Xpress" => Xpress.Optimizer,
						  "GuRoBi" => Gurobi.Optimizer,"IBM CPLEX" => CPLEX.Optimizer,
						  "Mosek" => Mosek.Optimizer,"SCIP" => SCIP.Optimizer);

### Solver Parameters gathering ###

# Select Threads Key
select_threads_key = Dict("FICO Xpress" => "THREADS",
						  "GuRoBi" => "Threads","IBM CPLEX" => "CPXPARAM_Threads",
						  "Mosek" => "MSK_IPAR_NUM_THREADS","SCIP" => SCIP.Param("lp/threads"));

# Primal & Dual Feasibility default tolerances 
primal_dual_feas_def = Dict("FICO Xpress" => 1e-7, "GuRoBi" => 1e-6, 
							"IBM CPLEX" => 1e-6,
							"Mosek" => 1e-8, "SCIP" => 1e-7);

# Integrality default tolerances 
integrality_tolerance_def = Dict("FICO Xpress" => 5e-6, "GuRoBi" => 1e-5, 
								 "IBM CPLEX" => 1e-5,
								 "Mosek" => 1e-5, "SCIP" => 1e-6);

# Relative gap default tolerances 
relative_gap_def = Dict("FICO Xpress" => 1e-4, "GuRoBi" => 1e-4, 
						"IBM CPLEX" => 1e-4,
						"Mosek" => 1e-4, "SCIP" => 1e-4);

# Absolute gap default tolerances 
absolute_gap_def = Dict("FICO Xpress" => 0.0, "GuRoBi" => 1e-10, 
						"IBM CPLEX" => 1e-6,
						"Mosek" => 0.0, "SCIP" => 0.0);

# Primal feasibility (Feasibility Tolerance) parameter Key
primal_par_key = Dict("FICO Xpress" => "FEASTOL",
					  "GuRoBi" => "FeasibilityTol","IBM CPLEX" => "CPXPARAM_Simplex_Tolerances_Feasibility",
					  "Mosek" => "MSK_DPAR_INTPNT_TOL_PFEAS","SCIP" => SCIP.Param("numerics/lpfeastol"));

# Dual feasibility (Optimality Tolerance) parameter Key
dual_par_key = Dict("FICO Xpress" => "OPTIMALITYTOL",
					"GuRoBi" => "OptimalityTol", "IBM CPLEX" => "CPXPARAM_Simplex_Tolerances_Optimality",
					"Mosek" => "MSK_DPAR_INTPNT_TOL_DFEAS","SCIP" => SCIP.Param("numerics/dualfeastol"));

# Integrality Tolerance parameter Key
integrality_par_key = Dict("FICO Xpress" => "MIPTOL",
					"GuRoBi" => "IntFeasTol", "IBM CPLEX" => "CPXPARAM_MIP_Tolerances_Integrality",
					"Mosek" => "MSK_DPAR_MIO_TOL_ABS_RELAX_INT","SCIP" => SCIP.Param("numerics/feastol"));

# Relative Gap parameter Key
relative_gap_key = Dict("FICO Xpress" => "MIPRELSTOP",
						"GuRoBi" => "MipGap", "IBM CPLEX" => "CPXPARAM_MIP_Tolerances_MIPGap",
						"Mosek" => "MSK_DPAR_MIO_TOL_REL_GAP","SCIP" => SCIP.Param("limits/gap"));

# Absolute Gap parameter Key
absolute_gap_key = Dict("FICO Xpress" => "MIPABSSTOP",
						"GuRoBi" => "MipGapAbs", "IBM CPLEX" => "CPXPARAM_MIP_Tolerances_AbsMIPGap",
						"Mosek" => "MSK_DPAR_MIO_TOL_ABS_GAP","SCIP" =>SCIP.Param("limits/absgap"));


### Mittelman Test Cases - 40 Problems ###

# Loading Mittelman Library namefiles
milp_list = DataFrame(CSV.File("test_cases\\milp_selection\\milp_list.csv"));
total_lps = size(milp_list)[1];

### Global Parameters ### 
time_limit = 30 #60*20
threads = 1
solver = "IBM CPLEX"
tolerance = findmin(primal_dual_feas_def)[1]
int_tolerance = findmin(integrality_tolerance_def)[1]
rel_gap_tolerance = findmin(relative_gap_def)[1]
abs_gap_tolerance = findmin(absolute_gap_def)[1]
solver_results = DataFrame(Problem = String[],Status = String[],
					Obj_Value = Float64[],Solver_Time = Float64[])
no_crossover = true

# Main Loop
for t in 3:3

	# Reading model from .mps file
	model = read_from_file("test_cases\\milp_selection\\$(milp_list[t,1])");

	# Set Optimizer
	set_optimizer(model,barrier_optimizers[solver]);
	set_time_limit_sec(model,time_limit);
	
	# Set Threads Used
	set_optimizer_attribute(model, select_threads_key[solver],threads);

	# Set Universal Tolerances
	set_optimizer_attribute(model, primal_par_key[solver],tolerance);
	set_optimizer_attribute(model, dual_par_key[solver],tolerance);
	set_optimizer_attribute(model, integrality_par_key[solver],int_tolerance);
	set_optimizer_attribute(model, relative_gap_key[solver],rel_gap_tolerance);
	set_optimizer_attribute(model, absolute_gap_key[solver],abs_gap_tolerance);
	
	
	# Execute Model
	sol_time = @elapsed optimize!(model);

	# Results
	if termination_status(model) == MOI.OPTIMAL
		status = "Optimal"
		obj_value = objective_value(model)
	elseif termination_status(model) == MOI.TIME_LIMIT
		status = "Time Limit"
		try
			obj_value = objective_value(model)
			sol_time = time_limit
		catch
			obj_value = Inf
			sol_time = Inf
		end
	else
		status = "Infeasible"
		obj_value = Inf
	end
	
	results = (milp_list[t,1],status,obj_value,sol_time)
	push!(solver_results, results)
end

CSV.write("results\\barrier-lp_$(solver)_$(total_lps)_problems.csv", solver_results)
