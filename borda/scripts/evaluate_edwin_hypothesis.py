import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier

warnings.filterwarnings('ignore')

def run_edwin_hypothesis_test():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--real_path', type=str, default='results/elite_borda_training_table.parquet')
    parser.add_argument('--synth_path', type=str, default='results/synthetic_samples_elite_borda_5000.parquet')
    args = parser.parse_args()

    real_path = args.real_path
    synth_path = args.synth_path

    # Autodetectar prefijo 'datasets/' si estamos en la raíz del repositorio de Colab
    prefix = ""
    if os.path.exists("datasets") and not os.path.exists(real_path):
        if os.path.exists(os.path.join("datasets", real_path)):
            prefix = "datasets/"
            print(f"ℹ️ Detectada estructura de carpetas de Drive: usando prefijo '{prefix}'")

    real_path = os.path.join(prefix, real_path)
    synth_path = os.path.join(prefix, synth_path)
    
    if not os.path.exists(real_path) or not os.path.exists(synth_path):
        print(f"❌ Error: Faltan los archivos de datos real o sintéticos.\nReal: {real_path}\nSynth: {synth_path}")
        return
        
    df_real = pd.read_parquet(real_path)
    df_synth = pd.read_parquet(synth_path)
    
    target_col = 'Category' if 'Category' in df_real.columns else 'target'
    drop_cols = ['GSE_ID', 'Category', 'target', 'Technology_Label']
    features = [c for c in df_real.columns if c not in drop_cols]
    
    # Identificar los top 5 estudios oncológicos más grandes
    valid_gses = []
    for gse in df_real['GSE_ID'].unique():
        group = df_real[df_real['GSE_ID'] == gse]
        y_gse = group[target_col]
        counts = y_gse.value_counts()
        if len(counts) == 2 and counts.get(0.0, 0) >= 15 and counts.get(1.0, 0) >= 15:
            valid_gses.append(gse)
            
    top_5_gses = df_real[df_real['GSE_ID'].isin(valid_gses)]['GSE_ID'].value_counts().head(5).index.tolist()
    print(f"🧬 Estudios seleccionados para la validación: {top_5_gses}")
    
    results = []
    
    for gse in top_5_gses:
        print(f"\n🧪 Evaluando: {gse}")
        
        # Muestras del estudio actual
        df_gse = df_real[df_real['GSE_ID'] == gse]
        X_gse = df_gse[features]
        y_gse = df_gse[target_col].astype(int)
        
        # Split 80/20 real para este estudio
        X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
            X_gse, y_gse, test_size=0.20, random_state=42, stratify=y_gse
        )
        
        # --- RÉGIMEN DE DATOS LIMITADOS (Simulando escasez local: 30 muestras de entrenamiento) ---
        # Tomar un subset de entrenamiento local de 30 muestras
        n_low = min(30, len(y_train_r))
        if n_low < len(y_train_r):
            X_train_r_low, _, y_train_r_low, _ = train_test_split(
                X_train_r, y_train_r, train_size=n_low, random_state=42, stratify=y_train_r
            )
        else:
            X_train_r_low, y_train_r_low = X_train_r, y_train_r
        
        # 1. Modelo Local Aislado (Escaso)
        clf_isolated_low = XGBClassifier(n_estimators=100, max_depth=3, random_state=42, n_jobs=-1, eval_metric='logloss')
        clf_isolated_low.fit(X_train_r_low, y_train_r_low)
        preds_isolated_low = clf_isolated_low.predict_proba(X_test_r)[:, 1]
        auc_isolated_low = roc_auc_score(y_test_r, preds_isolated_low)
        
        # 2. Modelo Aumentado con Muestras Sintéticas (30 Reales + 500 Sintéticas)
        # Tomar sintéticos del mismo target class
        df_synth_subset = df_synth.sample(n=500, random_state=42)
        X_synth_subset = df_synth_subset[features]
        y_synth_subset = df_synth_subset[target_col].astype(int)
        
        X_combined = pd.concat([X_train_r_low, X_synth_subset])
        y_combined = pd.concat([y_train_r_low, y_synth_subset])
        
        clf_augmented = XGBClassifier(n_estimators=100, max_depth=3, random_state=42, n_jobs=-1, eval_metric='logloss')
        clf_augmented.fit(X_combined, y_combined)
        preds_augmented = clf_augmented.predict_proba(X_test_r)[:, 1]
        auc_augmented = roc_auc_score(y_test_r, preds_augmented)
        
        # 3. Modelo Global Real (Sinergia Completa de Datos Reales de Otros Cánceres)
        # Entrenar con toda la base real excepto el test-set de este estudio
        df_global_train = df_real.drop(X_test_r.index)
        X_global = df_global_train[features]
        y_global = df_global_train[target_col].astype(int)
        
        clf_global = XGBClassifier(n_estimators=100, max_depth=3, random_state=42, n_jobs=-1, eval_metric='logloss')
        clf_global.fit(X_global, y_global)
        preds_global = clf_global.predict_proba(X_test_r)[:, 1]
        auc_global = roc_auc_score(y_test_r, preds_global)
        
        # --- RÉGIMEN DE DATOS COMPLETOS (Para comparar cuando no hay escasez) ---
        clf_isolated_full = XGBClassifier(n_estimators=100, max_depth=3, random_state=42, n_jobs=-1, eval_metric='logloss')
        clf_isolated_full.fit(X_train_r, y_train_r)
        preds_isolated_full = clf_isolated_full.predict_proba(X_test_r)[:, 1]
        auc_isolated_full = roc_auc_score(y_test_r, preds_isolated_full)
        
        print(f"    [Escaso]  Local: {auc_isolated_low:.3f} | Aumentado (Sintético): {auc_augmented:.3f} | Sinergia Global (Real): {auc_global:.3f}")
        print(f"    [Completo] Local: {auc_isolated_full:.3f}")
        
        # Guardar resultados
        results.append({
            'Study': gse,
            'Local_Isolated_Low': auc_isolated_low,
            'Augmented_Low': auc_augmented,
            'Global_Synergy_Real': auc_global,
            'Local_Isolated_Full': auc_isolated_full
        })
        
    df_results = pd.DataFrame(results)
    metrics_dir = os.path.join(prefix, 'results/metrics')
    os.makedirs(metrics_dir, exist_ok=True)
    csv_out = os.path.join(metrics_dir, 'edwin_hypothesis_results.csv')
    df_results.to_csv(csv_out, index=False)
    print(f"\n💾 Resultados guardados en {csv_out}")
    
    # Graficar
    df_melt = pd.melt(df_results, id_vars=['Study'], value_vars=['Local_Isolated_Low', 'Augmented_Low', 'Global_Synergy_Real'],
                      var_name='Configuración', value_name='ROC-AUC')
    
    # Traducir nombres para el gráfico
    name_map = {
        'Local_Isolated_Low': 'Modelo Local (Solo 30 Reales)',
        'Augmented_Low': 'Modelo Aumentado (30 Reales + Sintéticos)',
        'Global_Synergy_Real': 'Sinergia Global (Todos los Cánceres Reales)'
    }
    df_melt['Configuración'] = df_melt['Configuración'].map(name_map)
    
    plt.figure(figsize=(14, 7))
    sns.set_theme(style="whitegrid")
    
    ax = sns.barplot(
        data=df_melt,
        x='Study',
        y='ROC-AUC',
        hue='Configuración',
        palette=['#d95f02', '#1b9e77', '#7570b3']
    )
    
    # Dibujar los baselines "Full" como líneas horizontales de referencia por estudio
    for i, gse in enumerate(top_5_gses):
        full_auc = df_results[df_results['Study'] == gse]['Local_Isolated_Full'].values[0]
        # Dibujar una línea corta para representar el baseline completo
        plt.hlines(y=full_auc, xmin=i-0.4, xmax=i+0.4, colors='red', linestyles='--', linewidth=1.5)
        if i == 0:
            # Añadir etiqueta para la línea roja
            plt.plot([], [], color='red', linestyle='--', label='Límite Superior (Entrenamiento Real Completo)')
            
    plt.title('Evaluación de la Hipótesis de Edwin: Regularidades Inter-Enfermedades y Aumentación', fontsize=15, fontweight='bold', pad=20)
    plt.ylabel('Desempeño Diagnóstico (ROC-AUC) en Test Real', fontsize=12)
    plt.xlabel('Estudio Clínico (Cohorte Oncológica)', fontsize=12)
    plt.ylim(0.40, 1.05)
    plt.legend(loc='lower right', fontsize=10)
    
    # Añadir valores numéricos encima de las barras
    for p in ax.patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            ax.annotate(f"{height:.3f}", 
                        (p.get_x() + p.get_width() / 2., height), 
                        ha='center', va='bottom', 
                        fontsize=9, color='black', xytext=(0, 3), 
                        textcoords='offset points')
            
    plt.tight_layout()
    img_out = os.path.join(metrics_dir, 'validacion_hipothesis_edwin.png')
    plt.savefig(img_out, dpi=300)
    print(f"🎨 Gráfica guardada en {img_out}")

if __name__ == "__main__":
    run_edwin_hypothesis_test()
