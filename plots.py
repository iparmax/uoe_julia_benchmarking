import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

solvers = ["GuRoBi","IBM_CPLEX","FICO_Xpress","Clp","Mosek"]

all_solvers_any = np.zeros((5,35))
for count, solver in enumerate(solvers):
    any_simplex_time = []
    dual_time = []
    primal_time = []
    load_file = f"results\\final\\simplex_{solver}.csv"
    df = pd.read_csv(load_file)
    for index, row in df.iterrows():
        if (row[f'Status_{solver}_Dual']==row[f'Status_{solver}_Primal'] and row[f'Status_{solver}_Dual'] == "Optimal" ):
            solver_time = min(row[f'Solver_Time_{solver}_Dual'],row[f'Solver_Time_{solver}_Primal'])
            julia_time = min(row[f'Julia_Time_{solver}_Dual'],row[f'Julia_Time_{solver}_Primal'])
            best_solver = "Dual"
            if row[f'Solver_Time_{solver}_Dual']>row[f'Solver_Time_{solver}_Primal']:
                best_solver = "Primal"
            any_simplex_time.append(solver_time)
            dual_time.append(row[f'Solver_Time_{solver}_Dual'])
            primal_time.append(row[f'Solver_Time_{solver}_Primal'])
        elif row[f'Status_{solver}_Dual'] == "Optimal":
            solver_time = row[f'Solver_Time_{solver}_Dual']
            julia_time = row[f'Julia_Time_{solver}_Dual']
            best_solver = "Dual"
            any_simplex_time.append(solver_time)
            dual_time.append(row[f'Solver_Time_{solver}_Dual'])
            if row[f'Status_{solver}_Primal'] == "Time Limit":
                primal_time.append(1200)
            else:
                primal_time.append(0)
        elif row[f'Status_{solver}_Primal'] == "Optimal":
            solver_time = row[f'Solver_Time_{solver}_Primal']
            julia_time = row[f'Julia_Time_{solver}_Primal']
            best_solver = "Primal"
            any_simplex_time.append(solver_time)
            primal_time.append(row[f'Solver_Time_{solver}_Primal'])
            if row[f'Status_{solver}_Dual'] == "Time Limit":
                if solver == "Clp":
                    dual_time.append(1800)
                else:
                    dual_time.append(1200)
            else:
                dual_time.append(0)
        elif row[f'Status_{solver}_Dual'] == "Time Limit" and row[f'Status_{solver}_Primal'] == "Time Limit":
                if solver == "Clp":
                    any_simplex_time.append(1800)
                    dual_time.append(1800)
                    primal_time.append(1800)
                else:
                    any_simplex_time.append(1200)
                    dual_time.append(1200)
                    primal_time.append(1200)

        elif row[f'Status_{solver}_Dual'] == "Time Limit":
                if solver == "Clp":
                    any_simplex_time.append(1800)
                    dual_time.append(1800)
                    primal_time.append(0)
                else:
                    any_simplex_time.append(1200)
                    dual_time.append(1200)
                    primal_time.append(0)

        elif row[f'Status_{solver}_Primal'] == "Time Limit":

                if solver == "Clp":
                    any_simplex_time.append(1800)
                    dual_time.append(0)
                    primal_time.append(1800)
                else:
                    any_simplex_time.append(1200)
                    dual_time.append(0)
                    primal_time.append(1200)
        else:
            any_simplex_time.append(0)
            dual_time.append(0)
            primal_time.append(0)

    all_solvers_any[count,:] = any_simplex_time
    t = np.arange(all_solvers_any.shape[1])
    fig, ax = plt.subplots()
    ax.plot(t, dual_time,label='Dual')
    ax.plot(t, primal_time,label='Primal')
    ax.grid()
    ax.set_xticks(t)
    ax.set_xticklabels(df["Problem"],fontsize = 7,rotation =70)
    ax.set(xlabel='Problem', ylabel='Times (s)',
       title=f'Dual v Primal - {solver}')
    plt.legend(framealpha=1)
    plt.show()

results = all_solvers_any.T

x = np.arange(results.shape[0])
dx = (np.arange(results.shape[1])-results.shape[1]/2.)/(results.shape[1]+2.)
d = 1./(results.shape[1]+2.)


fig, ax=plt.subplots()
for i in range(results.shape[1]):
    ax.bar(x+dx[i],results[:,i], width=d, label=solvers[i])

ax.set_xticks(x)
ax.set_xticklabels(df["Problem"],fontsize = 7,rotation =70)
ax.set(xlabel='Problem', ylabel='Times (s)',
       title=f'Cumulative Performance of all Solvers')
plt.legend(framealpha=1)
plt.show()