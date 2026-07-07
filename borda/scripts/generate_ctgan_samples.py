import joblib
import pandas as pd
import argparse
import os
import time
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description="CTGAN — Generación Optimizada por Lotes (Chunks)")
    parser.add_argument('--dataset', type=str, default='elite_borda', help="Dataset a usar")
    parser.add_argument('--n_samples', type=int, default=120000, help="Número de muestras a generar")
    parser.add_argument('--chunk_size', type=int, default=20000, help="Tamaño de cada lote para evitar OOM")
    args = parser.parse_args()

    print("============================================================")
    print("🎲 CTGAN — Generación Optimizada por Lotes (Chunks)")
    print("============================================================")
    print(f"  Dataset:     {args.dataset}")
    print(f"  Muestras:    {args.n_samples}")
    print(f"  Lote (Chunk): {args.chunk_size}")
    print("============================================================")

    model_path = f'results/ctgan_model_{args.dataset}.pkl'
    output_path = f'results/synthetic_samples_ctgan_{args.dataset}_{args.n_samples}.parquet'

    if not os.path.exists(model_path):
        print(f"❌ Error: No se encontró el modelo CTGAN en: {model_path}")
        return

    print(f"\n🧠 Cargando modelo CTGAN ({model_path})...")
    load_start = time.time()
    model = joblib.load(model_path)
    print(f"   ✅ Modelo cargado en {time.time() - load_start:.1f} segundos.")

    # Generación en lotes para evitar picos de memoria
    chunks = []
    n_chunks = args.n_samples // args.chunk_size
    remainder = args.n_samples % args.chunk_size

    print(f"\n🚀 Iniciando generación de {args.n_samples} muestras en GPU/CPU...")
    gen_start = time.time()

    for i in tqdm(range(n_chunks), desc="Lotes Generados"):
        chunks.append(model.sample(args.chunk_size))

    if remainder > 0:
        print(f"📥 Generando lote final de {remainder} muestras...")
        chunks.append(model.sample(remainder))

    synthetic_df = pd.concat(chunks, ignore_index=True)

    # Ajustar categorías discretas a enteros biológicos
    discrete_columns = ['Technology_Label', 'Category']
    for col in discrete_columns:
        if col in synthetic_df.columns:
            synthetic_df[col] = synthetic_df[col].round().clip(0, 1).astype(int)

    synthetic_df.to_parquet(output_path)
    duration = (time.time() - gen_start) / 60
    print(f"\n✅ Guardado exitosamente en: {output_path} (Completado en {duration:.2f} minutos)")

if __name__ == "__main__":
    main()
