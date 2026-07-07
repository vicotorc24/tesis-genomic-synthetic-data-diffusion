import pandas as pd
import numpy as np
import os
from sklearn.neighbors import KNeighborsRegressor
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

def calculate_plc(actual_rankings, predicted_rankings):
    """
    PLC: Diferencia entre el mejor AUC global y el mejor encontrado 
    en el Top-N del ranking predicho.
    """
    # Encontramos la posición de cada algoritmo en el ranking predicho
    # y evaluamos el 'acierto' acumulado.
    n_algs = len(actual_rankings)
    best_overall = np.max(actual_rankings)
    
    # Ordenamos los índices de los algoritmos por su predicción (de mejor a peor)
    sorted_idx = np.argsort(predicted_rankings)[::-1]
    
    plc_curve = []
    current_best = -1
    for i in range(1, n_algs + 1):
        # Tomamos el mejor desempeño real encontrado hasta la posición i del ranking
        top_n_idx = sorted_idx[:i]
        current_best = np.max(actual_rankings[top_n_idx])
        loss = best_overall - current_best
        plc_curve.append(loss)
        
    return plc_curve

def run_loo_evaluation():
    # 1. Cargar datos
    meta_path = 'results/MASTER_METAFEATURES_2021_2026.csv'
    perf_path = 'results/REPRODUCED_MATRIX_2021.csv'
    
    if not (os.path.exists(meta_path) and os.path.exists(perf_path)):
        print("❌ Faltan archivos de datos. Asegúrate de terminar la Fase 2.")
        return

    meta_df = pd.read_csv(meta_path).fillna(0)
    perf_df = pd.read_csv(perf_path).fillna(0)
    
    # Unir datos directamente (ambos tienen el prefijo dataset_ o coinciden)
    data = pd.merge(meta_df, perf_df, on='dataset').fillna(0)
    
    if data.empty:
        print("⚠️ Advertencia: No se pudieron unir las matrices. Verificando nombres...")
        print(f"   Meta Datasets Sample: {meta_df['dataset'].iloc[0]}")
        print(f"   Perf Datasets Sample: {perf_df['dataset'].iloc[0]}")
        return
    
    # Separar X (Metafeatures) y Y (Performances de los 24 pares)
    # Eliminamos columnas no numéricas o identificadores
    X_cols = [c for c in meta_df.columns if c not in ['dataset']]
    Y_cols = [c for c in perf_df.columns if c not in ['dataset']]
    
    X = data[X_cols].values
    Y = data[Y_cols].values
    
    n_datasets = len(data)
    n_pairs = len(Y_cols)
    
    print(f"📊 Evaluando Metalearning sobre {n_datasets} datasets y {n_pairs} pares de algoritmos...")
    
    results_k = []
    
    # 2. Barrer K de 1 a N-1 (Leave-One-Out)
    for k in range(1, n_datasets):
        spearman_scores = []
        plc_curves = []
        
        for i in range(n_datasets):
            # LOO: i es el test, todos los demás son train
            X_train = np.delete(X, i, axis=0)
            Y_train = np.delete(Y, i, axis=0)
            X_test = X[i].reshape(1, -1)
            Y_test = Y[i]
            
            # Entrenar KNN Regressor
            model = KNeighborsRegressor(n_neighbors=k, weights='distance')
            model.fit(X_train, Y_train)
            
            # Predecir performances (vector de 24 valores)
            y_pred = model.predict(X_test)[0]
            
            # Calcular Spearman
            corr, _ = spearmanr(Y_test, y_pred)
            if not np.isnan(corr):
                spearman_scores.append(corr)
            
            # Calcular PLC
            plc = calculate_plc(Y_test, y_pred)
            plc_curves.append(plc)
            
        avg_spearman = np.mean(spearman_scores)
        avg_plc_curve = np.mean(plc_curves, axis=0)
        
        results_k.append({
            'k': k,
            'spearman_mean': avg_spearman,
            'plc_at_n1': avg_plc_curve[0], # Pérdida al elegir solo el Top 1
            'plc_avg': np.mean(avg_plc_curve)
        })
        
        if k % 10 == 0:
            print(f"   K={k} -> Spearman: {avg_spearman:.4f}, PLC(Top-1): {avg_plc_curve[0]:.4f}")

    # 3. Guardar resultados y generar gráficos
    final_results = pd.DataFrame(results_k)
    final_results.to_csv('results/METALEARNING_EVALUATION_K.csv', index=False)
    
    # Graficar Spearman vs K
    plt.figure(figsize=(10, 5))
    plt.plot(final_results['k'], final_results['spearman_mean'], marker='o', label='Spearman')
    plt.title('Evaluación del Modelo: Coef. Spearman vs K')
    plt.xlabel('K')
    plt.ylabel('Coef. Spearman')
    plt.grid(True)
    plt.savefig('results/PLOT_SPEARMAN_VS_K.png')
    
    # Graficar PLC vs K (Promedio de PLC)
    plt.figure(figsize=(10, 5))
    plt.plot(final_results['k'], final_results['plc_at_n1'], color='red', marker='x', label='PLC Top-1')
    plt.title('Curva de Pérdida de Rendimiento (PLC) vs K')
    plt.xlabel('K')
    plt.ylabel('Performance Loss')
    plt.grid(True)
    plt.savefig('results/PLOT_PLC_VS_K.png')
    
    print("\n✅ Evaluación LOO completada. Gráficos guardados en 'results/'.")

if __name__ == "__main__":
    run_loo_evaluation()
