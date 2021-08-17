import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import get_config
from scipy.stats.mstats import gmean
import matplotlib.ticker as ticker
import math

args = get_config()
correct = pd.read_csv("results//results_true.csv").values[:,2]

# Automatic Solvers
global automatic
automatic = ["Clp", "FICO_Xpress", "GuRoBi", "IBM_CPLEX", "HiGHS", "Mosek", "Tulip"]

# Barrier Solvers - No Crossover
global barrier
barrier = ["FICO_Xpress", "GuRoBi", "IBM_CPLEX", "Mosek", "Tulip"]

# Barrier Solver - Crossover
global c_barrier
c_barrier = ["FICO_Xpress", "GuRoBi", "IBM_CPLEX", "Mosek"]

# Primal Simplex Solvers
global p_simplex
p_simplex = ["Clp", "FICO_Xpress", "GuRoBi", "IBM_CPLEX", "Mosek"]

# Primal Simplex Solvers
global d_simplex
d_simplex = ["Clp", "FICO_Xpress", "GuRoBi", "IBM_CPLEX", "HiGHS", "Mosek"]

global modes
modes = ["Automatic", "Barrier", "Cross_Barrier", "Simplex_dual", "Simplex_primal"]

global labels
labels = {"A": "Automatic", "B": "Interior-Point Method without Crossover","CB": "Interior-Point Method with Crossover",
          "PS": "Primal Simplex", "DS": "Dual Simplex",}

def str2bool(v):
  return v.lower() in ("yes", "true", "t","1")

def matrix_processing (x):


    for index, row in x.iterrows():
        if np.isclose(row["Obj_Value"],correct[index],rtol=1e-02):
            pass
        elif row["Status"] == "Time Limit":
            pass
        else:
            x.loc[index,'Status']= "Fail"


    x = x.drop([0])
    rows = x.values.shape[0]
    report = x["Status"].value_counts()
    optimal = report["Optimal"]/rows
    
    try:
        time_limit = report["Time Limit"]/rows
    except:
        time_limit = 0 

    try:
        fails = report["Fail"]/rows
    except:
        fails = 0

    for i in metrics:
        x.loc[(x.Status == 'Time Limit'),i]= np.inf
        x.loc[(x.Status == 'Fail'),i]= np.inf
        x.loc[(x.Solver_Time == 0),i]= 0.0001
    report = [optimal,time_limit,fails] 
    return x,report

def num_status(df):
    b = df.values[:,1]  
    for i in range(0,df.shape[0]):
        if b[i] == "Optimal":
            b[i] = 0
        elif b[i] == "Time Limit":
           b[i] = 1
        else:
           b[i] = 2
    df['num_status'] = b
    return df

def assert_opt(df1,df2):
    b = df1.values[:,-1]
    a = df1.values[:,2]
    a = np.array(a, dtype=float)
    for i in range(0,df1.shape[0]):
        if np.isclose(a[i],df2[i],rtol=1e-02):
            pass
        elif b[i] !=0:
            pass
        else:
            b[i] = 2
    df1['num_status'] = b
    return df1

def metric_col(df,metric):

    b = list(range(0,df.shape[0]))
    m = df[metric].values
    for i in range(0,df.shape[0]):
        if df.values[i,-1] == 0:
            b[i] = int(math.ceil(m[i]))
        elif df.values[i,-1] == 1:
            b[i] = 't'
        else:
            b[i] = 'f'

    return b,m

def solved(df,solver):
    
    try:
        time_limit = df[solver].value_counts().t
    except:
        time_limit = 0
    
    try:
        fails = df[solver].value_counts().f
    except:
        fails = 0
    

    opt = df.shape[0] - time_limit - fails
    

    return [opt, time_limit, fails]

metrics = ["Solver_Time","Julia_Time","Iterations"]

if args.metric in metrics:
        
    if args.info == "table":
        
        tot = np.ones((correct.shape[0]-1,1))
        count = 1
        for i in range(args.loops):
            
            modes = ['Automatic','Barrier','Cross_Barrier','Simplex_dual','Simplex_primal']
            if args.table_mode in modes:
                
                # Clp
                if args.table_mode != "Barrier" and args.table_mode != "Cross_Barrier":
                    clp = pd.read_csv(f"results//{args.table_mode.lower()}//{args.table_mode}_Clp.csv")
                    clp = num_status(clp)
                    clp = (assert_opt(clp,correct))
                    clp_col = (metric_col(clp,args.metric))[0]
                    clp_it = (metric_col(clp,args.metric))[1]

                # FICO Xpress
                xpress = pd.read_csv(f"results//{args.table_mode.lower()}//{args.table_mode}_FICO_Xpress.csv")
                xpress = num_status(xpress)
                xpress = (assert_opt(xpress,correct))
                xpress_col  = (metric_col(xpress,args.metric))[0]
                xpress_it = (metric_col(xpress,args.metric))[1]

                # GuRoBi
                gurobi = pd.read_csv(f"results//{args.table_mode.lower()}//{args.table_mode}_GuRoBi.csv")
                gurobi = num_status(gurobi)
                gurobi = (assert_opt(gurobi,correct))
                gurobi_col  = (metric_col(gurobi,args.metric))[0]
                gurobi_it = (metric_col(gurobi,args.metric))[1]

                # IBM_CPLEX
                cplex = pd.read_csv(f"results//{args.table_mode.lower()}//{args.table_mode}_IBM_CPLEX.csv")
                cplex = num_status(cplex)
                cplex = (assert_opt(cplex,correct))
                cplex_col  = (metric_col(cplex,args.metric))[0]
                cplex_it = (metric_col(cplex,args.metric))[1]

                # HiGHS
                if args.table_mode != "Barrier" and args.table_mode != "Cross_Barrier" and args.table_mode != "Simplex_primal":
                    highs = pd.read_csv(f"results//{args.table_mode.lower()}//{args.table_mode}_HiGHS.csv")
                    highs = num_status(highs)
                    highs = (assert_opt(highs,correct))
                    highs_col  = (metric_col(highs,args.metric))[0]
                    highs_it = (metric_col(highs,args.metric))[1]

                # Mosek
                mosek = pd.read_csv(f"results//{args.table_mode.lower()}//{args.table_mode}_Mosek.csv")
                mosek = num_status(mosek)
                mosek = (assert_opt(mosek,correct))
                mosek_col = (metric_col(mosek,args.metric))[0]
                mosek_it = (metric_col(mosek,args.metric))[1]

                # Tulip
                if args.table_mode != "Simplex_dual" and args.table_mode != "Cross_Barrier" and args.table_mode != "Simplex_primal":
                    tulip = pd.read_csv(f"results//{args.table_mode.lower()}//{args.table_mode}_Tulip.csv")
                    tulip = num_status(tulip)
                    tulip = (assert_opt(tulip,correct))
                    tulip_col = (metric_col(tulip,args.metric))[0]
                    tulip_it = (metric_col(tulip,args.metric))[1]

                # Cumulative Table
                res_table = pd.DataFrame()
                it_table = pd.DataFrame()

                res_table["Problems"] = gurobi["Problem"]
                it_table["Problems"] = gurobi["Problem"]

                if args.table_mode != "Barrier" and args.table_mode != "Cross_Barrier":
                    res_table["Clp"] = clp_col
                    it_table["Clp"] = clp_it

                res_table["FICO_Xpress"] = xpress_col
                it_table["FICO_Xpress"] = xpress_it
                res_table["GuRoBi"] = gurobi_col
                it_table["GuRoBi"] = gurobi_it
                res_table["IBM_CPLEX"] = cplex_col
                it_table["IBM_CPLEX"] = cplex_it

                if args.table_mode != "Barrier" and args.table_mode != "Cross_Barrier" and args.table_mode != "Simplex_primal":
                    res_table["HiGHS"] = highs_col
                    it_table["HiGHS"] = highs_it

                res_table["Mosek"] = mosek_col
                it_table["Mosek"] = mosek_it

                if args.table_mode != "Simplex_dual" and args.table_mode != "Cross_Barrier" and args.table_mode != "Simplex_primal":
                    res_table["Tulip"] = tulip_col
                    it_table["Tulip"] = tulip_it
                
                res_table = res_table.drop([0])
                it_table = it_table.drop([0])

                # Status Table
                status = pd.DataFrame()
                status['status'] = ["Optimal","Time Limit","Fail"]

                if args.table_mode != "Barrier" and args.table_mode != "Cross_Barrier":
                    status["Clp"] = solved(res_table,'Clp')
                
                status["FICO_Xpress"] = solved(res_table,'FICO_Xpress')
                status["GuRoBi"] = solved(res_table,'GuRoBi')
                status["IBM_CPLEX"] = solved(res_table,'IBM_CPLEX')

                if args.table_mode != "Barrier" and args.table_mode != "Cross_Barrier" and args.table_mode != "Simplex_primal":
                    status["HiGHS"] = solved(res_table,'HiGHS')

                status["Mosek"] = solved(res_table,'Mosek')

                if args.table_mode != "Simplex_dual" and args.table_mode != "Cross_Barrier" and args.table_mode != "Simplex_primal":
                    status["Tulip"] = solved(res_table,'Tulip')

                # Geometric Mean

                if args.metric =="Solver_Time":
                    res_mod = res_table.replace(["t","f"], 1800)
                elif args.metric =="Julia_Time":
                    res_mod = res_table.replace("f", 1800)
                    res_mod = res_mod.replace("t", -1)
                else:
                    res_mod = it_table
                
                if args.metric =="Julia_Time":
                    res_mod = pd.concat([res_mod, it_table]).max(level=0)
            
                mod_np = res_mod.values[:,1:]
                ones = np.ones((mod_np.shape[0],mod_np.shape[1]))
                mod = (np.maximum(ones,mod_np+10))
                mod = np.array(mod,dtype=float)
                mod = np.log(mod)/res_mod.shape[0]
                unsc_geom_mean = np.exp((np.sum(mod,axis=0)))-10
                sc_geom_mean = unsc_geom_mean/np.min(unsc_geom_mean)
                geom= np.vstack((unsc_geom_mean,sc_geom_mean))

                # Cumulative Status tables
                g = pd.DataFrame()
                g["status"] = ["Unscaled Geometric Mean","Scaled Geometric Mean"]

                if args.table_mode == 'Automatic':
                    g["Clp"] = geom[:,0]
                    g["FICO_Xpress"] = geom[:,1]
                    g["GuRoBi"] = geom[:,2]
                    g["IBM_CPLEX"] = geom[:,3]
                    g["HiGHS"] = geom[:,4]
                    g["Mosek"] = geom[:,5]
                    g["Tulip"] = geom[:,6]
                
                elif args.table_mode == 'Barrier':
                    g["FICO_Xpress"] = geom[:,0]
                    g["GuRoBi"] = geom[:,1]
                    g["IBM_CPLEX"] = geom[:,2]
                    g["Mosek"] = geom[:,3]
                    g["Tulip"] = geom[:,4]

                elif args.table_mode == 'Cross_Barrier':
                    g["FICO_Xpress"] = geom[:,0]
                    g["GuRoBi"] = geom[:,1]
                    g["IBM_CPLEX"] = geom[:,2]
                    g["Mosek"] = geom[:,3]

                elif args.table_mode == 'Simplex_dual':
                    g["Clp"] = geom[:,0]
                    g["FICO_Xpress"] = geom[:,1]
                    g["GuRoBi"] = geom[:,2]
                    g["IBM_CPLEX"] = geom[:,3]
                    g["HiGHS"] = geom[:,4]
                    g["Mosek"] = geom[:,5]

                elif args.table_mode == 'Simplex_primal':
                    g["Clp"] = geom[:,0]
                    g["FICO_Xpress"] = geom[:,1]
                    g["GuRoBi"] = geom[:,2]
                    g["IBM_CPLEX"] = geom[:,3]
                    g["Mosek"] = geom[:,4]

                status = pd.concat([g, status], sort=False)
            
                status.to_csv(f'tables//{args.table_mode}_{args.metric}_stats.csv', index=False)
                print(status)
                res_table.to_csv(f'tables//{args.table_mode}_{args.metric}_results.csv', index=False)
                print(res_table)
                tot=np.hstack([tot,res_mod.values[:,1:]])

                if count < args.loops:
                    print(f"State mode for loop {i+1}. Choices : ( Automatic, Barrier , Cross_Barrier , Simplex_dual , Simplex_primal")
                    mode = input()
                    args.table_mode = mode
                    

                if count == args.loops and count!= 1:
                    tot = tot[:,1:]
                    minims = (np.argmin(tot, axis=1))
                    best_alg = []
                    for i in minims:
                        if i < 11:
                            best_alg.append("any_simplex")
                        else:
                            best_alg.append("IPM")
                    print(best_alg.count("any_simplex"))
                    print(minims)
                    print(tot)
                    break
                
                
                count+=1

            else:
                print("Wrong keyword for table mode. Check help. Exiting")

    elif args.info == "profile":

        if args.profile_mode == "by_Solver":

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
                automatic_res = matrix_processing(automatic)[0][args.metric]
                automatic_rep = matrix_processing(automatic)[1]
                matrix = np.vstack((matrix,automatic_res))
                success = np.vstack((success,automatic_rep))

            if "B" in selected:
                barrier = pd.read_csv(f"results\\barrier\\Barrier_{solver}.csv")
                barrier_res = matrix_processing(barrier)[0][args.metric]
                barrier_rep = matrix_processing(barrier)[1]
                matrix = np.vstack((matrix,barrier_res))
                success = np.vstack((success,barrier_rep))

            if "CB" in selected:
                cross_barrier = pd.read_csv(f"results\\cross_barrier\\Cross_Barrier_{solver}.csv")
                cross_barrier_res = matrix_processing(cross_barrier)[0][args.metric]
                cross_barrier_rep = matrix_processing(cross_barrier)[1]
                matrix = np.vstack((matrix,cross_barrier_res))
                success = np.vstack((success,cross_barrier_rep))

            if "DS" in selected:
                d_simplex = pd.read_csv(f"results\\simplex_dual\\Simplex_dual_{solver}.csv")
                d_simplex_res = matrix_processing(d_simplex)[0][args.metric]
                d_simplex_rep = matrix_processing(d_simplex)[1]
                matrix = np.vstack((matrix,d_simplex_res))
                success = np.vstack((success,d_simplex_rep))

            if "PS" in selected:
                p_simplex = pd.read_csv(f"results\\simplex_primal\\Simplex_primal_{solver}.csv")
                p_simplex_res = matrix_processing(p_simplex)[0][args.metric]
                p_simplex_rep = matrix_processing(p_simplex)[1]
                matrix = np.vstack((matrix,p_simplex_res))
                success = np.vstack((success,p_simplex_rep))

        
            matrix = matrix.T[:,1:]
            success = 100*success[1:,:]

            best_in_row = (np.amin(matrix,1))

            ratio = np.zeros((matrix.shape[0],matrix.shape[1]))
            for i in range(0,matrix.shape[0]):
                for j in range(0,matrix.shape[1]):
                    ratio[i][j] = matrix[i][j]/best_in_row[i]


            t = np.arange(1,float(args.tau),float(args.tau)/3000)
            
            prob_t = np.zeros((ratio.shape[0],ratio.shape[1],t.shape[0]))
            prob_s = np.zeros((ratio.shape[1],t.shape[0]))
            for j in range(0,ratio.shape[1]):
                for k in range(0,t.shape[0]):
                    for i in range(0,ratio.shape[0]):
                        if ratio[i][j]<=t[k]:
                            prob_t[i][j][k] = 1
                    prob_s[j][k] = np.sum(prob_t[:,j,k])/ratio.shape[0]

            fig, ax = plt.subplots()
            ax.grid()

            selected = sorted(selected, key=str.lower)
            ax.plot(t, (prob_s[0,:]),label=labels[selected[0]])
            ax.plot(t, (prob_s[1,:]),label=labels[selected[1]])
            
            if len(selected) >=3:
                ax.plot(t, (prob_s[2,:]),label=labels[selected[2]])

            if len(selected) >=4:
                ax.plot(t,  (prob_s[3,:]),label=labels[selected[3]])

            if len(selected) >=5:
                ax.plot(t, (prob_s[4,:]),label=labels[selected[4]])
            
            if str2bool(args.log_scale):
                ax.set_xscale('log')
                plt.xscale('log',base=2) 
                ax.xaxis.set_major_formatter(ticker.ScalarFormatter())

            if solver == "IBM_CPLEX":
                solver = "CPLEX"

            if solver == "FICO_Xpress":
                solver = "Xpress"            

            if args.metric != "Iterations":
                x = args.metric.split("_")

                ax.set(xlabel='tau', ylabel='Fraction of problems',
                    title=f"Performance Profile of {solver} - Measure {x[0]} {x[1]}")

                plt.legend(framealpha=1)
                plt.show()
            else:

                ax.set(xlabel='tau', ylabel='Fraction of problems',
                    title=f"Performance Profile of {solver} - Measure {args.metric}")
                plt.legend(framealpha=1)
                plt.show()

        elif args.profile_mode == "by_Mode":
                    
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
                clp_res = matrix_processing(clp)[0][args.metric]
                clp_rep = matrix_processing(clp)[1]
                matrix = np.vstack((matrix,clp_res))
                success = np.vstack((success,clp_rep))

            if "FICO_Xpress" in selected:

                fico_xpress = pd.read_csv(f"results\\{mode.lower()}\\{mode}_FICO_Xpress.csv")
                fico_xpress_res = matrix_processing(fico_xpress)[0][args.metric]
                fico_xpress_rep = matrix_processing(fico_xpress)[1]
                matrix = np.vstack((matrix,fico_xpress_res))
                success = np.vstack((success,fico_xpress_rep))

            if "GuRoBi" in selected:

                gurobi = pd.read_csv(f"results\\{mode.lower()}\\{mode}_GuRoBi.csv")
                gurobi_res = matrix_processing(gurobi)[0][args.metric]
                gurobi_rep = matrix_processing(gurobi)[1]
                matrix = np.vstack((matrix,gurobi_res))
                success = np.vstack((success,gurobi_rep))

            if "HiGHS" in selected:

                highs = pd.read_csv(f"results\\{mode.lower()}\\{mode}_HiGHS.csv")
                highs_res = matrix_processing(highs)[0][args.metric]
                highs_rep = matrix_processing(highs)[1]
                matrix = np.vstack((matrix,highs_res))
                success = np.vstack((success,highs_rep))


            if "IBM_CPLEX" in selected:

                ibm_cplex = pd.read_csv(f"results\\{mode.lower()}\\{mode}_IBM_CPLEX.csv")
                ibm_cplex_res = matrix_processing(ibm_cplex)[0][args.metric]
                ibm_cplex_rep = matrix_processing(ibm_cplex)[1]
                matrix = np.vstack((matrix,ibm_cplex_res))
                success = np.vstack((success,ibm_cplex_rep))

            if "Mosek" in selected:

                mosek = pd.read_csv(f"results\\{mode.lower()}\\{mode}_Mosek.csv")
                mosek_res = matrix_processing(mosek)[0][args.metric]
                mosek_rep = matrix_processing(mosek)[1]
                matrix = np.vstack((matrix,mosek_res))
                success = np.vstack((success,mosek_rep))

            if "Tulip" in selected:

                tulip = pd.read_csv(f"results\\{mode.lower()}\\{mode}_Tulip.csv")
                tulip_res = matrix_processing(tulip)[0][args.metric]
                tulip_rep = matrix_processing(tulip)[1]
                matrix = np.vstack((matrix,tulip_res))
                success = np.vstack((success,tulip_rep))

        
            matrix = matrix.T[:,1:]
            success = 100*success[1:,:]

            best_in_row = (np.amin(matrix,1))

            ratio = np.zeros((matrix.shape[0],matrix.shape[1]))
            for i in range(0,matrix.shape[0]):
                for j in range(0,matrix.shape[1]):
                    ratio[i][j] = matrix[i][j]/best_in_row[i]

            t = np.arange(1,float(args.tau),float(args.tau)/3000)
            
            prob_t = np.zeros((ratio.shape[0],ratio.shape[1],t.shape[0]))
            prob_s = np.zeros((ratio.shape[1],t.shape[0]))
            for j in range(0,ratio.shape[1]):
                for k in range(0,t.shape[0]):
                    for i in range(0,ratio.shape[0]):
                        if ratio[i][j]<=t[k]:
                            prob_t[i][j][k] = 1
                    prob_s[j][k] = np.sum(prob_t[:,j,k])/ratio.shape[0]

            fig, ax = plt.subplots()
            ax.grid()


            selected = sorted(selected, key=str.lower)

            for n, i in enumerate(selected):
                if i == "FICO_Xpress":
                    selected[n] = "Xpress"
                if i == "IBM_CPLEX":
                    selected[n] = "CPLEX"   
                    
            ax.plot(t, prob_s[0,:],label=selected[0])
            ax.plot((t), prob_s[1,:],label=selected[1])
            
            if len(selected) >=3:
                ax.plot((t), prob_s[2,:],label=selected[2])

            if len(selected) >=4:
                ax.plot((t),  prob_s[3,:],label=selected[3])

            if len(selected) >=5:
                ax.plot((t), prob_s[4,:],label=selected[4])

            if len(selected) >=6:
                ax.plot((t),  prob_s[5,:],label=selected[5])

            if len(selected) >=7:
                ax.plot((t), prob_s[6,:],label=selected[6])        

            if str2bool(args.log_scale):
                ax.set_xscale('log')
                plt.xscale('log',base=2)

                ax.xaxis.set_major_formatter(ticker.ScalarFormatter())

            if mode == "Simplex_dual":
                mode = "Dual Simplex"

            if mode == "Simplex_primal":
                mode = "Primal Simplex"            

            if mode == "Cross_Barrier":
                mode = "Interior-Point Method with Crossover" 

            if mode == "Barrier":
                mode = "Interior-Point Method without Crossover" 

            if args.metric != "Iterations":
                x = args.metric.split("_")

                ax.set(xlabel='tau', ylabel='Fraction of problems',
                    title=f"Performance Profile of {mode} - Measure {x[0]} {x[1]}")

                plt.legend(framealpha=1)
                plt.show()
            else:

                ax.set(xlabel='tau', ylabel='Fraction of problems',
                    title=f"Performance Profile of {mode} - Measure {args.metric}")

                plt.legend(framealpha=1)
                plt.show()
            
        else:
            print("Wrong Profile Mode. Check help. Exiting")

    elif args.info == "chart":
               
        modes = ['Automatic','Barrier','Cross_Barrier','Simplex_dual','Simplex_primal']
        if args.chart_mode in modes:
            
            # Clp
            if args.chart_mode != "Barrier" and args.chart_mode != "Cross_Barrier":
                clp = pd.read_csv(f"results//{args.chart_mode.lower()}//{args.chart_mode}_Clp.csv")
                clp = num_status(clp)
                clp = (assert_opt(clp,correct))
                clp_col = (metric_col(clp,args.metric))[0]
                clp_it = (metric_col(clp,args.metric))[1]

            # FICO Xpress
            xpress = pd.read_csv(f"results//{args.chart_mode.lower()}//{args.chart_mode}_FICO_Xpress.csv")
            xpress = num_status(xpress)
            xpress = (assert_opt(xpress,correct))
            xpress_col  = (metric_col(xpress,args.metric))[0]
            xpress_it = (metric_col(xpress,args.metric))[1]

            # GuRoBi
            gurobi = pd.read_csv(f"results//{args.chart_mode.lower()}//{args.chart_mode}_GuRoBi.csv")
            gurobi = num_status(gurobi)
            gurobi = (assert_opt(gurobi,correct))
            gurobi_col  = (metric_col(gurobi,args.metric))[0]
            gurobi_it = (metric_col(gurobi,args.metric))[1]

            # IBM_CPLEX
            cplex = pd.read_csv(f"results//{args.chart_mode.lower()}//{args.chart_mode}_IBM_CPLEX.csv")
            cplex = num_status(cplex)
            cplex = (assert_opt(cplex,correct))
            cplex_col  = (metric_col(cplex,args.metric))[0]
            cplex_it = (metric_col(cplex,args.metric))[1]

            # HiGHS
            if args.chart_mode != "Barrier" and args.chart_mode != "Cross_Barrier" and args.chart_mode != "Simplex_primal":
                highs = pd.read_csv(f"results//{args.chart_mode.lower()}//{args.chart_mode}_HiGHS.csv")
                highs = num_status(highs)
                highs = (assert_opt(highs,correct))
                highs_col  = (metric_col(highs,args.metric))[0]
                highs_it = (metric_col(highs,args.metric))[1]

            # Mosek
            mosek = pd.read_csv(f"results//{args.chart_mode.lower()}//{args.chart_mode}_Mosek.csv")
            mosek = num_status(mosek)
            mosek = (assert_opt(mosek,correct))
            mosek_col = (metric_col(mosek,args.metric))[0]
            mosek_it = (metric_col(mosek,args.metric))[1]

            # Tulip
            if args.chart_mode != "Simplex_dual" and args.chart_mode != "Cross_Barrier" and args.chart_mode != "Simplex_primal":
                tulip = pd.read_csv(f"results//{args.chart_mode.lower()}//{args.chart_mode}_Tulip.csv")
                tulip = num_status(tulip)
                tulip = (assert_opt(tulip,correct))
                tulip_col = (metric_col(tulip,args.metric))[0]
                tulip_it = (metric_col(tulip,args.metric))[1]

            # Cumulative Table
            res_table = pd.DataFrame()
            it_table = pd.DataFrame()

            res_table["Problems"] = gurobi["Problem"]
            it_table["Problems"] = gurobi["Problem"]

            if args.chart_mode != "Barrier" and args.chart_mode != "Cross_Barrier":
                res_table["Clp"] = clp_col
                it_table["Clp"] = clp_it

            res_table["FICO_Xpress"] = xpress_col
            it_table["FICO_Xpress"] = xpress_it
            res_table["GuRoBi"] = gurobi_col
            it_table["GuRoBi"] = gurobi_it
            res_table["IBM_CPLEX"] = cplex_col
            it_table["IBM_CPLEX"] = cplex_it

            if args.chart_mode != "Barrier" and args.chart_mode != "Cross_Barrier" and args.chart_mode != "Simplex_primal":
                res_table["HiGHS"] = highs_col
                it_table["HiGHS"] = highs_it

            res_table["Mosek"] = mosek_col
            it_table["Mosek"] = mosek_it

            if args.chart_mode != "Simplex_dual" and args.chart_mode != "Cross_Barrier" and args.chart_mode != "Simplex_primal":
                res_table["Tulip"] = tulip_col
                it_table["Tulip"] = tulip_it
            
            res_table = res_table.drop([0])
            it_table = it_table.drop([0])

            if args.metric!="Iterations":
                res_mod = res_table.replace(["t","f","i",'e'], 1800)
            else:
                res_mod = it_table

            res_mod['Gmean'] = gmean(res_mod.iloc[:,1:],axis=1)

            best = (res_mod.min(axis=1))

            avg = (res_mod['Gmean'].values)

            print(f"State solver for comparison to the baseline.")

            while True:
                x = input()

                if x in res_mod.columns[1:]:
                    break
                else:
                    print(f"Solver not available in this mode or wrong entry. Try again.")
            
            examined = res_mod[x].values

            t = np.arange(res_mod.values.shape[0])
            fig, ax = plt.subplots()
            ax.plot(t, best,label="Best")
            ax.plot(t, examined,label=f"{x}")
            ax.plot(t, avg,label="Average (Geometric Mean) ")

            ax.grid()
            ax.set_xticks(t)
            ax.set_xticklabels(res_table['Problems'],fontsize = 7,rotation = 60)

            if args.chart_mode == "Automatic":
                mode = "Automatic"


            if args.chart_mode == "Simplex_dual":
                mode = "Dual Simplex"

            if args.chart_mode == "Simplex_primal":
                mode = "Primal Simplex"            

            if args.chart_mode == "Cross_Barrier":
                mode = "Interior-Point Method with Crossover" 

            if args.chart_mode == "Barrier":
                mode = "Interior-Point Method without Crossover" 

            if args.metric != "Iterations":
                x = args.metric.split("_")

                ax.set(xlabel='Problem', ylabel=f'{x[0]} {x[1]}',
                title=f'Graph Chart of {mode} - Measure {x[0]} {x[1]}')

            else:

                ax.set(xlabel='Problem', ylabel=f'{args.metric}',
                title=f'Graph Chart of {args.chart_mode} - Measure {args.metric}')

            plt.legend(framealpha=1)
            plt.show()

    else:
        print("Wrong Information. Check help. Exiting")

else:
    print("Wrong Metric. Check help. Exiting")