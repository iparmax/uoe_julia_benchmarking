using JuMP,MathOptInterface;
using CSV,DataFrames;

test_cases_data = DataFrame(ProblemName = String[],
						TypeOfProblem = String[],
						MaxOrMin = String[],
						NumberOfVariables = Int64[],
						NumberOfConstraints = Int64[])

lp_list = DataFrame(CSV.File("test_cases\\netlib\\netlib_labels.csv"));
total_lps = size(lp_list)[1];
@time for t in 1:total_lps
	model = read_from_file("test_cases\\netlib\\$(lp_list[t,1])");
	type = MOI.get(model, MOI.ObjectiveSense());
	variables = MOI.get(model, MOI.NumberOfVariables());
	constraints = MOI.get(model, MOI.NumberOfConstraints{MOI.ScalarAffineFunction{Float64}, MOI.LessThan{Float64}}()) + MOI.get(model, MOI.NumberOfConstraints{MOI.ScalarAffineFunction{Float64}, MOI.EqualTo{Float64}}()) + MOI.get(model, MOI.NumberOfConstraints{MOI.ScalarAffineFunction{Float64}, MOI.GreaterThan{Float64}}()) + MOI.get(model, MOI.NumberOfConstraints{MOI.ScalarAffineFunction{Float64}, MOI.Interval{Float64}}());
	results = (lp_list[t,1],"LP",string(type),variables,constraints);
	push!(test_cases_data, results);
	println(results);
end

milp_list = DataFrame(CSV.File("test_cases\\miplib\\miplib_labels.csv"));
total_milps = size(milp_list)[1];
@time for t in 1:total_milps
	model = read_from_file("test_cases\\miplib\\$(milp_list[t,1])");
	type = MOI.get(model, MOI.ObjectiveSense());
	variables = MOI.get(model, MOI.NumberOfVariables());
	constraints = MOI.get(model, MOI.NumberOfConstraints{MOI.ScalarAffineFunction{Float64}, MOI.LessThan{Float64}}()) + MOI.get(model, MOI.NumberOfConstraints{MOI.ScalarAffineFunction{Float64}, MOI.EqualTo{Float64}}()) + MOI.get(model, MOI.NumberOfConstraints{MOI.ScalarAffineFunction{Float64}, MOI.GreaterThan{Float64}}()) + MOI.get(model, MOI.NumberOfConstraints{MOI.ScalarAffineFunction{Float64}, MOI.Interval{Float64}}());
	results = (milp_list[t,1],"MILP",string(type),variables,constraints);
	push!(test_cases_data, results);
	println(results);
end

CSV.write("results\\test_cases_data.csv", test_cases_data)
