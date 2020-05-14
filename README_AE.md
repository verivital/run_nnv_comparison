# NNV: NNV: The Neural Network Verification Tool for Deep Neural Networks and Learning-Enabled Cyber-Physical Systems
Hoang Dung Tran, Xiaodong Yang, Diego Manzanas, Patrick Musau, Luan Nguyen, Weiming Xiang, Stanley Bak and Taylor T Johnson
32nd International Conference on Computer-Aided Verification (CAV 2020)

## CodeOcean Capsule DOI:
https://doi.org/10.24433/CO.0221760.v1

## Source Code:
https://github.com/verivital/nnv

## CAV2020 AE Tag:
https://github.com/verivital/nnv/tree/cav2020

## CAV2020 AE Files:
https://github.com/verivital/nnv/tree/master/code/nnv/examples/Submission/CAV2020

## NNV, Marabou, ReluVal, etc. comparison scripts:
https://github.com/verivital/run_nnv_comparison

## CAV2020 AE Tag for Comparison Scripts:
https://github.com/verivital/run_nnv_comparison/tree/cav2020

## CodeOcean Capsule (username: see easychair, password: see easychair):
https://codeocean.com/capsule/1314285/

## REPRODUCING THE RESULTS IN THE PAPER

### 1. The paper contains the following computational elements:

Table 2 (and Appendix Tables): comparison between NNV (exact star set, approximate star set, zonotope a la DeepZono, abstract domains a la DeepPoly), Reluplex, Marabou, and ReluVal. Reproduced by this file:

https://github.com/verivital/run_nnv_comparison/blob/cav2020/run_tools.sh

Table 3: safety verification of adaptive cruise control (ACC) learning-enabled CPS case study. Reproduced by these files (linear and nonlinear columns respectively):

https://github.com/verivital/nnv/blob/cav2020/code/nnv/examples/Submission/CAV2020/ACC/verify_linear_ACC.m

https://github.com/verivital/nnv/blob/cav2020/code/nnv/examples/Submission/CAV2020/ACC/verify_nonlinear_ACC.m

Figure 4: safety verification of adaptive cruise control (ACC) learning-enabled CPS case study. Reproduced by this file:

https://github.com/verivital/nnv/blob/cav2020/code/nnv/examples/Submission/CAV2020/ACC/plot_linear_ACC_reachSets.m

### 2. System Requirements

#### 2a. CodeOcean

We STRONGLY recommend using the CodeOcean capsule described shortly, which will avoid you having to install anything. The configured CodeOcean capsule has Ubuntu 18.04 and Matlab 2019a, executed inside a Docker containerized environment. The underlying hardware is shared cloud infrastructure, specifically an AWS r5d.4xlarge (16-core, 120GB RAM, see: https://help.codeocean.com/en/articles/1120508-what-machine-will-my-code-run-on).

As CodeOcean is shared infrastructure, exact runtimes are not expected to be reproducible due to varying compute load. We provide scripts that automatically generate results like those presented in the paper, but that may differ in magnitude. Additionally, as some results take significant runtime (order of days of runtime), specifically some ACAS-Xu experiments, we have configured the set up to consider subsets of the full set of initial states that can execute more quickly (as reproduced in the appendix tables). Specifically, to reproduce the full Table 2 results, one can select the full set of initial states by setting property_size = 0 here:

https://github.com/verivital/run_nnv_comparison/blob/master/scripts/run_comparison.py#L12

The smaller initial set of states that CodeOcean and the comparison scripts use, for all detailed ACAS-Xu tables, are specified with property_size = 2 here:

https://github.com/verivital/run_nnv_comparison/blob/master/scripts/run_comparison.py#L14

#### 2b. OS

Window 10 or Linux, but either should work (CodeOcean described below is run on Linux). Mac may work, but has not been tested.

#### 2c. Dependencies

Matlab 2018b or later (may work on earlier versions, but untested)

### 3. CodeOcean Capsule

3a. NNV is configured to run without installation and without dependence upon users having Matlab licenses through CodeOcean, which has an agreement with the MathWorks to provide publicly available infrastructure for reproducing computational research.

3b. The latest CodeOcean capsule may be accessed here, a login is required (no public sharing by link is available until the capsule is published and has an updated DOI):

https://codeocean.com/capsule/1314285/

Username: email authors
Password: email authors

The CodeOcean capsule corresponding to the paper at the time of sumbission is available here:
https://doi.org/10.24433/CO.0221760.v1

3c. After opening the capsule through the above URL, one can view code, navigate existing reproduced results, etc.

A full prior execution of all results in this paper is available in "Run 250950." This process takes about 2 hours, including the time to build the Docker container, set up the tools, etc., which takes around 15-20 minutes for NNV and all the compared tools. The comparison execution takes around 30-45 minutes, and the remainder of the results another ~40 minutes. One can navigate the results from any prior execution, so e.g., one can view the tables and figures generated for this paper at:

Run 250950\logs

For example, Figure 4 showing the ACC case study reachable states can be seen at:

Run 250950\logs\ACC\figure4_plot_linear_ACC_reachSets.png

To re-run all computations and reproduce the results, one selects "Reproducible Run," which will run scripts to execute all of NNVs tests, examples, etc. We next explain what this process does.

This starts by building the Docker container, which first executes this Dockerfile (if the container is already cached, it doesn't rebuild, so runtime can be faster):

https://github.com/verivital/nnv/blob/cav2020/environment/Dockerfile

This subsequently runs a post-installation script that installs further dependencies:

https://github.com/verivital/nnv/blob/cav2020/environment/postInstall

Finally, the main entry point that is executed when selecting "Reproducible Run" is this bash script:

https://github.com/verivital/nnv/blob/cav2020/code/run

Within this shell script, the computational artifacts are reproduced through two scripts, a run shell script and a run_codeocean.m Matlab script.

First, the ACAS-Xu comparison between NNV, Marabou, ReluVal, etc., is done by executing the run_scripts.sh shell script, which using the smaller subset of initial states for ACAS-Xu takes around 30 minutes to run (the full ranges would take days). The run_tools.sh script is called here:

https://github.com/verivital/nnv/blob/cav2020/code/run#L26

Which executes this script (which will call NNV, Marabou, Reluval, etc.):

https://github.com/verivital/run_nnv_comparison/blob/cav2020/run_tools.sh

Next, the shell script launches Matlab and executes the run_codeocean.m script:

https://github.com/verivital/nnv/blob/cav2020/code/run_codeocean.m

Within this, first the ACC learning-enabled CPS case study is run within by calling the reproduce.m script:

https://github.com/verivital/nnv/blob/cav2020/code/run_codeocean.m#L24

Which executes this script:

https://github.com/verivital/nnv/blob/cav2020/code/nnv/examples/Submission/CAV2020/ACC/reproduce.m

Finally, NNV's tests are executed (all .m test files recursively within the tests folder):

https://github.com/verivital/nnv/tree/cav2020/code/nnv/tests

There are a few other commands listed within the run_codeocean file as further examples, as we have not presented all examples, case studies, etc. that NNV has been evaluated on within this paper due to space, and there are significantly more.

- We have updated the published CodeOcean capsule with all reproducible results described in this paper and generated a new DOI so others can publicly reproduce, available here:

https://doi.org/10.24433/CO.0221760.v1

- A prior publicly accessible CodeOcean capsule that reproduces all the tests in NNV is available here:

https://doi.org/10.24433/CO.1314285.v1 

- There are some restrictions to using CodeOcean beyond the computational time limits, which is why some of the reproducibility is configured as it is, e.g., it does not support git submodules, which NNV depends upon for integration with HyST, CORA, and NNMT. There are workarounds for this that are deployed in the current CodeOcean setup (e.g., through the shell scripts).

### 4. Manual Installation

There are two primary ways to install NNV and the comparison scripts. If CodeOcean is not used or if reviewers want to attempt installing NNV, we recommend doing so through the comparison scripts, but will describe standalone installation second. The comparison scripts are also set up to execute within a Docker container, although for this, NNV will not be run as it would require having Matlab configured within the container (which technically is possible as CodeOcean illustrates, but that we cannot distribute for licensing reasons), so this mechanism only reproduces the comparison between the other tools.

#### 4a. Comparison Script Installation:

This set up is recommending for installing NNV and the compared tools on an existing computer not in a containerized environment (e.g., a desktop, laptop, etc.). We recommend having Matlab installed (2019a or above, although earlier versions may work) and using Ubuntu 18.04, which matches the CodeOcean configuration. In a terminal:

##### 4a1. Clone the comparison script:

git clone https://github.com/verivital/run_nnv_comparison

##### 4a2. Set up the tools (installs in subfolders all of Marabou, Reluplex, NNV, and ReluVal):

chmod +x setup_tools.sh
./setup_tools.sh

##### 4a3. Run the tools (we recommend redirecting the output to a log file for performance and reproducibility)

chmod +x run_tools.sh
./run_tools.sh > results.txt

#### 4a4. The results are generated in the logs/ folder.

This process may take 1-2 hours. The results will be produced in the log subfolders, including reproductions of the latex tables and figures presented in the paper.

### 4b. Standalone Manual Installation

This setup is if you want to delve more into NNV, and is recommended for any operating system with Matlab installed. 

Note that if you performed the comparison script installation (4a), you can do all the following reproduction by opening Matlab and going to the nnv subfolder that gets created from setup_tools.sh.

If for some reason you prefer to proceed with the standalone NNV installation, you may do the following.

#### 4b1. Clone NNV repository using the recursive option as it has submodules:

git clone --recursive https://github.com/verivital/nnv.git

#### 4b2. Install NNV (install.m)
In Matlab, navigate to the code/nnv/ folder. Execute the install.m script, which will set up various dependencies (mostly via tbxmanager). This should also set up the path correctly within Matlab so all dependencies are available.

install

https://github.com/verivital/nnv/blob/cav2020/code/nnv/install.m

If Matlab is restarted, to work again, either install.m or startup_nnv.m must be executed again. Alternatively, one can execute savepath to update the path after executing install (but in this case, Matlab may need to have been launched with administrative privilege).

savepath

https://github.com/verivital/nnv/blob/cav2020/code/nnv/startup_nnv.m

#### 4b3. Run paper reproducibility: ACAS-Xu

In Matlab, navigate to the CAV2020 submission folder at code/nnv/examples/Submission/CAV2020. One can reproduce any entry in the ACAS-Xu files through the scripts verify_P0_N00_*.m, where * is in {abs, star, star_appr, zono}. The property number (P0) ranges between 1-4 and the network numbers (N00) range between 11 and 56 (for the 45 ACAS-Xu networks). For example, one can run the following to verify the specified property for network 11 (1-indexed, so network 00):

verify_P0_N00_star_appr(1,1)

https://github.com/verivital/nnv/blob/cav2020/code/nnv/examples/Submission/CAV2020/verify_P0_N00_star_appr.m

The property to be verified is selected within the verify files (see the variable P0 and change it to between 1 and 4).

#### 4b4. Run paper reproducibility: ACC

In Matlab, assuming you are still at the CAV2020 submission folder at code/nnv/examples/Submission/CAV2020, navigate to the ACC subfolder (i.e., code/nnv/examples/Submission/CAV2020/ACC).

https://github.com/verivital/nnv/tree/cav2020/code/nnv/examples/Submission/CAV2020/ACC

Run the script reproduce.m:

reproduce

### 4c. Dockerfile set up

The comparison script repository includes a Dockerfile:

https://github.com/verivital/run_nnv_comparison/blob/cav2020/Dockerfile

This will set up a Docker container with all tools except NNV. This can be done from the run_nnv_comparison cloned directory via:

docker build . -t nnvcomp

docker run -it nnvcomp

This will now be in a shell in the Docker container. The scripts may be run via:

./run_tools.sh > results.txt

We recommend redirecting the output as it generates significant log messages (and this can influence performance, aside from saving the interaction log).

