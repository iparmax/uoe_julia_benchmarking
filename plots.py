import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Automatic Solvers
global automatic
automatic = ["Clp", "FICO_Xpress", "GuRoBi", "IBM_CPLEX", "HiGHS", "Mosek", "Tulip"]

# Barrier Solvers - No Crossover
global barrier
barrier = ["Clp", "FICO_Xpress", "GuRoBi", "IBM_CPLEX", "Mosek", "Tulip"]

# Barrier Solver - Crossover
global c_barrier
c_barrier = ["Clp", "FICO_Xpress", "GuRoBi", "IBM_CPLEX", "Mosek"]

# Primal Simplex Solvers
global p_simplex
p_simplex = ["Clp", "FICO_Xpress", "GuRoBi", "IBM_CPLEX", "Mosek"]

# Primal Simplex Solvers
global d_simplex
d_simplex = ["Clp", "FICO_Xpress", "GuRoBi", "IBM_CPLEX", "HiGHS", "Mosek"]

global modes
modes = ["Automatic", "Barrier", "Cross_Barrier", "Simplex_dual", "Simplex_primal"]

global labels
labels = {"A": "Automatic", "B": "Barrier - No Crossover","CB": "Barrier - With Crossover",
          "PS": "Simplex Primal", "DS": "Simplex Dual",}
measure = "Solver_Time"
def matrix_processing (x):

    x = x.drop([0])
    rows = x.values.shape[0]
    report = x["Status"].value_counts()

    optimal = report["Optimal"]/rows

    try:
        time_limit = report["Time Limit"]/rows
    except:
        time_limit = 0 
    try:
        infeasible = report["Infeasible"]/rows
    except:
        infeasible = 0

    x.loc[(x.Status == 'Time Limit'),'Solver_Time']= np.inf
    x.loc[(x.Status == 'Infeasible'),'Solver_Time']= np.inf
    x.loc[(x.Solver_Time == 0),'Solver_Time']= 0.0001
    report = [optimal,time_limit,infeasible] 
    return x,report



print('Performance profile plotter initialized.')

while True:

    print("State plots needed. Choices : (Performance Profile 'P' / Performance Graph Chart 'G' / Success Bar Chart 'B' / All 'A' )")

    x = input()

    if x.upper() == "P":
        to_plot = "Performance Profile"
        break
    elif x.upper() == "G":
        to_plot = "Graph Chart"
        break
    elif x.upper() == "B":
        to_plot = "Bar Chart"
        break
    elif x.upper() == "A":
        to_plot = "All"
        break
    else:
        print("Wrong Input - Try Again")

while True:
    if to_plot == "Bar Chart":
        break
    print("State performance measure. Choices : (Solver Time 'S' / Julia Time 'J' / Iterations 'I' )")

    x = input()

    if x.upper() == "S":
        measure = "Solver_Time"
        break
    elif x.upper() == "J":
        measure = "Julia_Time"
        break
    elif x.upper() == "I":
        measure = "Iterations"
        break
    else:
        print("Wrong Input - Try Again")
    

while True:
    
    print("State criteria of assessement. Choices : (by Mode (One Mode - Any Solver) 'M', by Solver (One Solver - Any Mode) 'S')")

    x = input()

    if x.upper() == "S":
        criteria = "Solver"
        break
    elif x.upper() == "M":
        criteria = "Mode"
        break
    else:
        print("Wrong Input - Try Again")

if criteria == "Solver":

    print("State solver to be assessed. Choices : ( Clp , FICO_Xpress , GuRoBi , IBM_CPLEX , HiGHS , Mosek , Tulip ")

    while True:

        x = input()
        
        if x in automatic:
            break
        else:
            print("Wrong Input - Try Again")

    count = 0
    available = [] 
    if x in automatic:
        count += 1
        available.append("A")
    
    if x in barrier:
        count += 1
        available.append("B")

    if x in c_barrier:
        count += 1
        available.append("CB") 

    if x in p_simplex:
        count += 1        
        available.append("PS")

    if x in d_simplex:
        count += 1 
        available.append("DS")

    solver = x
    print(f"State number of algorithms for comparison. Maximum algorithms for {solver} are {count}.")

    while True:

        x = input()

        try:
            if int(x) > count:
                print("More algorithms than supported: Try again")
            elif int(x)<=1:
                print("At least two algorithms must be selected.")
            else:
                break
        except:
            print("Input must be numerical.")
            pass
    
    if int(x) == count:
        print("All algorithms were selected.")
        selected = available
    else:
            
        print(f"Select {x} algorithms. Available algorithms are:")

        if solver in automatic:
            print("Automatic: keyword 'A'")
        
        if solver in barrier:
            print("Barrier - No Crossover: keyword  'B'")

        if solver in c_barrier:
            print("Barrier - With Crossover: keyword 'CB'")

        if solver in p_simplex:
            print("Primal Simplex: keyword  'PS'")

        if solver in d_simplex:
            print("Dual Simplex: keyword  'DS'")

        selected = []
        for i in range (0,int(x)):
            
            while True:
                print(f"Algorithm no.{i+1}")
                print("Type keywords of algorithms that to be examined.")
                y = input()

                if y in available and y not in selected:
                    selected.append(y)
                    break
                else:
                    print("Wrong Input. Keyword was wrong, already selected or not available.")
    
    matrix = np.zeros([35,])
    success = np.zeros([3,])

    if "A" in selected:

        automatic = pd.read_csv(f"results\\automatic\\Automatic_{solver}.csv")
        automatic_res = matrix_processing(automatic)[0][measure]
        automatic_rep = matrix_processing(automatic)[1]
        matrix = np.vstack((matrix,automatic_res))
        success = np.vstack((success,automatic_rep))

    if "B" in selected:
        barrier = pd.read_csv(f"results\\barrier\\Barrier_{solver}.csv")
        barrier_res = matrix_processing(barrier)[0][measure]
        barrier_rep = matrix_processing(barrier)[1]
        matrix = np.vstack((matrix,barrier_res))
        success = np.vstack((success,barrier_rep))

    if "CB" in selected:
        cross_barrier = pd.read_csv(f"results\\cross_barrier\\Cross_Barrier_{solver}.csv")
        cross_barrier_res = matrix_processing(cross_barrier)[0][measure]
        cross_barrier_rep = matrix_processing(cross_barrier)[1]
        matrix = np.vstack((matrix,cross_barrier_res))
        success = np.vstack((success,cross_barrier_rep))

    if "DS" in selected:
        d_simplex = pd.read_csv(f"results\\simplex_dual\\Simplex_dual_{solver}.csv")
        d_simplex_res = matrix_processing(d_simplex)[0][measure]
        d_simplex_rep = matrix_processing(d_simplex)[1]
        matrix = np.vstack((matrix,d_simplex_res))
        success = np.vstack((success,d_simplex_rep))

    if "PS" in selected:
        p_simplex = pd.read_csv(f"results\\simplex_primal\\Simplex_primal_{solver}.csv")
        p_simplex_res = matrix_processing(p_simplex)[0][measure]
        p_simplex_rep = matrix_processing(p_simplex)[1]
        matrix = np.vstack((matrix,p_simplex_res))
        success = np.vstack((success,p_simplex_rep))

   
    matrix = matrix.T[:,1:]
    success = 100*success[1:,:]

    if to_plot == "Performance Profile" or to_plot == "All":
        best_in_row = (np.amin(matrix,1))

        ratio = np.zeros((matrix.shape[0],matrix.shape[1]))
        for i in range(0,matrix.shape[0]):
            for j in range(0,matrix.shape[1]):
                ratio[i][j] = matrix[i][j]/best_in_row[i]

        print("State tau range for performance profile: ")

        while True:

            i = input()
            
            try: 
                float(i)
                break
            except:
                print("Wrong Input - Must be numerical")

        t = np.arange(1,float(i),float(i)/30)
        
        prob_t = np.zeros((ratio.shape[0],ratio.shape[1],t.shape[0]))
        prob_s = np.zeros((ratio.shape[1],t.shape[0]))
        for j in range(0,ratio.shape[1]):
            for k in range(0,t.shape[0]):
                for i in range(0,ratio.shape[0]):
                    if ratio[i][j]<=t[k]:
                        prob_t[i][j][k] = 1
                prob_s[j][k] = np.sum(prob_t[:,j,k])/ratio.shape[0]

        fig, ax = plt.subplots()
        ax.set_xticks(t)
        ax.grid()

        selected = sorted(selected, key=str.lower)
        ax.plot(t, prob_s[0,:],label=labels[selected[0]])
        ax.plot(t, prob_s[1,:],label=labels[selected[1]])
        
        if len(selected) >=3:
            ax.plot(t, prob_s[2,:],label=labels[selected[2]])

        if len(selected) >=4:
            ax.plot(t,  prob_s[3,:],label=labels[selected[3]])

        if len(selected) >=5:
            ax.plot(t, prob_s[4,:],label=labels[selected[4]])
        
        
        ax.set(xlabel='tau', ylabel='Fraction of problems',
            title=f"Performance Profile of {solver} - Measure {measure}")

        plt.legend(framealpha=1)
        plt.show()

    if measure == "Solver_Time":
        matrix = np.where(matrix >=1900, 1800, matrix)
    problems = pd.read_csv(f"results\\results_true.csv")['Problem']
    if to_plot == "Graph Chart" or to_plot == "All":
       
        t = np.arange(matrix.shape[0])
        fig, ax = plt.subplots()
        ax.plot(t, matrix[:,0],label=labels[selected[0]])
        ax.plot(t, matrix[:,1],label=labels[selected[1]])

        if len(selected) >=3:
            ax.plot(t, matrix[:,2],label=labels[selected[2]])

        if len(selected) >=4:
            ax.plot(t,  matrix[:,3],label=labels[selected[3]])

        if len(selected) >=5:
            ax.plot(t, matrix[:,4],label=labels[selected[4]])

        ax.grid()
        ax.set_xticks(t)
        ax.set_xticklabels(problems,fontsize = 7,rotation = 60)
        ax.set(xlabel='Problem', ylabel='Times (s)',
        title=f'Graph Chart of {solver} - Measure {measure}')
        plt.legend(framealpha=1)
        plt.show()

    if to_plot == "Bar Chart" or to_plot == "All":

        x = np.arange(success.shape[0])
        dx = (np.arange(success.shape[1])-success.shape[1]/2.)/(success.shape[1]+2.)
        d = 1./(success.shape[1]+2.)


        fig, ax=plt.subplots()
        flag = ["Optimal","Time Limit","Infeasible"]
        for i in range(success.shape[1]):
            ax.bar(x+dx[i],success[:,i], width=d,label = flag[i])

        modes = []
        selected = sorted(selected, key=str.lower)
        for i in selected:
            modes.append(labels[i])
        ax.set_xticks(x)
        ax.set_xticklabels(modes,fontsize = 7,rotation = 0)
        ax.set(xlabel='Mode', ylabel='Problem Status (%)',
            title=f'Percentage of status result by Mode')
        plt.legend(framealpha=1)
        plt.show()

elif criteria == "Mode":

    print("State mode to be assessed. Choices : ( Automatic, Barrier , Cross_Barrier , Simplex_dual , Simplex_primal")

    while True:

        x = input()
        
        if x in modes:
            break
        else:
            print("Wrong Input - Try Again")


    if x == "Automatic":
        available = automatic

    elif x == "Barrier":
        available = barrier

    elif x == "Cross_Barrier":
        available = c_barrier

    elif x == "Simplex_dual":
        available = d_simplex
    
    elif x == "Simplex_primal":
        available = p_simplex 

    count = len(available)
    mode = x
    print(f"State number of solvers for comparison. Maximum solver for {mode} are {count}.")

    while True:

        x = input()

        try:
            if int(x) > count:
                print("More solvers than supported: Try again")
            elif int(x)<=1:
                print("At least two solvers must be selected.")
            else:
                break
        except:
            print("Input must be numerical.")
            pass
    
    if int(x) == count:
        print("All solvers were selected.")
        selected = available
    else:
            
        print(f"Select {x} solvers. Available solvers are:")
        
        for i in available:
            print(i)
        
        selected = []
        for i in range (0,int(x)):
            
            while True:
                print(f"Algorithm no.{i+1}")
                print("Type name of algorithm as stated above.")
                y = input()

                if y in available and y not in selected:
                    selected.append(y)
                    break
                else:
                    print("Wrong Input. Keyword was wrong, already selected or not available.")
    
    matrix = np.zeros([35,])
    success = np.zeros([3,])

    if "Clp" in selected:

        clp = pd.read_csv(f"results\\{mode.lower()}\\{mode}_Clp.csv")
        clp_res = matrix_processing(clp)[0][measure]
        clp_rep = matrix_processing(clp)[1]
        matrix = np.vstack((matrix,clp_res))
        success = np.vstack((success,clp_rep))

    if "FICO_Xpress" in selected:

        fico_xpress = pd.read_csv(f"results\\{mode.lower()}\\{mode}_FICO_Xpress.csv")
        fico_xpress_res = matrix_processing(fico_xpress)[0][measure]
        fico_xpress_rep = matrix_processing(fico_xpress)[1]
        matrix = np.vstack((matrix,fico_xpress_res))
        success = np.vstack((success,fico_xpress_rep))

    if "GuRoBi" in selected:

        gurobi = pd.read_csv(f"results\\{mode.lower()}\\{mode}_GuRoBi.csv")
        gurobi_res = matrix_processing(gurobi)[0][measure]
        gurobi_rep = matrix_processing(gurobi)[1]
        matrix = np.vstack((matrix,gurobi_res))
        success = np.vstack((success,gurobi_rep))

    if "HiGHS" in selected:

        highs = pd.read_csv(f"results\\{mode.lower()}\\{mode}_HiGHS.csv")
        highs_res = matrix_processing(highs)[0][measure]
        highs_rep = matrix_processing(highs)[1]
        matrix = np.vstack((matrix,highs_res))
        success = np.vstack((success,highs_rep))


    if "IBM_CPLEX" in selected:

        ibm_cplex = pd.read_csv(f"results\\{mode.lower()}\\{mode}_IBM_CPLEX.csv")
        ibm_cplex_res = matrix_processing(ibm_cplex)[0][measure]
        ibm_cplex_rep = matrix_processing(ibm_cplex)[1]
        matrix = np.vstack((matrix,ibm_cplex_res))
        success = np.vstack((success,ibm_cplex_rep))

    if "Mosek" in selected:

        mosek = pd.read_csv(f"results\\{mode.lower()}\\{mode}_Mosek.csv")
        mosek_res = matrix_processing(mosek)[0][measure]
        mosek_rep = matrix_processing(mosek)[1]
        matrix = np.vstack((matrix,mosek_res))
        success = np.vstack((success,mosek_rep))

    if "Tulip" in selected:

        tulip = pd.read_csv(f"results\\{mode.lower()}\\{mode}_Tulip.csv")
        tulip_res = matrix_processing(tulip)[0][measure]
        tulip_rep = matrix_processing(tulip)[1]
        matrix = np.vstack((matrix,tulip_res))
        success = np.vstack((success,tulip_rep))

  
    matrix = matrix.T[:,1:]
    success = 100*success[1:,:]

    if to_plot == "Performance Profile" or to_plot == "All":
        best_in_row = (np.amin(matrix,1))

        ratio = np.zeros((matrix.shape[0],matrix.shape[1]))
        for i in range(0,matrix.shape[0]):
            for j in range(0,matrix.shape[1]):
                ratio[i][j] = matrix[i][j]/best_in_row[i]

        print("State tau range for performance profile: ")

        while True:

            i = input()
            
            try: 
                float(i)
                break
            except:
                print("Wrong Input - Must be numerical")

        t = np.arange(1,float(i),float(i)/30)
        
        prob_t = np.zeros((ratio.shape[0],ratio.shape[1],t.shape[0]))
        prob_s = np.zeros((ratio.shape[1],t.shape[0]))
        for j in range(0,ratio.shape[1]):
            for k in range(0,t.shape[0]):
                for i in range(0,ratio.shape[0]):
                    if ratio[i][j]<=t[k]:
                        prob_t[i][j][k] = 1
                prob_s[j][k] = np.sum(prob_t[:,j,k])/ratio.shape[0]

        fig, ax = plt.subplots()
        ax.set_xticks(t)
        ax.grid()

        selected = sorted(selected, key=str.lower)
        ax.plot(t, prob_s[0,:],label=selected[0])
        ax.plot(t, prob_s[1,:],label=selected[1])
        
        if len(selected) >=3:
            ax.plot(t, prob_s[2,:],label=selected[2])

        if len(selected) >=4:
            ax.plot(t,  prob_s[3,:],label=selected[3])

        if len(selected) >=5:
            ax.plot(t, prob_s[4,:],label=selected[4])

        if len(selected) >=6:
            ax.plot(t,  prob_s[5,:],label=selected[3])

        if len(selected) >=7:
            ax.plot(t, prob_s[6,:],label=selected[4])        
        
        ax.set(xlabel='tau', ylabel='Fraction of problems',
            title=f"Performance Profile of {mode} - Measure {measure}")

        plt.legend(framealpha=1)
        plt.show()

    if measure == "Solver_Time":
        matrix = np.where(matrix >=1900, 1800, matrix)
    problems = pd.read_csv(f"results\\results_true.csv")['Problem']
    if to_plot == "Graph Chart" or to_plot == "All":
       
        t = np.arange(matrix.shape[0])
        fig, ax = plt.subplots()
        ax.plot(t, matrix[:,0],label=selected[0])
        ax.plot(t, matrix[:,1],label=selected[1])

        if len(selected) >=3:
            ax.plot(t, matrix[:,2],label=selected[2])

        if len(selected) >=4:
            ax.plot(t,  matrix[:,3],label=selected[3])

        if len(selected) >=5:
            ax.plot(t, matrix[:,4],label=selected[4])

        if len(selected) >=6:
            ax.plot(t, matrix[:,5],label=selected[5])
        
        if len(selected) >=7:
            ax.plot(t, matrix[:,6],label=selected[6])

        ax.grid()
        ax.set_xticks(t)
        ax.set_xticklabels(problems,fontsize = 7,rotation = 60)
        ax.set(xlabel='Problem', ylabel='Times (s)',
        title=f'Graph Chart of {mode} - Measure {measure}')
        plt.legend(framealpha=1)
        plt.show()

    if to_plot == "Bar Chart" or to_plot == "All":

        x = np.arange(success.shape[0])
        dx = (np.arange(success.shape[1])-success.shape[1]/2.)/(success.shape[1]+2.)
        d = 1./(success.shape[1]+2.)


        fig, ax=plt.subplots()
        flag = ["Optimal","Time Limit","Infeasible"]
        for i in range(success.shape[1]):
            ax.bar(x+dx[i],success[:,i], width=d,label = flag[i])

        selected = sorted(selected, key=str.lower)

        ax.set_xticks(x)
        ax.set_xticklabels(selected,fontsize = 7,rotation = 0)
        ax.set(xlabel='Mode', ylabel='Problem Status (%)',
            title=f'Percentage of status result by Solver')
        plt.legend(framealpha=1)
        plt.show()