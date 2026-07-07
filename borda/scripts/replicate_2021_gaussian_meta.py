import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

def replicate_gaussian_synthesis():
    meta_path = 'results/MASTER_METAFEATURES_2021_2026.csv'
    perf_path = 'results/REPRODUCED_MATRIX_2021.csv'
    
    if not os.path.exists(meta_path) or not os.path.exists(perf_path):
        print("❌ Archivos base no encontrados.")
        return

    meta_df = pd.read_csv(meta_path).fillna(0)
    perf_df = pd.read_csv(perf_path).fillna(0)
    
    # Unir datos para asegurar alineación
    data = pd.merge(meta_df, perf_df, on='dataset')
    
    # Separar identificadores, metafeatures y performances
    ids = data[['dataset']]
    X_cols = [c for c in meta_df.columns if c != 'dataset']
    Y_cols = [c for c in perf_df.columns if c != 'dataset']
    
    X = data[X_cols]
    Y = data[Y_cols]
    
    # ESTANDARIZACIÓN (Z-Score) - Clave del descubrimiento de Ingeniería Inversa
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X_cols).fillna(0)
    
    sigmas = [0.001, 0.01, 0.1, 0.2]
    scenarios = [1, 3] # 1r+1s y 1r+3s
    
    output_dir = 'results/gaussian_scenarios'
    os.makedirs(output_dir, exist_ok=True)
    
    for sigma in sigmas:
        for n_syn in scenarios:
            # Empezamos con la data real
            X_aug = [X_scaled]
            Y_aug = [Y]
            
            # Generamos N copias perturbadas
            for i in range(n_syn):
                noise = np.random.normal(0, sigma, X_scaled.shape)
                X_noisy = X_scaled + noise
                X_aug.append(X_noisy)
                Y_aug.append(Y)
            
            # Concatenamos el escenario completo
            X_final = pd.concat(X_aug, ignore_index=True)
            Y_final = pd.concat(Y_aug, ignore_index=True)
            
            # Guardamos
            scenario_df = pd.concat([X_final, Y_final], axis=1)
            # Re-añadimos identificadores (solo para referencia, el dataset original se repite)
            # scenario_df['dataset_ref'] = np.repeat(ids['dataset'].values, n_syn + 1)
            
            filename = f"{output_dir}/AUG_META_S{str(sigma).replace('.','')}_1R{n_syn}S.csv"
            scenario_df.to_csv(filename, index=False)
            print(f"✅ Escenario Sigma {sigma} (1R+{n_syn}S) generado con {len(scenario_df)} instancias.")

if __name__ == "__main__":
    replicate_gaussian_synthesis()
