import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import time

def run_pseudo_labeler():
    real_path = 'results/optimal_training_table.parquet'
    synth_path = 'results/synthetic_samples_optimal_120000.parquet'
    
    print(f"\n{'='*60}")
    print(f"👨‍⚕️ Iniciando Médico Virtual (Pseudo-Labeling Post-Hoc)")
    print(f"{'='*60}")
    
    # 1. Cargar datos reales para entrenar al médico
    print(f"📥 Cargando datos biológicos reales desde {real_path}...")
    df_real = pd.read_parquet(real_path)
    target_col = 'Category' if 'Category' in df_real.columns else 'target'
    
    if target_col not in df_real.columns:
        print("❌ Error: Los datos reales no tienen columna de diagnóstico (Category).")
        return
        
    df_real = df_real.dropna(subset=[target_col])
    
    # Aislar variables (quitamos GSE_ID y Target)
    cols_to_drop = [col for col in ['GSE_ID', target_col, 'target'] if col in df_real.columns]
    X_real = df_real.drop(columns=cols_to_drop)
    y_real = df_real[target_col].astype(int)
    
    print(f"   📐 Muestras reales: {len(X_real):,} | Genes: {X_real.shape[1]}")
    
    # 2. Entrenar el Médico Virtual (XGBoost)
    print("\n🧠 Entrenando al Médico Virtual (XGBoost SOTA)...")
    start = time.time()
    # Usamos parámetros rigurosos para máxima confiabilidad clínica
    clf = XGBClassifier(
        n_estimators=200, 
        max_depth=7, 
        learning_rate=0.05, 
        n_jobs=-1, 
        random_state=42,
        eval_metric='logloss'
    )
    clf.fit(X_real, y_real)
    print(f"   ✅ Entrenamiento completado en {time.time() - start:.2f} segundos.")
    
    # 3. Cargar Pacientes Sintéticos
    print(f"\n📥 Cargando pacientes sintéticos (sin etiquetar) desde {synth_path}...")
    df_synth = pd.read_parquet(synth_path)
    
    # Asegurarnos de que las columnas están en el mismo orden exacto
    missing_cols = [col for col in X_real.columns if col not in df_synth.columns]
    if missing_cols:
        print(f"❌ Error: A los sintéticos les faltan {len(missing_cols)} genes presentes en los reales.")
        return
        
    X_synth = df_synth[X_real.columns]
    print(f"   📐 Pacientes sintéticos a diagnosticar: {len(X_synth):,}")
    
    # 4. Diagnóstico (Pseudo-Labeling)
    print("\n🩺 Realizando diagnóstico masivo...")
    y_pred = clf.predict(X_synth)
    
    # Calcular métricas de balance (cuántos sanos vs enfermos generó la difusión)
    cancer_count = np.sum(y_pred == 1)
    normal_count = np.sum(y_pred == 0)
    print(f"   📊 Resultados del diagnóstico:")
    print(f"      🔴 Tejido Tumoral (1): {cancer_count:,} ({(cancer_count/len(y_pred))*100:.1f}%)")
    print(f"      🟢 Tejido Sano (0):   {normal_count:,} ({(normal_count/len(y_pred))*100:.1f}%)")
    
    # 5. Estampar la etiqueta en el DataFrame Sintético
    df_synth[target_col] = y_pred
    
    # Guardar sobreescribiendo el archivo para que el benchmark lo lea directo
    print(f"\n💾 Guardando pacientes diagnosticados...")
    df_synth.to_parquet(synth_path)
    print(f"🎉 ¡Éxito! Archivo actualizado y listo para el Benchmark TSTR.")

if __name__ == "__main__":
    run_pseudo_labeler()
