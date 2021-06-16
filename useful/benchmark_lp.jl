using JuMP,MathOptInterface;
#using Mosek, MosekTools;
#using CPLEX;
using Gurobi;
#using Xpress;
using CSV,DataFrames;

function lp_solve_model(model,optimizer,time_limit)

	# Set solver attributes
	set_optimizer(model,optimizer);
	set_time_limit_sec(model,time_limit);
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
			obj_value = 99999999999999
			sol_time = 99999999999999
		end
	else
		status = "Infeasible"
		obj_value = 99999999999999
		sol_time = 99999999999999
	end

	return status,obj_value,sol_time
end

# LP Benchmark Start
lp_list = DataFrame(CSV.File("test_cases\\mittelman_selection_lp\\lp_mittelman_list.csv"));
total_lps = size(lp_list)[1];
						
time_results = DataFrame(Problem = String[],
						Obj_Value = Float64[],GuRoBi_time = Float64[])

@time for t in 1:total_lps
	# Reading model from .mps file
	model = read_from_file("test_cases\\mittelman_selection_lp\\$(lp_list[t,1])");
	time_limit = 300

	# Running Gurobi Solver
	result_gurobi = lp_solve_model(model,Gurobi.Optimizer,time_limit);
	
	results = (lp_list[t,1],result_gurobi[2],result_gurobi[3])
	push!(time_results, results)

end

# Export results to CSV
CSV.write("results\\lp_time_results_mit.csv", time_results)