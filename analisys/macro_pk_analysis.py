import os
import pandas as pd
from pathlib import Path

# Diretórios
input_dir = Path("../runs")
output_dir = Path("../results")
output_dir.mkdir(exist_ok=True)
# Salvar o diretório atual e mudar para o diretório "analisys" em macro_pk
original_cwd = os.getcwd()
print(original_cwd)
os.chdir(Path(__file__).parent)

# Carregar arquivos Household
files = [f for f in os.listdir(input_dir) if "macro_model_Household" in f]
if files:
    Household = pd.read_csv(input_dir / files[0])
    Household = Household.drop(columns=[col for col in ["run", "index_no"] if col in Household.columns])
else:
    Household = pd.DataFrame()

# Carregar arquivos CGFirm
files = [f for f in os.listdir(input_dir) if "macro_model_CGFirm" in f]
if files:
    CGFirm = pd.read_csv(input_dir / files[0])
    CGFirm = CGFirm.drop(columns=[col for col in ["run", "index_no"] if col in CGFirm.columns])
else:
    CGFirm = pd.DataFrame()

# Gerar dataframes de médias e contagem de booleanos
if not Household.empty:
    household_means = Household.groupby("step").agg({**{col: "mean" for col in Household.select_dtypes(include="number").columns if col != "step"},
                                                      **{col: "sum" for col in Household.select_dtypes(include="bool").columns}}).reset_index()
    household_means.to_csv(output_dir / "household_means.csv", index=False)
else:
    print("Nenhum dado Household encontrado.")

if not CGFirm.empty:
    cg_means = CGFirm.groupby("step").agg({**{col: "mean" for col in CGFirm.select_dtypes(include="number").columns if col != "step"},
                                            **{col: "sum" for col in CGFirm.select_dtypes(include="bool").columns}}).reset_index()
    cg_means.to_csv(output_dir / "cg_means.csv", index=False)
else:
    print("Nenhum dado CGFirm encontrado.")

print("Processamento concluído.")
