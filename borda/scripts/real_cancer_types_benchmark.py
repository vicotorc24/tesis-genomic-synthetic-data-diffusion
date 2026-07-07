import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier

def run_real_empirical_benchmark():
    print("Iniciando Benchmarking Empírico (Datos Reales)...")
    
    path_real = 'results/elite_borda_training_table.parquet'
    path_synth = 'results/synthetic_samples_elite_borda_5000.parquet'
    
    if not os.path.exists(path_real) or not os.path.exists(path_synth):
        print(f"Error: No se encontraron los datasets requeridos.")
        return
        
    df_real = pd.read_parquet(path_real)
    df_synth = pd.read_parquet(path_synth)
    
    target_col = 'target' if 'target' in df_real.columns else 'Category'
    
    # Asegurar parseo numérico para XGBoost
    for col in df_real.columns:
        if df_real[col].dtype == object and col not in ['GSE_ID', target_col]:
            df_real[col] = df_real[col].astype(str).str.replace(r'[\[\]]', '', regex=True).astype(float)
            
    for col in df_synth.columns:
        if df_synth[col].dtype == object and col not in ['GSE_ID', target_col]:
            df_synth[col] = df_synth[col].astype(str).str.replace(r'[\[\]]', '', regex=True).astype(float)
            
    # Filtrar estudios (GSE) que tengan al menos 15 muestras de cada clase para un benchmark estable
    valid_gses = []
    for gse in df_real['GSE_ID'].unique():
        y_gse = df_real[df_real['GSE_ID'] == gse][target_col]
        counts = y_gse.value_counts()
        if len(counts) == 2 and counts.get(0.0, 0) >= 15 and counts.get(1.0, 0) >= 15:
            valid_gses.append(gse)
            
    # Obtener los top 5 estudios más grandes de entre los válidos
    gse_counts = df_real[df_real['GSE_ID'].isin(valid_gses)]['GSE_ID'].value_counts()
    top_5_gses = gse_counts.head(5).index.tolist()
    print(f"Top 5 Cohortes Balanceadas y Grandes identificadas: {top_5_gses}")
    
    # Preparar X, y sintético para el modelo TSTR
    # El modelo sintético entrena con TODO el datalake (Sinergia de cánceres)
    drop_cols_synth = ['GSE_ID', 'Category', 'target']
    X_synth = df_synth.drop(columns=[c for c in drop_cols_synth if c in df_synth.columns])
    y_synth = df_synth[target_col].astype(int)
    
    results = []
    
    # Configurar modelo rápido pero potente
    clf = XGBClassifier(n_estimators=100, max_depth=4, random_state=42, n_jobs=-1, eval_metric='logloss')
    
    # Entrenar el Modelo TSTR (Sintético Armonizado) UNA SOLA VEZ
    print("\n[+] Entrenando Modelo Maestro (Datalake Sintético Armonizado)...")
    clf_synth = XGBClassifier(n_estimators=100, max_depth=4, random_state=42, n_jobs=-1, eval_metric='logloss')
    clf_synth.fit(X_synth, y_synth)
    print("    Listo.")
    
    for gse in top_5_gses:
        print(f"\n🧪 Evaluando cohorte aislada: {gse}")
        
        # Filtrar pacientes reales de esta cohorte específica
        df_gse = df_real[df_real['GSE_ID'] == gse]
        
        X_gse = df_gse.drop(columns=[c for c in drop_cols_synth if c in df_real.columns])
        y_gse = df_gse[target_col].astype(int)
        
        # Validar si hay ambas clases (Cáncer vs Sano) en este GSE
        if len(y_gse.unique()) < 2:
            print(f"    ⚠️ {gse} saltado: Solo contiene una clase (no se puede medir AUC).")
            continue
            
        # Split 80/20 real
        try:
            X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_gse, y_gse, test_size=0.20, random_state=42, stratify=y_gse)
        except ValueError:
            # Si hay muy pocos de una clase, hacemos fallback sin stratify
            X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_gse, y_gse, test_size=0.20, random_state=42)
            
        # --- MODELO TRTR (Aislado Real) ---
        print("    Entrenando modelo Aislado (Solo con datos de este GSE)...")
        clf_real = XGBClassifier(n_estimators=100, max_depth=4, random_state=42, n_jobs=-1, eval_metric='logloss')
        # Si test/train no tienen 2 clases, saltar
        if len(y_train_r.unique()) < 2 or len(y_test_r.unique()) < 2:
             print("    ⚠️ Saltado por falta de varianza de clases en split.")
             continue
             
        clf_real.fit(X_train_r, y_train_r)
        preds_real = clf_real.predict_proba(X_test_r)[:, 1]
        auc_isolated = roc_auc_score(y_test_r, preds_real)
        
        # --- MODELO TSTR (Sintético Armonizado) ---
        print("    Evaluando modelo Armonizado en el Test Set de este GSE...")
        preds_synth = clf_synth.predict_proba(X_test_r)[:, 1]
        auc_harmonized = roc_auc_score(y_test_r, preds_synth)
        
        print(f"    -> AUC Aislado: {auc_isolated:.3f} | AUC Armonizado: {auc_harmonized:.3f}")
        
        # Guardar en resultados (dos filas por GSE para la gráfica)
        results.append({'Cohorte Oncológica (GSE)': gse, 'AUC Score': auc_isolated, 'Contexto del Generador': 'Cohorte Aislada (Específico)'})
        results.append({'Cohorte Oncológica (GSE)': gse, 'AUC Score': auc_harmonized, 'Contexto del Generador': 'Datalake Armonizado (Sinergia)'})
        
    df_res = pd.DataFrame(results)
    
    if len(df_res) == 0:
        print("Error: No se pudo generar suficientes resultados válidos.")
        return
        
    # Guardar CSV
    os.makedirs('results/metrics/', exist_ok=True)
    df_res.to_csv('results/metrics/elite_borda_inter_disease.csv', index=False)
    
    # Plotear Gráfica
    plt.figure(figsize=(12, 7))
    sns.set_theme(style="whitegrid")
    
    ax = sns.barplot(
        data=df_res, 
        x='Cohorte Oncológica (GSE)', 
        y='AUC Score', 
        hue='Contexto del Generador', 
        palette=['#808080', '#FF8C00']
    )
    
    plt.title('Demostración Empírica de Regularidades Inter-Enfermedades (Datos Reales)', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Fidelidad Predictiva (ROC-AUC) en Test Holdout Real', fontsize=12)
    plt.xlabel('Estudio Clínico (Cohorte Oncológica)', fontsize=12)
    plt.ylim(0.50, 1.0)
    
    # Añadir valores
    for p in ax.patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            ax.annotate(f"{height:.3f}", 
                        (p.get_x() + p.get_width() / 2., height), 
                        ha='center', va='bottom', 
                        fontsize=10, color='black', xytext=(0, 5), 
                        textcoords='offset points')
                        
    plt.legend(loc='upper right')
    plt.tight_layout()
    
    output_path = 'results/metrics/comparativa_inter_enfermedades_ELITE.png'
    plt.savefig(output_path, dpi=300)
    print(f"\n¡Éxito Científico! Gráfica real guardada en {output_path}")

if __name__ == "__main__":
    run_real_empirical_benchmark()
