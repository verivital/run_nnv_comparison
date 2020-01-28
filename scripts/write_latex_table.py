import os
import numpy as np
import batch_config as cfg
import subprocess

file_mara = cfg.path_logs + 'logs_mara/results_p'
file_dnc = cfg.path_logs + 'logs_dnc/results_p'
file_reluval = cfg.path_logs + 'logs_reluval/results_p'
file_nnv_star = cfg.path_logs + 'logs_nnv_star/P'
file_nnv_star_appr = cfg.path_logs + 'logs_nnv_star_appr/P'
file_nnv_abs = cfg.path_logs + 'logs_nnv_abs/P'
file_nnv_zono = cfg.path_logs + 'logs_nnv_zono/P'

# check if a program exists on path (for matlab here)
def is_tool(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True

def get_data_mara(mara):
    try:
        f = open(mara, 'r')
        contents = f.readlines()
        f.close()
        result=''
        try:
            idx = len(contents) - 1 - contents[::-1].index('\t--- Time Statistics ---\n')
            i0= 21
            value = ''
            for n in range(i0, len(contents[idx + 1])):
                if contents[idx + 1][n] == 'm':
                    break
                else:
                    value = value+contents[idx + 1][n]

            value = str(int(value)/1000)
        except:
            value = '0.0'

        if 'SAT\n' in contents:
            result = 'SAT'
        elif 'UNSAT\n' in contents:
            result = 'UNSAT'
        else:
            result = 'UNKOWN'

        return value, result
    except:
        print("ERROR: marabou parse failure")
        return '0', 'ERR'

def get_data_dnc(dnc):
    try:
        f = open(dnc, 'r')
        contents = f.readlines()
        f.close()
        value =''
        result=''
        for e in contents[::-1]:
            if e[:11]=='Total Time:':
                value = e[11:-1]
                break
        if value=='':
            value = '0'

        if ('DnCManager::solve SAT query\n' in contents) or ('SAT\n' in contents):
            result = 'SAT'
        elif ('DnCManager::solve UNSAT query\n' in contents) or ('UNSAT\n' in contents):
            result = 'UNSAT'
        else:
            result = 'UNKNOWN'

        return value, result
    except:
        print("ERROR: marabou dnc result parse failure")
        return '0', 'ERR'

def get_data_reluval(reluval):
    try:
        f = open(reluval, 'r')
        contents = f.readlines()
        f.close()
        result =''
        if 'adv found:\n' in contents:
            result = 'SAT'
        elif 'No adv!\n' in contents:
            result = 'UNSAT'
        else:
            result = 'UNKNOWN'

        value = ''
        for e in contents[::-1]:
            xx = e[:5]
            if e[:5]=='time:':
                value = e[6:-1]
                break

        return value, result
    except:
        print("ERROR: reluval result parse failure")
        return '0', 'ERR'


def get_data_nnv(nnv):
# TODO: matlab detection with the following not quite right, need to not launch the gui, so probably need to modify to pass in command arguments
# otherwise we can get a stall here as matlab launches the GUI
#    if is_tool('matlab -nodisplay -nodesktop -r'):
    try:
        f = open(nnv, 'r')
        contents = f.readlines()
        f.close()
        result = contents[0][:-1]
        num = contents[1][23:-1]
        value = contents[2][12:-1]
        return num, value, result
    except:
#        print("WARNING: nnv not run, so table results invalid for it")
        print("ERROR: problem parsing nnv results")
        return '0', '0', 'ERR'



def create_str(filename, time_temp, result_temp):
    temp_str = ''
    temp_sat = sum('SAT' == s for s in result_temp)
    temp_unsat = sum('UNSAT' == s for s in result_temp)
    temp_unk = sum('UNKNOWN' == s for s in result_temp)
    time_temp_np = np.array(time_temp)
    time_temp_1h = len(time_temp_np[time_temp_np >= 3600])
    time_temp_2h = len(time_temp_np[time_temp_np >= 7200])
    time_temp_10h = len(time_temp_np[time_temp_np >= 36000])
    time_total = round(sum(time_temp_np),2)

    temp_str = filename + '&' + str(temp_sat) + '&' + str(temp_unsat) + '&' + str(temp_unk) + \
        '&' + str(time_temp_1h) + '&' + str(time_temp_2h) + '&' + str(time_temp_10h) + '&' + str(time_total) +'\\\\ \n'

    return temp_str


property_num = 4
network_n1 = 5
network_n2 = 9
str_temp_head = '\\begin{table}\n'+\
'\\centering\n'+\
'\\renewcommand{\\arraystretch}{1.5}\n'+\
'\\renewcommand{\\tabcolsep}{1.5mm}\n' +\
'\\begin{adjustbox}{angle=0, max width=\\textwidth}\n'+\
'\\begin{tabular}{c|ccccccccccccccc}\n'+\
'\\hline\n'+\
' & \\multicolumn{2}{c|}{\\textbf{Zonotope}} & \\multicolumn{2}{c|}{\\textbf{Abstract Domain}} & \multicolumn{2}{c|}{\\textbf{Marabou}} & \\multicolumn{2}{c|}{\\textbf{Marabou DnC}} & \\multicolumn{2}{c|}{\\textbf{ReluVal}} & \\multicolumn{3}{c|}{\\textbf{NNV Exact Star}} & \\multicolumn{2}{c}{\\textbf{NNV Appr. Star}} \\\\ \\cline{2-16}\n'+\
'\\multirow{-2}{*}{\\textbf{ID}} &  $VT$  & \\multicolumn{1}{c|}{$V$}    &  $VT$  & \\multicolumn{1}{c|}{$V$}    & $VT$    & \\multicolumn{1}{c|}{$V$}   & $VT$    & \\multicolumn{1}{c|}{$V$}   & $VT$   & \\multicolumn{1}{c|}{$V$}  & $N_p$ &  $VT$ & \\multicolumn{1}{c|}{$V$}   &  $VT$     & \\multicolumn{1}{c}{$V$} \\\\ \hline\n'
for p in range(1,property_num+1):
    str_temp = str_temp_head
    for n1 in range(1, network_n1+1):
        for n2 in range(1, network_n2+1):

            mara = file_mara + str(p) + '_n' + str(n1) + str(n2) + '.txt'
            dnc = file_dnc + str(p) + '_n' + str(n1) + str(n2) + '.txt'
            reluval = file_reluval + str(p) + '_n' + str(n1) + str(n2) + '.txt'
            nnv_star = file_nnv_star + str(p) + '_N' + str(n1) + str(n2) + '_star.txt'
            nnv_star_appr = file_nnv_star_appr + str(p) + '_N' + str(n1) + str(n2) + '_star_appr.txt'
            nnv_abs = file_nnv_abs + str(p) + '_N' + str(n1) + str(n2) + '_abs.txt'
            nnv_zono = file_nnv_zono + str(p) + '_N' + str(n1) + str(n2) + '_zono.txt'

            num, value, result = get_data_nnv(nnv_zono)
            str_temp = str_temp + '$N_{'+str(n1)+str(n2)+'}$&'+value + '&' + result +'&'
            num, value, result = get_data_nnv(nnv_abs)
            str_temp = str_temp + value + '&' + result + '&'
            value, result = get_data_mara(mara)
            str_temp = str_temp + value + '&' + result + '&'
            value, result = get_data_dnc(dnc)
            str_temp = str_temp + value + '&' + result + '&'
            value, result = get_data_reluval(reluval)
            str_temp = str_temp + value + '&' + result + '&'
            num, value, result = get_data_nnv(nnv_star)
            str_temp = str_temp + num +'&'+ value + '&' + result + '&'
            num, value, result = get_data_nnv(nnv_star_appr)
            str_temp = str_temp + value + '&' + result + '\\\\\n'


    str_temp = str_temp + '\\hline\n\\end{tabular}\n\\end{adjustbox}\n\\end{table}'
    filename = cfg.path_logs + 'table_property'+str(p)+'.tex'
    f = open(filename, 'w')
    f.write(str_temp)
    f.close()

# create summary tables

str_temp_head = '\\begin{table}[] \n \
\\centering \n \
\\renewcommand{\\arraystretch}{1.5} \n \
\\renewcommand{\\tabcolsep}{1.5mm} \n \
\\begin{adjustbox}{angle=0, max width=\\textwidth}\n \
\\begin{tabular}{l|ccccccc} \n \
\\hline \n \
\\multirow{2}{*}{\\textbf{ACAS XU $\\phi_1$}} &\\multirow{2}{*}{\\textbf{SAT}} & \\multirow{2}{*}{\\textbf{UNSAT}} & \\multirow{2}{*}{\\textbf{UNK}} & \\multicolumn{3}{l}{\\textbf{TIMEOUT}}      & \\multirow{2}{*}{\\textbf{TIME}}  \\\\ \\cline{5-7} \n \
                    &                     &                        &                      & \\textbf{1h} & \\textbf{2h} &{\\textbf{10h}} &                     \\\\ \\hline \n'
str_temp = str_temp_head
for p in range(1,property_num+1):
    time_mara = []
    result_mara = []
    time_dnc = []
    result_dnc = []
    time_reluval = []
    result_reluval = []
    time_star = []
    result_star = []
    time_appr = []
    result_appr = []
    time_abs = []
    result_abs = []
    time_zono = []
    result_zono = []

    if p > 1:
        str_temp = str_temp + '\\multirow{1}{*}{\\textbf{ACAS XU $\\phi_' + str(p) + '$}} & \\\\\\hline '
    for n1 in range(1, network_n1+1):
        for n2 in range(1, network_n2+1):

            mara = file_mara + str(p) + '_n' + str(n1) + str(n2) + '.txt'
            dnc = file_dnc + str(p) + '_n' + str(n1) + str(n2) + '.txt'
            reluval = file_reluval + str(p) + '_n' + str(n1) + str(n2) + '.txt'
            nnv_star = file_nnv_star + str(p) + '_N' + str(n1) + str(n2) + '_star.txt'
            nnv_star_appr = file_nnv_star_appr + str(p) + '_N' + str(n1) + str(n2) + '_star_appr.txt'
            nnv_abs = file_nnv_abs + str(p) + '_N' + str(n1) + str(n2) + '_abs.txt'
            nnv_zono = file_nnv_zono + str(p) + '_N' + str(n1) + str(n2) + '_zono.txt'

            num, value, result = get_data_nnv(nnv_zono)
            time_zono.append(float(value))
            result_zono.append(result)
            num, value, result = get_data_nnv(nnv_abs)
            time_abs.append(float(value))
            result_abs.append(result)
            value, result = get_data_mara(mara)
            time_mara.append(float(value))
            result_mara.append(result)
            value, result = get_data_dnc(dnc)
            time_dnc.append(float(value))
            result_dnc.append(result)
            value, result = get_data_reluval(reluval)
            time_reluval.append(float(value))
            result_reluval.append(result)
            num, value, result = get_data_nnv(nnv_star)
            time_star.append(float(value))
            result_star.append(result)
            num, value, result = get_data_nnv(nnv_star_appr)
            time_appr.append(float(value))
            result_appr.append(result)

    str_temp = str_temp + create_str('Marabou', time_mara, result_mara)
    str_temp = str_temp + create_str('Marabou DnC', time_dnc, result_dnc)
    str_temp = str_temp + create_str('ReluVal', time_reluval, result_reluval)
    str_temp = str_temp + create_str('Zonotope', time_zono, result_zono)
    str_temp = str_temp + create_str('Abstract Domain', time_abs, result_abs)
    str_temp = str_temp + create_str('NNV Exact Star', time_star, result_star)
    str_temp = str_temp + create_str('NNV Appr. Star', time_appr, result_appr)
    str_temp = str_temp + '\\hline \\hline \n'



str_temp = str_temp + '\n\\end{tabular}\n \\end{adjustbox}\n \\end{table}'
filename = cfg.path_logs + 'property_summary.tex'
f = open(filename, 'w')
f.write(str_temp)
f.close()


# create main.tex

str_temp = '\documentclass{article} \n \
\\usepackage[utf8]{inputenc} \n \
\\usepackage{adjustbox} \n \
\\usepackage{multirow} \n \
\\usepackage{multicol} \n \
\\title{Results} \n \
\\begin{document} \n \
\\maketitle \n \
\\section{Introduction} \n \
\\input{table_property1.tex} \n \
\\input{table_property2.tex} \n \
\\input{table_property3.tex} \n \
\\input{table_property4.tex} \n \
\\input{property_summary.tex} \n \
\\end{document}'
filename = cfg.path_logs + 'main.tex'
f = open(filename, 'w')
f.write(str_temp)
f.close()
