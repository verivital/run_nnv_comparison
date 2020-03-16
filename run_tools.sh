#/bin/bash

DIRECTORY=/codeocean-true

# if on codeocean, results must go to /results during a 
# run, otherwise they do not get saved
if [ -d "$DIRECTORY" ]; then
	OUTPUT_PREFIX=/results/
# otherwise, use the current directory
else
	OUTPUT_PREFIX=./
fi

FILE=$OUTPUT_PREFIX/logs
if [ -d "$FILE" ]; then
    sudo rm -r $OUTPUT_PREFIX/logs
fi

mkdir -p $OUTPUT_PREFIX/logs/logs_dnc
mkdir -p $OUTPUT_PREFIX/logs/logs_mara
mkdir -p $OUTPUT_PREFIX/logs/logs_reluval

mkdir -p $OUTPUT_PREFIX/logs/logs_nnv_star
mkdir -p $OUTPUT_PREFIX/logs/logs_nnv_star_appr
mkdir -p $OUTPUT_PREFIX/logs/logs_nnv_abs
mkdir -p $OUTPUT_PREFIX/logs/logs_nnv_zono
mkdir -p $OUTPUT_PREFIX/logs/logs_reluplex

# 4 acas-xu properties
# select runtime based on considering 
# subsets of the property sizes
#property_size = 0 # full ranges (slowest: days of runtime)
#property_size = 1 # medium ranges
property_size=2 # small ranges (fast: seconds for most)

p_num=4
i=1

# iterate over the acas-xu properties
while [ $i -le $p_num ]
do
    cd scripts
    # generate shell scripts to call tools 
    # for each property i
    python3 run_comparison.py $i $property_size
    chmod +x run_reluval.sh
    chmod +x run_marabou.sh
    chmod +x run_marabou_dnc.sh
    chmod +x run_nnv_star.sh
    chmod +x run_nnv_star_appr.sh
    chmod +x run_nnv_abs.sh
    chmod +x run_nnv_zono.sh
    chmod +x run_reluplex.sh
    cd ..
    ./scripts/run_reluplex.sh
    ./scripts/run_reluval.sh
    ./scripts/run_marabou.sh
    ./scripts/run_marabou_dnc.sh
    
    # skip running nnv if matlab is not installed
    if command -v matlab 2>/dev/null; then
        sudo ./scripts/run_nnv_star.sh
        ./scripts/run_nnv_star_appr.sh
        ./scripts/run_nnv_abs.sh
        ./scripts/run_nnv_zono.sh
    else
        echo "Matlab not detected, skipping NNV"
    fi
    
    rm -f scripts/run_reluval.sh
    rm -f scripts/run_marabou.sh
    rm -f scripts/run_marabou_dnc.sh
    rm -f scripts/run_nnv_star.sh
    rm -f scripts/run_nnv_star_appr.sh
    rm -f scripts/run_nnv_abs.sh
    rm -f scripts/run_nnv_zono.sh
    rm -f scripts/run_reluplex.sh
    ((i++))
done

python3 scripts/write_latex_table.py
echo "All done with ACAS-Xu comparisons!"

echo "Starting closed-loop CPS examples in NNV"
# run nnv-only closed-loop CPS examples
# do not do this on codeocean, as it is executed in a different manner (from run_codeocean.m)
if ! [ -d "$DIRECTORY" ]; then
    matlab -nodisplay -nodesktop -r 'run $(pwd)/nnv/code/nnv/examples/Submission/CAV2020/ACC/reproduce.m; quit;'
fi
