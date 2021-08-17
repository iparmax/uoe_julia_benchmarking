# uoe_julia_benchmarking
Repository containing relevant code used in the development of the dissertation "Optimization Modelling and Solver Benchmarking Using the Julia Language", as part of the MSc Operational Research with Data Science at the University of Edinburgh.

## Installation 
Consult the requirements file for the required packages needed to use the solvers mentioned. Most commercial solvers (CPLEX,Gurobi,etc.) , require both a manual installation (with relevant license) and a Julia Package (mentioned in the requirements.txt).

## benchmark_lp.jl
An interface for benchmarking seven solvers (Clp, FICO Xpress, GuRoBi, IBM CPLEX, HiGHS, Mosek, Tulip), using simplex based or interior-point methods for LPs. Three modes are available on this inteface, a simplex mode, a barrier mode or an automatic mode (default). If a simplex mode is chosen, the choice between dual or primal simplex must be given as well. Accordingly, if an interior point method is given crossover must be either activated or deactivated. Threads can be influenced for non-automatic modes, as well as feasiility tolernaces. The script is setup to solve the thirty five instances mentiones in the dissertation attached to this repository. Parameters that influence different bechmarks run can be changed in lines 135 to 165.

## benchmark_barrier.jl
An interface for benchmarking six solvers (Clp, FICO Xpress, GuRoBi, IBM CPLEX, Tulip, Mosek), using interior point methods for LPs. Parameters such as primal feasiblity and dual feasibity can be universally set for fair comparison. Parameters such as barrier convergence tolerance can't be influenced by all solvers but all solvers have the same default tolerance. Additionally, the Tulip solver does not support crossover, so there is the option of disabling crossover for all solvers.Finally, parameters such as time limits and multiple threads can be included for solvers that support them. Consult the solvers_info pdf for proper usage.
