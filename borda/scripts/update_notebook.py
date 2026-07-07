import json

notebook_path = 'EJECUCION_COLAB_SOTA_2026.ipynb'

with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Update the instruction cell
nb['cells'][0]['source'] = [
    "# 🧬 Tesis Genómica 2026: Ejecución SOTA con Checkpoints\n",
    "**Investigador:** Gary Velasquez  \n",
    "**Objetivo:** Entrenar Forest Diffusion sobre el Master Datalake (28,048 muestras) superando problemas de memoria (OOM).\n",
    "\n",
    "### 🚀 Instrucciones de Inicio:\n",
    "1. Asegúrate de estar usando un entorno de **GPU** (Entorno de ejecución -> Cambiar tipo de entorno -> T4/L4/A100).\n",
    "2. Sube la carpeta del proyecto a tu Google Drive en una carpeta llamada `tesis_genetica/`."
]

# Find the cell with the training command and update it
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if '!python scripts/train_forest_diffusion' in source:
            cell['source'] = ["!python scripts/train_forest_diffusion_checkpoints.py --dataset master --n_t 50 --mode both --device cuda"]

with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)

print("Notebook actualizado exitosamente.")
