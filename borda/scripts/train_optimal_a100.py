import pandas as pd
import numpy as np
from ForestDiffusion import ForestDiffusionModel
from xgboost import XGBRegressor
import joblib
import os
import time
import argparse
import gc

# ─────────────────────────────────────────────────────────────────────────────
# CLASE HEREDADA: inicializa el modelo sin entrenar (solo metadata + scaler)
# ─────────────────────────────────────────────────────────────────────────────
class CheckpointForestDiffusionModel(ForestDiffusionModel):
    def __init__(self, X, n_t=50, duplicate_K=1, cat_indexes=[], bin_indexes=[], int_indexes=[]):
        assert isinstance(X, np.ndarray), "Input must be Numpy array"
        np.random.seed(666)

        obs_to_remove = np.isnan(X).any(axis=1)
        X = X[~obs_to_remove]
        self.p_in_one = True

        self.X_min = np.nanmin(X, axis=0, keepdims=True)
        self.X_max = np.nanmax(X, axis=0, keepdims=True)
        self.cat_indexes = cat_indexes
        self.int_indexes = int_indexes + bin_indexes

        from sklearn.preprocessing import MinMaxScaler
        self.scaler = MinMaxScaler(feature_range=(-1, 1))
        X = self.scaler.fit_transform(X)

        self.b, self.c = X.shape
        self.c_all = self.c
        self.n_t = n_t
        self.duplicate_K = duplicate_K
        self.model = 'xgboost'
        self.n_estimators = 100
        self.max_depth = 7
        self.seed = 666
        self.eta = 0.1
        self.gpu_hist = False
        self.label_y = None
        self.n_jobs = 1

        self.y_probs = np.array([1.0])
        self.y_uniques = np.array([0])
        self.diffusion_type = 'flow'
        self.n_batch = 1
        self.regr = [[None for _ in range(n_t)]]


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIÓN DE ENSAMBLAJE
# ─────────────────────────────────────────────────────────────────────────────
def assemble_model(steps_dir, shell_path, final_model_path, n_t):
    existing_steps = sorted([
        int(f.split('_')[1].split('.')[0])
        for f in os.listdir(steps_dir)
        if f.startswith('step_') and f.endswith('.joblib')
    ])

    print(f"\n🔍 Pasos encontrados en {steps_dir}: {len(existing_steps)}/{n_t}")

    if len(existing_steps) < n_t:
        missing = [t for t in range(n_t) if t not in existing_steps]
        print(f"❌ Faltan {len(missing)} pasos. Descárgalos y vuelve a ejecutar.")
        return False

    print(f"✅ Todos los {n_t} pasos presentes. Iniciando ensamblaje...")
    print(f"   📦 Destino: {final_model_path}\n")

    model = joblib.load(shell_path)
    n_features = model.c

    model.regr_ = [[[None for _ in range(n_features)] for _ in range(n_t)] for _ in range(1)]

    assemble_start = time.time()
    for t in range(n_t):
        step_file = os.path.join(steps_dir, f"step_{t}.joblib")
        feature_models = joblib.load(step_file)
        for k in range(n_features):
            model.regr_[0][t][k] = feature_models[k]
        del feature_models
        gc.collect()

        elapsed = time.time() - assemble_start
        eta = (elapsed / (t + 1)) * (n_t - t - 1)
        print(f"   📥 [{t+1:>2}/{n_t}] cargado — ETA restante: {eta/60:.1f} min    ", end="\r")

    model.p_in_one = False
    print(f"\n\n💾 Guardando modelo maestro (compress=0)...")
    joblib.dump(model, final_model_path, compress=0)

    elapsed_total = (time.time() - assemble_start) / 60
    final_size_gb = os.path.getsize(final_model_path) / 1e9
    print(f"\n🎉 ¡ENSAMBLAJE COMPLETADO en {elapsed_total:.1f} min!")
    print(f"📦 Modelo maestro: {final_size_gb:.1f} GB → {final_model_path}")
    return True


# ─────────────────────────────────────────────────────────────────────────────
# ENTRENAMIENTO SOTA OPTIMIZADO PARA A100
# ─────────────────────────────────────────────────────────────────────────────
def train_with_checkpoints():
    parser = argparse.ArgumentParser(description="Forest Diffusion SOTA A100")
    # HARDCODED: El dataset por defecto ahora es el Óptimo
    parser.add_argument('--dataset', type=str, default='optimal')
    parser.add_argument('--n_t', type=int, default=50)
    parser.add_argument('--max_steps', type=int, default=None)
    # HARDCODED: Device por defecto a cuda para forzar el uso de la A100
    parser.add_argument('--device', type=str, default='cuda', choices=['cpu', 'cuda'])
    parser.add_argument('--mode', type=str, default='both', choices=['train', 'assemble', 'both'])
    parser.add_argument('--input', type=str, default=None)
    parser.add_argument('--steps_dir', type=str, default=None)
    args, _ = parser.parse_known_args()

    input_path     = args.input or f'results/{args.dataset}_training_table.parquet'
    checkpoint_dir = 'results/checkpoints/'
    steps_dir      = args.steps_dir or os.path.join(checkpoint_dir, f'steps_{args.dataset}')
    os.makedirs(steps_dir, exist_ok=True)

    shell_path       = os.path.join(checkpoint_dir, f"fd_shell_{args.dataset}.joblib")
    final_model_path = os.path.join('results', f"forest_diffusion_model_{args.dataset}.joblib")

    print(f"\n{'='*60}")
    print(f"🚀 Forest Diffusion — OPTIMIZACIÓN A100 (BRAZO ÓPTIMO)")
    print(f"{'='*60}")
    print(f"  Dataset:   {args.dataset}")
    print(f"  Device:    {args.device.upper()} (Forzado para Tensor Cores)")
    print(f"  Steps dir: {steps_dir}")
    print(f"{'='*60}\n")

    if args.mode == 'assemble':
        assemble_model(steps_dir, shell_path, final_model_path, args.n_t)
        return

    print(f"📥 Cargando dataset óptimo desde: {input_path}")
    df = pd.read_parquet(input_path)
    df_train = df.drop(columns=['GSE_ID', 'Category', 'target'], errors='ignore')
    X_train = df_train.to_numpy().astype(np.float32)
    print(f"   📐 {X_train.shape[0]:,} muestras × {X_train.shape[1]:,} features")

    existing_steps = sorted([
        int(f.split('_')[1].split('.')[0])
        for f in os.listdir(steps_dir)
        if f.startswith('step_') and f.endswith('.joblib')
    ])

    if os.path.exists(shell_path):
        print(f"\n🔄 Shell detectado — reanudando sesión previa")
        model = joblib.load(shell_path)
        start_step = max(existing_steps) + 1 if existing_steps else 0
        print(f"   ✅ Pasos completados: {len(existing_steps)}/{args.n_t}")
        print(f"   ▶️  Reanudando desde el paso {start_step + 1}")
    else:
        print(f"\n🆕 Primera ejecución — inicializando modelo")
        model = CheckpointForestDiffusionModel(X_train, n_t=args.n_t)
        start_step = 0
        shell_regr_backup = model.regr
        model.regr = [[None for _ in range(args.n_t)]]
        joblib.dump(model, shell_path, compress=3)
        model.regr = shell_regr_backup

    # ── OPTIMIZACIÓN PARA A100 ────────────────────────────────────────────────
    xgb_kwargs_single = {
        'n_estimators': 100,
        'max_depth': 7,
        'learning_rate': 0.3,
        'tree_method': 'hist',
        'device': args.device,
        'n_jobs': 1 # Dejamos que joblib controle los hilos
    }

    X_scaled = model.scaler.transform(X_train)
    n_features = X_scaled.shape[1]

    from joblib import Parallel, delayed

    def train_single_feature(X_input, y_single, xgb_kw):
        mdl = XGBRegressor(**xgb_kw)
        mdl.fit(X_input, y_single)
        return mdl

    session_start = time.time()
    steps_done_this_session = 0
    
    # OPTIMIZACIÓN: Limitar hilos a 12 (Núcleos de la A100) para evitar 
    # cuellos de botella en la memoria de la GPU (CUDA OOM Contexts).
    parallel_jobs = 12 if args.device == 'cuda' else -1

    print(f"\n🧬 Iniciando entrenamiento paralelo (Limitado a {parallel_jobs} hilos)\n")

    for t in range(start_step, args.n_t):
        if args.max_steps is not None and steps_done_this_session >= args.max_steps:
            print(f"\n🛑 Límite de sesión alcanzado.")
            break

        step_file = os.path.join(steps_dir, f"step_{t}.joblib")
        if os.path.exists(step_file):
            continue

        step_start = time.time()
        print(f"⏳ [Paso {t+1:>2}/{args.n_t}] Entrenando {n_features} bosques...", flush=True)

        alpha = (t + 1) / args.n_t
        noise = np.random.normal(0, 1, X_scaled.shape).astype(np.float32)
        X_t = (1 - alpha) * X_scaled + alpha * noise
        # OPTIMIZACIÓN A100: En GPU, paralelizar por genes es un anti-patrón porque la GPU ya 
        # paraleliza internamente. Enviar miles de hilos satura el bus PCIe y bloquea Python (GIL).
        # Un bucle secuencial alimenta la GPU rapidísimo sin choques de memoria.
        feature_models = []
        for k in range(n_features):
            mdl = train_single_feature(X_t, Y_t[:, k], xgb_kwargs_single)
            feature_models.append(mdl)
            
        joblib.dump(feature_models, step_file, compress=0)

        # Limpieza profunda de RAM y VRAM
        del noise, X_t, Y_t, feature_models
        gc.collect()

        duration = time.time() - step_start
        step_size_mb = os.path.getsize(step_file) / 1e6
        steps_done_this_session += 1

        elapsed_session = time.time() - session_start
        avg_per_step = elapsed_session / steps_done_this_session
        remaining = args.n_t - t - 1
        eta_h = (avg_per_step * remaining) / 3600

        print(f"   ✅ Completado en {duration/60:.1f} min | {step_size_mb:.0f} MB | ETA: {eta_h:.1f}h")

    if args.mode == 'both':
        assemble_model(steps_dir, shell_path, final_model_path, args.n_t)


if __name__ == "__main__":
    train_with_checkpoints()
