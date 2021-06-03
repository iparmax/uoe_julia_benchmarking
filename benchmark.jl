using JuMP;
using Mosek, MosekTools;
using CPLEX;
using Gurobi;
using Xpress;

function solve_model(model,optimizer,time_limit)
	# Set solver attributes
	set_optimizer(model,optimizer);
	set_time_limit_sec(model,time_limit);
	set_silent(model);
	optimize!(model);
	# Print results
	@show termination_status(model)
	@show objective_value(model)
	@show solve_time(model)
	return
end

# Reading model from .mps file
model = read_from_file("random_model.mps");

# Running CPLEX Solver
solve_model(model,CPLEX.Optimizer,5)

# Running Gurobi Solver
solve_model(model,Gurobi.Optimizer,5)

# Running Xpress Solver
solve_model(model,Xpress.Optimizer,5)

# Running Mosek Solver
solve_model(model,Mosek.Optimizer,5)
