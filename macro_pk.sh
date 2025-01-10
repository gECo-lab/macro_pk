# Basic execution of benchmark model
# usage: benchmark.sh <model> <scenarios>
# model: models/model.json
# scenarios: scenarios/scenarios.json
# example: ,/benchmark.sh models/model.json scenarios/scenarios.json
model=$1
scenarios=$2


. venv


rm runs/*.csv

app_dir=$(pwd)

kernel_dir=$"/home/rivero/Dropbox/Workspace_Current/Projects/Apps/EcoSim/EcoSim_p/main/EcoSim_p"

cd "$kernel_dir"

python3 ecosimp.py "$app_dir" "$model" "$scenarios"

cd "/home/rivero/Dropbox/Workspace_Current/Projects/Apps/EcoSim/EcoSim_p/apps/macro_pk/"

quarto render "analisys/macro_pk.qmd" --output-dir=../results 

xdg-open results/macro_pk.html




