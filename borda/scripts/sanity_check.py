import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def run_sanity_check(gse_id=None):
    # Cargar datos
    print("📂 Cargando base de datos...")
    df = pd.read_parquet('results/master_training_table.parquet')
    
    if gse_id is None:
        # Buscar el estudio más grande con balance de clases
        counts = df.groupby('GSE_ID')['Category'].nunique()
        valid_studies = counts[counts > 1].index
        gse_id = df[df['GSE_ID'].isin(valid_studies)].groupby('GSE_ID').size().idxmax()
        
    print(f"🕵️ Iniciando Prueba de Cordura para el estudio: {gse_id}...")
    df_study = df[df['GSE_ID'] == gse_id]
    
    if df_study.empty:
        print(f"Error: No se encontró el estudio {gse_id}")
        return

    print(f"Total de muestras en {gse_id}: {len(df_study)}")
    print(f"Distribución de clases:\n{df_study['Category'].value_counts()}")

    # Preparar X e y (usando los genes, ignorando metadatos)
    X = df_study.drop(columns=['GSE_ID', 'Technology_Label', 'Category'])
    y = df_study['Category'].astype(int)

    # Split sencillo
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    # Entrenar un Random Forest rápido
    print("\nEntrenando un Random Forest (100 árboles)...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluar
    y_pred = clf.predict(X_test)
    
    print("\n" + "="*50)
    print(f"📊 RESULTADOS PARA UN SOLO ESTUDIO ({gse_id})")
    print("="*50)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nReporte Detallado:")
    print(classification_report(y_test, y_pred))
    print("="*50)
    print("Reflexión: Si este número es alto (ej. > 0.90), el modelo SÍ sabe aprender biología.")
    print("El 0.52 que vimos antes es producto del RUIDO de mezclar 148 laboratorios.")

if __name__ == "__main__":
    run_sanity_check()
