using JuMP,MathOptInterface;
using Mosek, MosekTools;
using CPLEX;
using Gurobi;
using Xpress;
using CSV,DataFrames;

function lp_solve_model(model,optimizer,time_limit)

	# Set solver attributes
	set_optimizer(model,optimizer);
	set_time_limit_sec(model,time_limit);
	set_silent(model);
	optimize!(model);

	if termination_status(model) == MOI.OPTIMAL
		status = "Optimal"
		obj_value = objective_value(model)
		sol_time = solve_time(model)
	elseif termination_status(model) == MOI.TIME_LIMIT
		status = "Time Limit"
		try
			obj_value = objective_value(model)
			sol_time = solve_time(model)
		catch
			obj_value = "NaN"
			sol_time = 99999999999999
		end
	else
		status = "Infeasible"
		obj_value = "NaN"
		sol_time = 99999999999999
	end

	return status,obj_value,sol_time
end

# LP Benchmark Start
lp_list = DataFrame(CSV.File("test_cases\\netlib\\netlib_labels.csv"));
total_lps = size(lp_list)[1];
time_results = DataFrame(Obj_Value = 1.0:total_lps,CPLEX = 1.0:total_lps,
						GuRoBi = 1.0:total_lps,FICO = 1.0:total_lps,
						Mosek = 1.0:total_lps)

@time for t in 1:total_lps
	# Reading model from .mps file
	model = read_from_file("test_cases\\netlib\\$(lp_list[t,1])");
	time_limit = 10

	# Running CPLEX Solver
	result_cplex = lp_solve_model(model,CPLEX.Optimizer,time_limit);
	time_results[t,1] = result_cplex[2]
	time_results[t,2] = result_cplex[3]

	# Running Gurobi Solver
	result_gurobi = lp_solve_model(model,Gurobi.Optimizer,time_limit);
	time_results[t,3] = result_gurobi[3]

	# Running Xpress Solver
	result_xpress = lp_solve_model(model,Xpress.Optimizer,time_limit);
	time_results[t,4] = result_xpress[3]

	# Running Mosek Solver
	result_mosek = lp_solve_model(model,Mosek.Optimizer,time_limit);
	time_results[t,5] = result_mosek[3]
end

# Export results to CSV
CSV.write("results\\lp_time_results.csv", time_results)
