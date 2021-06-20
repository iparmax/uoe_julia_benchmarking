using JuMP,MathOptInterface;
using Mosek, MosekTools;
using Clp;
using CPLEX;
using Gurobi;
using Xpress;
using Tulip
using CSV,DataFrames;

### Barrier Solvers to be tested ### 
# Listed Alphabetically
# 1. Clp
# 2. FICO Xpress
# 3. GuRoBi
# 4. IBM CPLEX
# 5. Mosek
# 6. Tulip

# List of Barrier Solvers
barrier_optimizers = Dict("Clp" => Clp.Optimizer,"FICO Xpress" => Xpress.Optimizer,
						  "GuRoBi" => Gurobi.Optimizer,"IBM CPLEX" => CPLEX.Optimizer,
						  "Mosek" => Mosek.Optimizer,"Tulip" => Tulip.Optimizer);

### Solver Parameters gathering ###

# Select Threads Key
select_threads_key = Dict("Clp" => "Not Supported","FICO Xpress" => "THREADS",
						  "GuRoBi" => "Threads","IBM CPLEX" => "CPXPARAM_Threads",
						  "Mosek" => "MSK_IPAR_NUM_THREADS","Tulip" => "Threads");

# Fixing Algorithm Key
select_algorithm_key = Dict("Clp" => "SolveType","FICO Xpress" => "DEFAULTALG",
						    "GuRoBi" => "Method", "IBM CPLEX" => "CPXPARAM_LPMethod",
							"Mosek" => "MSK_IPAR_OPTIMIZER");

# Barrier Algorithm Key 
barrier_algorithm = Dict("Clp" => 3,"FICO Xpress" => 4,
						 "GuRoBi" => 2, "IBM CPLEX" => 4,
 						 "Mosek" => 4);

# Primal & Dual Feasibility default tolerances 
primal_dual_feas_def = Dict("Clp" => 1e-7,"FICO Xpress" => 1e-7, "GuRoBi" => 1e-6, 
							"IBM CPLEX" => 1e-6,
							"Mosek" => 1e-8, "Tulip" => 1e-8);

# Barrier Convergence default tolerances 
convergence_def = Dict("FICO Xpress" => 1e-8, "GuRoBi" => 1e-8, 
					   "IBM CPLEX" => 1e-8,
					   "Mosek" => 1e-8, "Tulip" => 1e-8);

# Primal feasibility (Feasibility Tolerance) parameter Key
primal_par_key = Dict("Clp" => "PrimalTolerance","FICO Xpress" => "FEASTOL",
					  "GuRoBi" => "FeasibilityTol","IBM CPLEX" => "CPXPARAM_Simplex_Tolerances_Feasibility",
					  "Mosek" => "MSK_DPAR_INTPNT_TOL_PFEAS","Tulip" => "IPM_TolerancePFeas");

# Dual feasibility (Optimality Tolerance) parameter Key
dual_par_key = Dict("Clp" => "DualTolerance","FICO Xpress" => "OPTIMALITYTOL",
					"GuRoBi" => "OptimalityTol", "IBM CPLEX" => "CPXPARAM_Simplex_Tolerances_Optimality",
					"Mosek" => "MSK_DPAR_INTPNT_TOL_DFEAS","Tulip" => "IPM_ToleranceDFeas");

# Barrier Convergence Tolerance parameter Key
conv_par_key = Dict("FICO Xpress" => "BARGAPSTOP","GuRoBi" => "BarConvTol", 
					"IBM CPLEX" => "CPXPARAM_Barrier_ConvergeTol",
					"Mosek" => "MSK_DPAR_INTPNT_TOL_REL_GAP","Tulip" => "IPM_ToleranceRGap");

# Crossover Off parameter
crossover_par = Dict("Clp" => "SolveType","FICO Xpress" => "CROSSOVER",
						 "GuRoBi" => "Crossover", "IBM CPLEX" => "CPXPARAM_SolutionType",
				 		 "Mosek" => "MSK_IPAR_INTPNT_BASIS",);

crossover_par_key = Dict("Clp" => 4,"FICO Xpress" => 0,
				     "GuRoBi" => 0, "IBM CPLEX" => 2,
					 "Mosek" => 0);

### Mittelman Test Cases - 40 Problems ###

# Loading Mittelman Library namefiles
lp_list = DataFrame(CSV.File("test_cases\\mittelman_selection_lp\\lp_mittelman_list.csv"));
total_lps = size(lp_list)[1];

### Global Parameters ### 
time_limit = 60*20
threads = 1
solver = "IBM CPLEX"
tolerance = findmin(primal_dual_feas_def)[1]
conv_tolerance = findmin(convergence_def)[1]
solver_results = DataFrame(Problem = String[],Status = String[],
					Obj_Value = Float64[],Solver_Time = Float64[])
no_crossover = false

# Main Loop
for t in 3:3

	# Reading model from .mps file
	model = read_from_file("test_cases\\mittelman_selection_lp\\$(lp_list[t,1])");

	# Set Optimizer
	set_optimizer(model,barrier_optimizers[solver]);
	set_time_limit_sec(model,time_limit);
	
	# Set Threads Used
	if solver!="Clp"
		set_optimizer_attribute(model, select_threads_key[solver],threads);
	end

	# Set algorithm
	if solver!= "Tulip"
		set_optimizer_attribute(model, select_algorithm_key[solver],barrier_algorithm[solver]);
	end

	# Set Universal Tolerance
	set_optimizer_attribute(model, primal_par_key[solver],tolerance);
	set_optimizer_attribute(model, dual_par_key[solver],tolerance);
	
	if solver!="Clp"
		set_optimizer_attribute(model, conv_par_key[solver],conv_tolerance);
	end
	
	if no_crossover
		if solver!="Tulip"
			set_optimizer_attribute(model, crossover_par[solver],crossover_par_key[solver]);	
		end
	end
	
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
	
	results = (lp_list[t,1],status,obj_value,sol_time)
	push!(solver_results, results)
end

CSV.write("results\\barrier-lp_$(solver)_$(total_lps)_problems.csv", solver_results)
