import pandas as pd
import matplotlib.pyplot as plt
import math
from pathlib import Path

# Diretórios
input_dir = Path("../runs")
output_dir = Path("../results")

# Carregar os dataframes já processados
household_means_path = output_dir / "household_means.csv"
cg_means_path = output_dir / "cg_means.csv"

if household_means_path.exists():
    household_means = pd.read_csv(household_means_path)
else:
    household_means = None
    print("Arquivo household_means.csv não encontrado.")

if cg_means_path.exists():
    cg_means = pd.read_csv(cg_means_path)
else:
    cg_means = None
    print("Arquivo cg_means.csv não encontrado.")

# Função para plotar múltiplos gráficos em grid
def plot_grid(df, title_prefix, ncol=4):
    if df is None:
        return
    cols = [col for col in df.columns if col != "step"]
    n = len(cols)
    nrow = math.ceil(n / ncol)
    fig, axes = plt.subplots(nrow, ncol, figsize=(5*ncol, 3*nrow), squeeze=False)
    for idx, var in enumerate(cols):
        ax = axes[idx // ncol][idx % ncol]
        ax.plot(df["step"], df[var], marker="o", linewidth=1)
        ax.set_title(f"{title_prefix} - {var}", fontsize=10)
        ax.set_xlabel("Step", fontsize=8)
        ax.set_ylabel(f"means - {var}", fontsize=8)
        ax.grid(True, alpha=0.3)
    # Remove empty subplots
    for idx in range(n, nrow * ncol):
        fig.delaxes(axes[idx // ncol][idx % ncol])
    plt.tight_layout()
    plt.show()

# Household plots
plot_grid(household_means, "Household", ncol=4)

# CGFirm plots
plot_grid(cg_means, "CGFirm", ncol=4)
