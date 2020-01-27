import numpy as np
import copy as cp
import os
import batch_config as cfg

def write_property_marabou(p, x, y, mean, std):
    x_temp = (np.array(x).transpose()-np.array([mean[:-1]]).transpose())/np.array([std[:-1]]).transpose()
    temp = (np.array(y)[:,-1] -  np.dot(np.array(y)[:,:-1], np.repeat(mean[-1], len(y[0])-1, axis=0)))/np.array(std[-1])
    y_temp = cp.deepcopy(y)
    for i in range(len(y)):
        y_temp[i][-1] = temp[i]
    # write property into marabou
    filename = '../Marabou/resources/properties/property_temp'+str(p)+'.txt'
    afile = open(filename, 'w')
    for i in range(len(x_temp)):
        x_lb = x_temp[i][0]
        x_ub = x_temp[i][1]
        afile.write('x' + str(i) + ' >= ' + str(x_lb) + '\n')
        afile.write('x' + str(i) + ' <= ' + str(x_ub) + '\n')
    for e in y_temp:
        str_temp = ''
        if e[0] == 1:
            for i in range(len(e)-1):
                if e[i]==1:
                    str_temp = str_temp + '+y' + str(i)
                elif e[i]==-1:
                    str_temp = str_temp + ' -y' + str(i)

            str_temp = str_temp + ' <= ' + str(e[-1]) + '\n'
            afile.write(str_temp)
        elif e[0] == -1:
            for i in range(len(e)-1):
                if e[i]==1:
                    str_temp = str_temp + ' -y' + str(i)
                elif e[i]==-1:
                    str_temp = str_temp + '+y' + str(i)

            if len(str_temp)==3:
                str_temp = str_temp[1:]
            str_temp = str_temp + ' >= ' + str(-e[-1]) + '\n'
            afile.write(str_temp)
        else:
            print('Error in adding Marabou property!')

    afile.close()


def write_property_reluval(p,x):
    filename = '../ReluVal/nnet.c'
    f = open(filename, 'r')
    contents = f.readlines()
    f.close()
    line_to_find = '    if (PROPERTY == ' + str(p) + ') {\n'
    idx = contents.index(line_to_find)
    line0 = '        float upper[] = {'
    for e in x[1]:
        line0 = line0 + str(e)+','
    line0 = line0[:-1]
    line0 = line0 + '};\n'

    line1 = '        float lower[] = {'
    for e in x[0]:
        line1 = line1 + str(e)+','
    line1 = line1[:-1]
    line1 = line1+'};\n'

    contents[idx+1] = line0
    contents[idx+2] = line1
    f = open(filename, 'w')
    contents = "".join(contents)
    f.write(contents)
    f.close()

def write_property_nnv_star(p,x,y):
    filename = cfg.path_nnv + 'nnv/examples/Submission/CAV2020/verify_P0_N00_star.m'
    f = open(filename, 'r')
    contents = f.readlines()
    f.close()
    line_to_find = '% edit property here\n'
    idx = contents.index(line_to_find)

    line0 = 'lb = ['
    for e in x[0]:
        line0 = line0 + str(e) + ';'

    line0 = line0[:-1]
    line0 = line0 + '];\n'

    line1 = 'ub = ['
    for e in x[1]:
        line1 = line1 + str(e) + ';'

    line1 = line1[:-1]
    line1 = line1 + '];\n'

    line2 = 'unsafe_mat = ['
    for e in y:
        for i in range(len(e)-1):
            line2 = line2 + str(e[i]) + ','
        line2 = line2[:-1]
        line2 = line2 + ';'

    line2 = line2[:-1]
    line2 = line2 + '];\n'

    line3 = 'unsafe_vec = ['
    for e in y:
        line3 = line3 + str(e[-1]) + ';'

    line3 = line3[:-1]
    line3 = line3 + '];\n'

    contents[idx + 1] = 'P0 = ' + str(p) + ';\n'
    contents[idx + 2] = line0
    contents[idx + 3] = line1
    contents[idx + 4] = line2
    contents[idx + 5] = line3
    f = open(filename, 'w')
    contents = "".join(contents)
    f.write(contents)
    f.close()

def write_property_nnv_abs(p,x,y):
    filename = cfg.path_nnv + 'nnv/examples/Submission/CAV2020/verify_P0_N00_abs.m'
    f = open(filename, 'r')
    contents = f.readlines()
    f.close()
    line_to_find = '% edit property here\n'
    idx = contents.index(line_to_find)

    line0 = 'lb = ['
    for e in x[0]:
        line0 = line0 + str(e) + ';'

    line0 = line0[:-1]
    line0 = line0 + '];\n'

    line1 = 'ub = ['
    for e in x[1]:
        line1 = line1 + str(e) + ';'

    line1 = line1[:-1]
    line1 = line1 + '];\n'

    line2 = 'unsafe_mat = ['
    for e in y:
        for i in range(len(e)-1):
            line2 = line2 + str(e[i]) + ','
        line2 = line2[:-1]
        line2 = line2 + ';'

    line2 = line2[:-1]
    line2 = line2 + '];\n'

    line3 = 'unsafe_vec = ['
    for e in y:
        line3 = line3 + str(e[-1]) + ';'

    line3 = line3[:-1]
    line3 = line3 + '];\n'

    contents[idx + 1] = 'P0 = ' + str(p) + ';\n'
    contents[idx + 2] = line0
    contents[idx + 3] = line1
    contents[idx + 4] = line2
    contents[idx + 5] = line3
    f = open(filename, 'w')
    contents = "".join(contents)
    f.write(contents)
    f.close()


def write_property_nnv_star_appr(p,x,y):
    filename = cfg.path_nnv + 'nnv/examples/Submission/CAV2020/verify_P0_N00_star_appr.m'
    f = open(filename, 'r')
    contents = f.readlines()
    f.close()
    line_to_find = '% edit property here\n'
    idx = contents.index(line_to_find)

    line0 = 'lb = ['
    for e in x[0]:
        line0 = line0 + str(e) + ';'

    line0 = line0[:-1]
    line0 = line0 + '];\n'

    line1 = 'ub = ['
    for e in x[1]:
        line1 = line1 + str(e) + ';'

    line1 = line1[:-1]
    line1 = line1 + '];\n'

    line2 = 'unsafe_mat = ['
    for e in y:
        for i in range(len(e)-1):
            line2 = line2 + str(e[i]) + ','
        line2 = line2[:-1]
        line2 = line2 + ';'

    line2 = line2[:-1]
    line2 = line2 + '];\n'

    line3 = 'unsafe_vec = ['
    for e in y:
        line3 = line3 + str(e[-1]) + ';'

    line3 = line3[:-1]
    line3 = line3 + '];\n'

    contents[idx + 1] = 'P0 = ' + str(p) + ';\n'
    contents[idx + 2] = line0
    contents[idx + 3] = line1
    contents[idx + 4] = line2
    contents[idx + 5] = line3
    f = open(filename, 'w')
    contents = "".join(contents)
    f.write(contents)
    f.close()

def write_property_nnv_zono(p,x,y):
    filename = cfg.path_nnv + 'nnv/examples/Submission/CAV2020/verify_P0_N00_zono.m'
    f = open(filename, 'r')
    contents = f.readlines()
    f.close()
    line_to_find = '% edit property here\n'
    idx = contents.index(line_to_find)

    line0 = 'lb = ['
    for e in x[0]:
        line0 = line0 + str(e) + ';'

    line0 = line0[:-1]
    line0 = line0 + '];\n'

    line1 = 'ub = ['
    for e in x[1]:
        line1 = line1 + str(e) + ';'

    line1 = line1[:-1]
    line1 = line1 + '];\n'

    line2 = 'unsafe_mat = ['
    for e in y:
        for i in range(len(e)-1):
            line2 = line2 + str(e[i]) + ','
        line2 = line2[:-1]
        line2 = line2 + ';'

    line2 = line2[:-1]
    line2 = line2 + '];\n'

    line3 = 'unsafe_vec = ['
    for e in y:
        line3 = line3 + str(e[-1]) + ';'

    line3 = line3[:-1]
    line3 = line3 + '];\n'

    contents[idx + 1] = 'P0 = ' + str(p) + ';\n'
    contents[idx + 2] = line0
    contents[idx + 3] = line1
    contents[idx + 4] = line2
    contents[idx + 5] = line3
    f = open(filename, 'w')
    contents = "".join(contents)
    f.write(contents)
    f.close()



# add subset of input range of the selected property
def write_property(property, x, y, mean, std):
    # Marabou
    try:
        write_property_marabou(property, x, y, mean, std)
    except:
        print('Error in adding property into Marabou!')

    # ReluVal
    try:
        write_property_reluval(property, x)
        os.system('cd ../ReluVal && make')
    except:
        print('Error in editting ReluVal nnet.c!')

    # nnv_star
    try:
        write_property_nnv_star(property, x, y)
    except:
        print('Error in editting NNV')

    # nnv_abs
    try:
        write_property_nnv_abs(property, x, y)
    except:
        print('Error in editting the abstract domain method')

    # nnv_appr
    try:
        write_property_nnv_star_appr(property, x, y)
    except:
        print('Error in editting NNV approximation method')

    # zono
    try:
        write_property_nnv_zono(property, x, y)
    except:
        print('Error in editting Zonotope method')
