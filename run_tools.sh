#/bin/bash

mkdir -p logs/logs_nnv_star
mkdir -p logs/logs_nnv_star_appr
mkdir -p logs/logs_nnv_abs
mkdir -p logs/logs_nnv_zono
mkdir -p logs/logs_dnc
mkdir -p logs/logs_mara
mkdir -p logs/logs_reluval

p_num=4
i=1
while [ $i -le $p_num ]
do
    cd scripts
    python3 run_comparison.py $i
    chmod +x run_reluval.sh
    chmod +x run_marabou.sh
    chmod +x run_marabou_dnc.sh
    chmod +x run_nnv_star.sh
    chmod +x run_nnv_star_appr.sh
    chmod +x run_nnv_abs.sh
    chmod +x run_nnv_zono.sh
    cd ..
    ./scripts/run_reluval.sh
    ./scripts/run_marabou.sh
    ./scripts/run_marabou_dnc.sh
    ./scripts/run_nnv_star.sh
    ./scripts/run_nnv_star_appr.sh
    ./scripts/run_nnv_abs.sh
    ./scripts/run_nnv_zono.sh
    rm -f scripts/run_reluval.sh
    rm -f scripts/run_marabou.sh
    rm -f scripts/run_marabou_dnc.sh
    rm -f scripts/run_nnv_star.sh
    rm -f scripts/run_nnv_star_appr.sh
    rm -f scripts/run_nnv_abs.sh
    rm -f scripts/run_nnv_zono.sh
    ((i++))
done

python3 scripts/write_latex_table.py
echo "All done!"







