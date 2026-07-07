import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import os
import glob

def calculate_plc(y_true, y_pred, k_range=range(1, 25)):
    """Calcula la pérdida de rendimiento para el top-K predicho."""
    results = []
    # Convertimos a ranking (desempeño -> ranking, mayor es mejor)
    # y_true es un vector de AUCs
    true_best_idx = np.argsort(y_true)[::-1]
    true_max = y_true[true_best_idx[0]]
    
    pred_best_indices = np.argsort(y_pred)[::-1]
    
    for k in k_range:
        current_top_indices = pred_best_indices[:k]
        best_in_top_k = np.max(y_true[current_top_indices])
        loss = true_max - best_in_top_k
        results.append(loss)
    return results

def evaluate_scenarios():
    output_dir = 'results/gaussian_scenarios'
    perf_path = 'results/REPRODUCED_MATRIX_2021.csv'
    meta_path = 'results/MASTER_METAFEATURES_2021_2026.csv'
    
    real_meta = pd.read_csv(meta_path).fillna(0)
    real_perf = pd.read_csv(perf_path).fillna(0)
    real_data = pd.merge(real_meta, real_perf, on='dataset').fillna(0)
    
    datasets = real_data['dataset'].unique()
    n_datasets = len(datasets)
    
    scenario_files = glob.glob(f"{output_dir}/*.csv")
    
    overall_results = []
    
    for file in scenario_files:
        scenario_name = os.path.basename(file).replace('.csv', '')
        print(f"🧐 Evaluando Escenario: {scenario_name}")
        
        df = pd.read_csv(file).fillna(0)
        
        # Metafeatures cols (todas menos los performances de los 24 pares)
        # En el escenario generado, X_cols son las primeras, Y_cols son las últimas 24
        Y_cols = [c for c in real_perf.columns if c != 'dataset']
        X_cols = [c for c in df.columns if c not in Y_cols]
        
        spearmans = []
        plcs = []
        
        # LEAVE-ONE-OUT POR DATASET (No por fila)
        for i in range(n_datasets):
            test_ds = datasets[i]
            
            # El conjunto de test es la fila REAL del dataset excluido
            test_row = real_data[real_data['dataset'] == test_ds]
            X_test = test_row[X_cols]
            Y_test = test_row[Y_cols].values.flatten()
            
            # El conjunto de entrenamiento son TODOS los otros datasets y sus clones
            # Para identificar el dataset original en la matriz aumentada, asumimos que se repite el patrón
            # de 60 rows reales -> 60 rows noisy1 -> 60 rows noisy2...
            # Así que calculamos el índice relativo
            indices_to_drop = []
            for j in range(len(df)//n_datasets):
                indices_to_drop.append(i + (j * n_datasets))
                
            train_df = df.drop(indices_to_drop)
            
            X_train = train_df[X_cols]
            Y_train = train_df[Y_cols]
            
            # Entrenar KNN (K=5 base como en la tesis)
            knn = KNeighborsRegressor(n_neighbors=5)
            knn.fit(X_train, Y_train)
            
            # Predecir ranking para el dataset excluido
            y_pred = knn.predict(X_test)[0]
            
            # Métricas
            corr, _ = spearmanr(Y_test, y_pred)
            if not np.isnan(corr):
                spearmans.append(corr)
                
            plcs.append(calculate_plc(Y_test, y_pred))
            
        overall_results.append({
            'scenario': scenario_name,
            'spearman_mean': np.mean(spearmans),
            'plc_mean': np.mean(plcs, axis=0)
        })

    # Guardar resultados y graficar
    results_df = pd.DataFrame(overall_results)
    print("\n🏆 RESULTADOS FINALES DE LA RÉPLICA:")
    print(results_df[['scenario', 'spearman_mean']])
    
    # Graficar Spearman comparativo
    plt.figure(figsize=(10, 6))
    plt.bar(results_df['scenario'], results_df['spearman_mean'], color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title('Comparativa de Spearman vs Escenario de Aumento (2021)')
    plt.ylabel('Coeficiente de Spearman (Promedio LOO)')
    plt.tight_layout()
    plt.savefig('results/REPLICA_SPEARMAN_COMPARISON.png')
    
    # Graficar PLC comparativo
    plt.figure(figsize=(10, 6))
    for res in overall_results:
        plt.plot(range(1, 25), res['plc_mean'], label=res['scenario'])
    plt.title('Curvas de Pérdida (PLC) por Escenario 2021')
    plt.xlabel('Top-N Algoritmos Probados')
    plt.ylabel('Pérdida de AUC respecto al óptimo')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('results/REPLICA_PLC_COMPARISON.png')

if __name__ == "__main__":
    evaluate_scenarios()
