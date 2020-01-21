import os
import batch_config

file_mara = output_prefix + 'logs_mara/results_p'
file_dnc = output_prefix + 'logs_dnc/results_p'
file_reluval = output_prefix + 'logs_reluval/results_p'
file_nnv_star = output_prefix + 'logs_nnv_star/P'
file_nnv_star_appr = output_prefix + 'logs_nnv_star_appr/P'
file_nnv_abs = output_prefix + 'logs_nnv_abs/P'
file_nnv_zono = output_prefix + 'logs_nnv_zono/P'



def get_data_mara(mara):
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


def get_data_dnc(dnc):
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


def get_data_reluval(reluval):
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


def get_data_nnv(nnv):
    try:
        f = open(nnv, 'r')
        contents = f.readlines()
    except:
        print("error parsing nnv results")
    finally:
        f.close()
    result = contents[0][:-1]
    num = contents[1][23:-1]
    value = contents[2][12:-1]

    return num, value, result


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
            num, value, result = get_data_nnv(nnv_star)
            str_temp = str_temp + value + '&' + result + '\\\\\n'


    str_temp = str_temp + '\\hline\n\\end{tabular}\n\\end{adjustbox}\n\\end{table}'
    filename = 'table_property'+str(p)+'.tex'
    f = open(filename, 'w')
    f.write(str_temp)
    f.close()
