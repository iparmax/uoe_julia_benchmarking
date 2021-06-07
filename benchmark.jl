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

	label = split(string(optimizer), ".")
	if label[1] == "Optimizer"
		println("Mosek Optimizer Report")
	else
		println("$(label[1]) Optimizer Report")
	end

	@show termination_status(model)
	@show objective_value(model)
	@show solve_time(model)
	println(" ")
	return
end

# Reading model from .mps file
model = read_from_file("s250r10.mps.bz2");
time_limit = 30

# Running CPLEX Solver
solve_model(model,CPLEX.Optimizer,time_limit)

# Running Gurobi Solver
solve_model(model,Gurobi.Optimizer,time_limit)

# Running Xpress Solver
solve_model(model,Xpress.Optimizer,time_limit)

# Running Mosek Solver
solve_model(model,Mosek.Optimizer,time_limit)
