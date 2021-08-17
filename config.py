import argparse

def get_config():

    # Creating configuration file
    parser = argparse.ArgumentParser(description='Configuration file for Benchmarking Plots Gerneration.')

    # Required Input for loader.py and main.py
    group = parser.add_argument_group('Required Arguments (Marked with asterisk)')
    group.add_argument('-i','--info', type=str,metavar='*', required=True, help = 'The examined city. Required information - \
       Accepted Vaslues : (table, profile, chart)')
    group.add_argument('-m','--metric', type=str,metavar='*', required=True, help = 'Examined Metric - \
       Accepted Vaslues : (Solver_Time, Julia_Time, Iterations)')

    # Required argument if info = tables
    group = parser.add_argument_group('Table requirements')
    group.add_argument('-tm', '--table_mode', type=str, metavar='*',default='Automatic', help = 'Which mode requires table generation.\
        Default value is Automatic - Accepted Values (Cross_Barrier,Barrier,Automatic,Simplex_dual,Simplex_primal). ')
    group.add_argument('-l', '--loops',type=int, metavar='', nargs='?',default=1, help = 'No.loops')

    # Required argument if info = profile
    group = parser.add_argument_group('Performance Profile requirements')
    group.add_argument('-pm', '--profile_mode', type=str, metavar='*',default='by_Solver', help = 'Performance Profile mode.\
        Default value is by_Solver - Accepted Values (by_Solver,by_Mode). ')
    group.add_argument('-t', '--tau', type=int, metavar='', nargs='?',default=1000, help = 'Tau for performance profile')
    group.add_argument('-lsc', '--log_scale', type=str, metavar='*',default='True', help = 'Flag that determines whether use log scale')
    
    # Required argument if info = chart
    group = parser.add_argument_group('Chart requirements')
    group.add_argument('-cm', '--chart_mode', type=str, metavar='*',default='Automatic', help = 'Which mode requires chart generation.\
        Default value is Automatic - Accepted Values (Cross_Barrier,Barrier,Automatic,Simplex_dual,Simplex_primal). ')


    return parser.parse_args()