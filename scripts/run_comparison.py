import numpy as np
import sys
import os
import write_property as wp
import create_bash_scripts as cs


property = int(sys.argv[1])

if property == 1:
    # x = [[55947.69, -3.14, -3.14, 1145, 0], [60760, 3.14, 3.14, 1200, 60]]
    # y = [[-1, 0, 0, 0, 0, -1500]]
    x = [[60750, 3.13, 3.13, 1190, 55], [60760, 3.14, 3.14, 1200, 60]] # subset of input range
    y = [[-1, 0, 0, 0, 0, -1500]]

elif property == 2:
    # x = [[55947.69, -3.14, -3.14, 1145, 0] ,[60760, 3.14, 3.14, 1200, 60]]
    # y = [[-1, 1, 0, 0, 0, 0], [-1, 0, 1, 0, 0, 0], [-1, 0, 0, 1, 0, 0], [-1, 0, 0, 0, 1, 0]]
    x = [[60750, 3.13, 3.13, 1190, 55], [60760, 3.14, 3.14, 1200, 60]]  # subset of input range
    y = [[-1, 1, 0, 0, 0, 0], [-1, 0, 1, 0, 0, 0], [-1, 0, 0, 1, 0, 0], [-1, 0, 0, 0, 1, 0]]

elif property == 3:
    # x = [[1500, -0.06, 3.1, 980, 960], [1800, 0.06, 3.14, 1200, 1200]]
    # y = [[1, -1, 0, 0, 0, 0], [1, 0, -1, 0, 0, 0], [1, 0, 0, -1, 0, 0], [1, 0, 0, 0, -1, 0]]
    x = [[1790, 0.05, 3.13, 1190, 1190], [1800, 0.06, 3.14, 1200, 1200]] # subset of input range
    y = [[1, -1, 0, 0, 0, 0], [1, 0, -1, 0, 0, 0], [1, 0, 0, -1, 0, 0], [1, 0, 0, 0, -1, 0]]

elif property == 4:
    # x = [[1500, -0.06, 0, 1000, 700], [1800, 0.06, 0, 1200, 800]]
    # y = [[1, -1, 0, 0, 0, 0], [1, 0, -1, 0, 0, 0], [1, 0, 0, -1, 0, 0], [1, 0, 0, 0, -1, 0]]
    x = [[1790, 0.05, 0, 1190, 790], [1800, 0.06, 0, 1200, 800]]  # subset of input range
    y = [[1, -1, 0, 0, 0, 0], [1, 0, -1, 0, 0, 0], [1, 0, 0, -1, 0, 0], [1, 0, 0, 0, -1, 0]]

else:
    print('This property is not defined!')

mean = [1.9791091e+04,0.0,0.0,650.0,600.0,7.5188840201005975]
std = [60261.0,6.28318530718,6.28318530718,1100.0,1200.0,373.94992]

# edit the input range of the selected property
wp.write_property(property, x, y, mean, std)

# generate bash scripts to run comparison
cs.create_bash(property)
