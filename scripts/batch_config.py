import os

def is_codeocean():
    if os.path.isdir("/codeocean-true"):
        return True
    else:
        return False

#file paths
if is_codeocean():
    output_prefix = "/results/logs/"
    path_nnv = "/code/"
    path_nnv_abs = path_nnv
    path_logs = "/results/logs/"
else:
    output_prefix = "logs/"
    path_nnv = "../nnv/code/"
    path_nnv_abs = "$(pwd)/nnv/code/"
    path_logs = "logs/"
