# uoe_julia_benchmarking
Repository containing relevant code used in the development of the dissertation "Optimization Modelling and Solver Benchmarking Using the Julia Language", as part of the MSc Operational Research with Data Science at the University of Edinburgh.

## Installation 
Consult the requirements file for the required packages needed to use the solvers mentioned. Most commercial solvers (CPLEX,Gurobi,etc.) , require both a manual installation (with relevant license) and a Julia Package (mentioned in the requirements.txt).

## benchmark_simplex.jl
An interface for benchmarking six solvers (Clp, FICO Xpress, GuRoBi, IBM CPLEX, HiGHS, Mosek), using simplex based algorithms for LPs. Parameters such as primal feasiblity and dual feasibity can be universally set for fair comparison. Also parameters such as time limits and multiple threads can be included for solvers that support them. Consult the solvers_info pdf for proper usage.

## benchmark_barrier.jl
An interface for benchmarking six solvers (Clp, FICO Xpress, GuRoBi, IBM CPLEX, Tulip, Mosek), using interior point methods for LPs. Parameters such as primal feasiblity and dual feasibity can be universally set for fair comparison. Parameters such as barrier convergence tolerance can't be influenced by all solvers but all solvers have the same default tolerance. Additionally, the Tulip solver does not support crossover, so there is the option of disabling crossover for all solvers.Finally, parameters such as time limits and multiple threads can be included for solvers that support them. Consult the solvers_info pdf for proper usage.

## benchmark_milp.jl
An interface for benchmarking five solvers (FICO Xpress, GuRoBi, IBM CPLEX, SCIP, Mosek), for mixed integer linear programming problems. Parameters such as primal feasiblity and dual feasibity, integrality tolerance, absolute and relative gap can be universally set for fair comparison. Also, parameters such as time limits and multiple threads can be included for solvers that support them. Consult the solvers_info pdf for proper usage.
