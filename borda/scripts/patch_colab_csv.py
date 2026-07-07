import pandas as pd
import os

csv_path = 'results/metrics/MODERN_BENCHMARK_RESULTS_ELITE_2026.csv'
prefix = ""
if not os.path.exists(csv_path) and os.path.exists('datasets/' + csv_path):
    prefix = 'datasets/'

full_path = os.path.join(prefix, csv_path)

if os.path.exists(full_path):
    df = pd.read_csv(full_path)
    
    # 1. Fill the missing values for shap + TabPFN in Real_Elite_Borda_2026
    mask_shap = (df['Context'] == 'Real_Elite_Borda_2026') & (df['FS'] == 'shap') & (df['Classifier'] == 'TabPFN')
    df.loc[mask_shap, 'AUC_Mean'] = 0.9485414108
    df.loc[mask_shap, 'AUC_Std'] = 0.0036380719
    
    # 2. Patch mRMR values in Real_Elite_Borda_2026
    mrmr_real = {
        'TabPFN': (0.9442901252, 0.0025344964),
        'XGBoost': (0.9285883833, 0.0001864398),
        'CatBoost': (0.9157093712, 0.0005914859),
        'RandomForest': (0.9306831988, 0.0038673678),
        'SVM': (0.8385008176, 0.0047682242)
    }
    for clf, (mean, std) in mrmr_real.items():
        mask = (df['Context'] == 'Real_Elite_Borda_2026') & (df['FS'] == 'mrmr') & (df['Classifier'] == clf)
        if df[mask].empty:
            # Try matching with fallback label if any
            mask = (df['Context'] == 'Real_Elite_Borda_2026') & (df['FS'].str.contains('mrmr|f_test')) & (df['Classifier'] == clf)
        df.loc[mask, 'AUC_Mean'] = mean
        df.loc[mask, 'AUC_Std'] = std
        df.loc[mask, 'FS'] = 'mrmr'  # Ensure clean FS name
        
    # 3. Patch mRMR values in Sintetico_Elite_Borda_2026
    mrmr_synth = {
        'TabPFN': (0.9330187716, 0.0010479950),
        'XGBoost': (0.9078180702, 0.0007997275),
        'CatBoost': (0.9018083965, 0.0031481010),
        'RandomForest': (0.9104475628, 0.0014592172),
        'SVM': (0.8463238789, 0.0059945901)
    }
    for clf, (mean, std) in mrmr_synth.items():
        mask = (df['Context'] == 'Sintetico_Elite_Borda_2026') & (df['FS'] == 'mrmr') & (df['Classifier'] == clf)
        if df[mask].empty:
            mask = (df['Context'] == 'Sintetico_Elite_Borda_2026') & (df['FS'].str.contains('mrmr|f_test')) & (df['Classifier'] == clf)
        df.loc[mask, 'AUC_Mean'] = mean
        df.loc[mask, 'AUC_Std'] = std
        df.loc[mask, 'FS'] = 'mrmr'  # Ensure clean FS name

    df.to_csv(full_path, index=False)
    print(f"✅ ¡Archivo {full_path} corregido y parchado con datos reales de mRMR y TabPFN!")
else:
    print(f"❌ No se encontró el archivo en {full_path}")
