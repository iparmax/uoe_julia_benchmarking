# uoe_julia_benchmarking
Repository containing relevant code used in the development of the dissertation "Optimization Modelling and Solver Benchmarking Using the Julia Language", as part of the MSc Operational Research with Data Science at the University of Edinburgh.

## Installation 
Consult the requirements file for the required packages needed to use the solvers mentioned. Most commercial solvers (CPLEX,Gurobi,etc.) , require both a manual installation (with relevant license) and a Julia Package (mentioned in the requirements.txt).

## benchmark.jl
A function has been created that returns terminal condition of the solver, obejctive value and execution time for a given solver, provided that a model has been passed in the .mps format. (Ongoing)