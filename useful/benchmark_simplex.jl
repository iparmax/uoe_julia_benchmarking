using JuMP,MathOptInterface;
using Mosek, MosekTools;
using CPLEX;
using Gurobi;
using Xpress;
using HiGHS
using Clp
using CSV,DataFrames;

### Simplex Solvers to be tested ### 
# Listed Alphabetically
# 1. Clp
# 2. FICO Xpress
# 3. GuRoBi
# 4. HiGHS
# 5. IBM CPLEX
# 6. Mosek

# List of Simplex Solvers
simplex_optimizers = Dict("Clp" => Clp.Optimizer, "FICO Xpress" => Xpress.Optimizer,
						  "GuRoBi" => Gurobi.Optimizer, "HiGHS" => HiGHS.Optimizer,
						  "IBM CPLEX" => CPLEX.Optimizer, "Mosek" => Mosek.Optimizer);

### Solver Parameters gathering ###

# Select Threads Key
select_threads_key = Dict("Clp" => "Not Supported", "FICO Xpress" => "THREADS",
						  "GuRoBi" => "Threads", "HiGHS" => "highs_max_threads",
						  "IBM CPLEX" => "CPXPARAM_Threads", "Mosek" => "MSK_IPAR_NUM_THREADS");

# Fixing Algorithm Key
select_algorithm_key = Dict("Clp" => "SolveType", "FICO Xpress" => "DEFAULTALG",
							"GuRoBi" => "Method", "HiGHS" => "solver",
							"IBM CPLEX" => "CPXPARAM_LPMethod", "Mosek" => "MSK_IPAR_OPTIMIZER");

# Primal Simplex Key 
primal_simplex_key = Dict("Clp" => 1, "FICO Xpress" => 3,
						  "GuRoBi" => 0, "HiGHS" => "NaN",
						  "IBM CPLEX" => 1, "Mosek" => 6);

# Dual Simplex Key 
dual_simplex_key = Dict("Clp" => 0, "FICO Xpress" => 2,
						  "GuRoBi" => 1, "HiGHS" => "simplex",
						  "IBM CPLEX" => 2, "Mosek" => 1);

# Primal & Dual Feasibility default tolerances 
primal_dual_feas_def = Dict("Clp" => 1e-7, "FICO Xpress" => 1e-7,
							"GuRoBi" => 1e-6, "HiGHS" => 1e-7,
							"IBM CPLEX" => 1e-6, "Mosek" => 1e-8);

# Primal feasibility (Feasibility Tolerance) parameter Key
primal_par_key = Dict("Clp" => "PrimalTolerance", "FICO Xpress" => "FEASTOL",
					  "GuRoBi" => "FeasibilityTol", "HiGHS" => "primal_feasibility_tolerance",
					  "IBM CPLEX" => "CPXPARAM_Simplex_Tolerances_Feasibility", "Mosek" => "MSK_DPAR_BASIS_TOL_X");

# Dual feasibility (Optimality Tolerance) parameter Key
dual_par_key = Dict("Clp" => "DualTolerance", "FICO Xpress" => "OPTIMALITYTOL",
					"GuRoBi" => "OptimalityTol", "HiGHS" => "dual_feasibility_tolerance",
					"IBM CPLEX" => "CPXPARAM_Simplex_Tolerances_Optimality", "Mosek" => "MSK_DPAR_BASIS_TOL_S");

### Mittelman Test Cases - 40 Problems ###

# Loading Mittelman Library namefiles
lp_list = DataFrame(CSV.File("test_cases\\mittelman_selection_lp\\lp_mittelman_list.csv"));
total_lps = size(lp_list)[1];

### Global Parameters ### 
time_limit = 30*60
threads = 1
algorithm = "dual simplex"
solver = "HiGHS"
tolerance = findmin(primal_dual_feas_def)[1]
solver_results = DataFrame(Problem = String[],Status = String[],
					Obj_Value = Float64[],Iterations = Int64[],Solver_Time = Float64[],Julia_Time =Float64[] )

# Main Loop
@time for t in 15:38#total_lps
	if t != 6 && t != 12
		# Reading model from .mps file
		model = read_from_file("test_cases\\mittelman_selection_lp\\$(lp_list[t,1])");
		println(lp_list[t,1])
		# Set Optimizer and time limit
		set_optimizer(model,simplex_optimizers[solver]);
		set_time_limit_sec(model,time_limit);

		# Set Threads Used
		if solver != "Clp"
			set_optimizer_attribute(model, select_threads_key[solver],threads);
		end

		# Set algorithm
		if algorithm == "dual simplex"
			set_optimizer_attribute(model, select_algorithm_key[solver],dual_simplex_key[solver]);
		else
			if solver == "HiGHS"
				break
			else
				set_optimizer_attribute(model, select_algorithm_key[solver],primal_simplex_key[solver]);
			end
		end

		# Set Universal Tolerance
		#set_optimizer_attribute(model, primal_par_key[solver],tolerance);
		#set_optimizer_attribute(model, dual_par_key[solver],tolerance);

		# Execute Model
		julia_time = @elapsed optimize!(model);

		# Results
		if termination_status(model) == MOI.OPTIMAL
			status = "Optimal"
			obj_value = objective_value(model)
			sol_time = solve_time(model)
			
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
			sol_time = Inf
		end
		
		iterations = 0 
		if solver != "Clp"
			iterations = simplex_iterations(model)
		end
		
		results = (lp_list[t,1],status,obj_value,iterations,sol_time,julia_time)
		push!(solver_results, results)
	end
end

CSV.write("results\\$(algorithm)_$(solver)_$(total_lps-1)_problems.csv", solver_results)
