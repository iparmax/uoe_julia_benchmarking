using JuMP,MathOptInterface;
using Mosek, MosekTools;
using CPLEX;
using Gurobi;
using Xpress;
using CSV,DataFrames;

function milp_solve_model(model,optimizer,time_limit)

	# Set solver attributes
	set_optimizer(model,optimizer);
	set_time_limit_sec(model,time_limit);
	set_silent(model);
	optimize!(model);
	iterations = MOI.get(model, MOI.NodeCount())

	if termination_status(model) == MOI.OPTIMAL
		status = "Optimal"
		obj_value = objective_value(model)
		sol_time = solve_time(model)
		optimality_gap = 0
	elseif termination_status(model) == MOI.TIME_LIMIT
		status = "Time Limit"
		try
			obj_value = objective_value(model)
			sol_time = solve_time(model)
			optimality_gap = MOI.get(model, MOI.RelativeGap())
		catch
			obj_value = Inf
			sol_time = Inf
			optimality_gap = Inf
		end
	else
		status = "Infeasible"
		obj_value = Inf
		sol_time = Inf
		optimality_gap = Inf
	end

	return status,obj_value,sol_time,iterations,optimality_gap
end

# LP Benchmark Start
milp_list = DataFrame(CSV.File("test_cases\\miplib\\miplib_labels.csv"));
total_milps = size(milp_list)[1];
total_milps = 3
time_results = DataFrame(Problem = String[],
						CPLEX_status = String[],CPLEX_result = Float64[],CPLEX_time = Float64[],CPLEX_node_count = Int64[],CPLEX_gap = Float64[],
						GuRoBi_status = String[],GuRoBi_result = Float64[],GuRoBi_time = Float64[],GuRoBi_node_count = Int64[],GuRoBi_gap = Float64[],
						Xpress_status = String[],Xpress_result = Float64[],Xpress_time = Float64[],Xpress_node_count = Int64[],Xpress_gap = Float64[],
						Mosek_status = String[],Mosek_result = Float64[],Mosek_time = Float64[],Mosek_node_count = Int64[],Mosek_gap = Float64[])
@time for t in 3:5

	# Reading model from .mps file
	model = read_from_file("test_cases\\miplib\\$(milp_list[t,1])");
	time_limit = 5

	# Running CPLEX Solver
	result_cplex = milp_solve_model(model,CPLEX.Optimizer,time_limit);

	# Running Gurobi Solver
	result_gurobi = milp_solve_model(model,Gurobi.Optimizer,time_limit);

	# Running Gurobi Solver
	result_xpress = milp_solve_model(model,Xpress.Optimizer,time_limit);

	# Running Mosek Solver
	result_mosek = milp_solve_model(model,Mosek.Optimizer,time_limit);

	results = (milp_list[t,1],result_cplex...,result_gurobi...,result_xpress...,result_mosek...)
	push!(time_results, results)

end

# Export results to CSV
CSV.write("results\\milp_time_results.csv", time_results)
