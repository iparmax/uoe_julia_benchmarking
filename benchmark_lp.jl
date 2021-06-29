using JuMP,MathOptInterface;
using Mosek, MosekTools;
using CPLEX;
using Gurobi;
using Xpress;
using HiGHS
using Clp
using CSV,DataFrames;
using Tulip

### Solvers to be tested ### 
# Listed Alphabetically
# 1. Clp
# 2. FICO Xpress
# 3. GuRoBi
# 4. HiGHS
# 5. IBM CPLEX
# 6. Mosek
# 7. Tulip

# List of Simplex Solvers
optimizers = Dict("Clp" => Clp.Optimizer, "FICO Xpress" => Xpress.Optimizer,
						  "GuRoBi" => Gurobi.Optimizer, "HiGHS" => HiGHS.Optimizer,
						  "IBM CPLEX" => CPLEX.Optimizer, "Mosek" => Mosek.Optimizer,
						  "Tulip" => Tulip.Optimizer);
						
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
select_threads_key = Dict("Clp" => "Not Supported", "FICO Xpress" => "THREADS",
						  "GuRoBi" => "Threads", "HiGHS" => "highs_max_threads",
						  "IBM CPLEX" => "CPXPARAM_Threads", "Mosek" => "MSK_IPAR_NUM_THREADS","Tulip" => "Threads");

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

# Barrier Algorithm Key 
barrier_algorithm = Dict("Clp" => 3,"FICO Xpress" => 4,
						 "GuRoBi" => 2, "IBM CPLEX" => 4,
 						 "Mosek" => 4);

### Changing Tolerances option ###                        

# Primal & Dual Feasibility default tolerances 
primal_dual_feas_def = Dict("Clp" => 1e-7, "FICO Xpress" => 1e-7,
							"GuRoBi" => 1e-6, "HiGHS" => 1e-7,
							"IBM CPLEX" => 1e-6, "Mosek" => 1e-8,"Tulip" => 1e-8);

# Barrier Convergence default tolerances 
convergence_def = Dict("FICO Xpress" => 1e-8, "GuRoBi" => 1e-8, 
					   "IBM CPLEX" => 1e-8,
					   "Mosek" => 1e-8, "Tulip" => 1e-8);

# Primal feasibility (Feasibility Tolerance) parameter Key
primal_par_key = Dict("Clp" => "PrimalTolerance", "FICO Xpress" => "FEASTOL",
					  "GuRoBi" => "FeasibilityTol", "HiGHS" => "primal_feasibility_tolerance",
					  "IBM CPLEX" => "CPXPARAM_Simplex_Tolerances_Feasibility", "Mosek" => "MSK_DPAR_BASIS_TOL_X",
					  "Tulip" => "IPM_TolerancePFeas");

# Dual feasibility (Optimality Tolerance) parameter Key
dual_par_key = Dict("Clp" => "DualTolerance", "FICO Xpress" => "OPTIMALITYTOL",
					"GuRoBi" => "OptimalityTol", "HiGHS" => "dual_feasibility_tolerance",
					"IBM CPLEX" => "CPXPARAM_Simplex_Tolerances_Optimality", "Mosek" => "MSK_DPAR_BASIS_TOL_S",
					"Tulip" => "IPM_ToleranceDFeas");

# Barrier Convergence Tolerance parameter Key
conv_par_key = Dict("FICO Xpress" => "BARGAPSTOP","GuRoBi" => "BarConvTol", 
					"IBM CPLEX" => "CPXPARAM_Barrier_ConvergeTol",
					"Mosek" => "MSK_DPAR_INTPNT_TOL_REL_GAP","Tulip" => "IPM_ToleranceRGap");

### Turning on/off Crossover (Barrier Only)
crossover_par = Dict("Clp" => "SolveType","FICO Xpress" => "CROSSOVER",
						 "GuRoBi" => "Crossover", "IBM CPLEX" => "CPXPARAM_SolutionType",
				 		 "Mosek" => "MSK_IPAR_INTPNT_BASIS",);

crossover_par_key = Dict("Clp" => 4,"FICO Xpress" => 0,
				     "GuRoBi" => 0, "IBM CPLEX" => 2,
					 "Mosek" => 0);

### Mittelman Test Cases - 35 Problems ###

# Loading Mittelman Library namefiles
lp_list = DataFrame(CSV.File("test_cases\\mittelman_selection_lp\\lp_mittelman_list.csv"));
total_lps = size(lp_list)[1];










### Global Parameters ###

# Mode can be Automatic, Simplex or Barrier #
mode = "Automatic"

# Time limit strictly integer - if zero no time limit set #
time_limit = 30

# Threads in the 1-16 range due to CPU restrictions - Not in use if Automatic mode is on # 
threads = 1

# Selecting Solver
solver = "GuRoBi"

# Simplex algorithm selection - irrelevant if mode not simplex
simplex_algorithm = "primal"

# Crossover on/off
crossover = "on"

# Any appropriate float - if zero no influence is set on different tolerances
tolerance = 0.0
conv_tolerance = 0.0

# Declaring DataFrames for saving results
solver_results = DataFrame(Problem = String[],Status = String[],
					Obj_Value = Float64[],Iterations = Int64[],Solver_Time = Float64[],Julia_Time =Float64[] )

# Range of problems solved #
start = 1
finish = total_lps

### Global Parameters ###










### Main Loop begins ###
@time for t in start:finish
	
	# Reading model from .mps file
	model = read_from_file("test_cases\\mittelman_selection_lp\\$(lp_list[t,1])");
	println("Solving problem no. $(t) - $(lp_list[t,1])")

	# Setting Optimizer
	set_optimizer(model,optimizers[solver]);
	println("Optimizer $(solver) was set succesfully.")

	# Setting time limit
	if time_limit > 0
		set_time_limit_sec(model,time_limit);
		println("Time limit at $(time_limit) seconds was set succesfully.")
	else
		println("No time limit was set.")
	end

	# Setting number of threads
	if mode != "Automatic"
		try
			if solver != "Clp" 
				set_optimizer_attribute(model, select_threads_key[solver],threads);
				println("$(threads) threads were set succesfully.")
			end
		catch
			if solver == "Clp"
				println("Clp can't influence number of threads - Only 1 is set.")
			else
				println("Something went wrong 1.")
			end
		end
	end

	# Set algorithm
	if mode != "Automatic"

		if simplex_algorithm == "dual" && mode == "Simplex"
			try
				set_optimizer_attribute(model, select_algorithm_key[solver],dual_simplex_key[solver]);
			catch
				if solver == "Tulip"
					println("Tulip does not have a dual simplex algorithm.")
				else
					println("Something went wrong.")
				end
			end

		elseif simplex_algorithm == "primal" && mode == "Simplex"
			try
				set_optimizer_attribute(model, select_algorithm_key[solver],primal_simplex_key[solver]);
			catch
				if solver == "Tulip"
					println("Tulip does not have a primal simplex algorithm.")
				elseif solver == "HiGHS" 
					println("HiGHS does not have a primal simplex algorithm.")
				else
					println("Something went wrong.")
				end
			end

		elseif mode == "Barrier"
			try
				set_optimizer_attribute(model, select_algorithm_key[solver],barrier_algorithm[solver]);
			catch
				if solver == "HiGHS"
					println("HiGHS does not have a barrier algorithm.")
				elseif solver == "Tulip"
				else 
					println("Something went wrong.")
				end
			end
		end
	end

	# Set Universal Tolerancea
	if tolerance != 0.0 
		set_optimizer_attribute(model, primal_par_key[solver],tolerance);
		set_optimizer_attribute(model, dual_par_key[solver],tolerance);
	end

	if mode == "Barrier" && conv_tolerance != 0.0
		try 
			set_optimizer_attribute(model, conv_par_key[solver],conv_tolerance);
		catch
			if solver == "Clp"
				println("Clp can't influence barrier convergence tolerance.")
			end
		end
	end

	# Activate/Deactivate Crossover 
	if mode == "Barrier" && crossover == "off"
		try 
			set_optimizer_attribute(model, crossover_par[solver],crossover_par_key[solver]);
		catch
			if solver == "Tulip"
				println("Tulip does not support Crossover.")
			end
		end
	end

	# Execute Model and collect Julia time
	println("Optimization starts.")
	julia_time = @elapsed optimize!(model);

	# Results
	if termination_status(model) == MOI.OPTIMAL
		status = "Optimal"
		obj_value = objective_value(model)

		if solver != "Tulip"
			sol_time = solve_time(model)
		else
			sol_time = julia_time
		end

	elseif termination_status(model) == MOI.TIME_LIMIT
		status = "Time Limit"
		try
			obj_value = objective_value(model)
			sol_time = time_limit
		catch
			obj_value = Inf
			sol_time = time_limit
		end
	elseif julia_time >= time_limit && solver == "Clp"
		status = "Time Limit"
		obj_value = Inf
		sol_time = time_limit
	else
		status = "Infeasible"
		obj_value = 0.0
		sol_time = 0.0
	end
	
	# Gathering iterations
	iterations = 0
	if mode == "Barrier" && solver != "Clp"
		iterations = barrier_iterations(model)
	elseif mode == "Simplex" && solver != "Clp"
		iterations = simplex_iterations(model)
	elseif mode == "Automatic" && solver != "Clp"
		iterations = barrier_iterations(model) + simplex_iterations(model)
	end

	# Pushing results to CSV
	results = (lp_list[t,1],status,obj_value,iterations,sol_time,julia_time)
	push!(solver_results, results)
	println("Results were pushed to file. Optimizations Ends.")
end

# Saving results to file
if mode == "Simplex"
	CSV.write("results\\$(mode)_$(simplex_algorithm)_$(solver)_$(start)-$(finish)_problems.csv", solver_results)
else
	CSV.write("results\\$(mode)_$(solver)_$(start)-$(finish)_problems.csv", solver_results)
end
