"""
train_fd_colab.py — Forest Diffusion para Google Colab GPU
===========================================================
Script autónomo optimizado para ejecutarse en Google Colab con GPU T4/A100.
Sube este archivo a tu Google Drive y ejecútalo desde Colab.

Características:
  - Detecta y usa GPU automáticamente
  - Guarda checkpoints individuales en Google Drive (compress=0, instantáneo)
  - Reanuda automáticamente si la sesión se interrumpe
  - Ensambla el modelo final al completar todos los pasos
  - Benchmark integrado para calcular ETA real antes de lanzar

Uso básico en Colab:
  !python /content/drive/MyDrive/datasets/scripts/train_fd_colab.py

Con benchmark previo (recomendado en primera sesión):
  !python /content/drive/MyDrive/datasets/scripts/train_fd_colab.py --benchmark

Solo ensamblar pasos ya descargados:
  !python /content/drive/MyDrive/datasets/scripts/train_fd_colab.py --mode assemble
"""

import pandas as pd
import numpy as np
import joblib
import os
import time
import argparse
import gc
import sys

# ─────────────────────────────────────────────────────────────────────────────
# DETECCIÓN DE ENTORNO
# ─────────────────────────────────────────────────────────────────────────────
IN_COLAB = 'google.colab' in sys.modules
try:
    import google.colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False


def detect_device():
    """Detecta si hay GPU disponible y configura el dispositivo."""
    try:
        import subprocess
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            # Extraer nombre de GPU
            lines = [l for l in result.stdout.split('\n') if 'Tesla' in l or 'A100' in l or 'T4' in l or 'V100' in l]
            gpu_name = lines[0].strip() if lines else "GPU detectada"
            print(f"🚀 GPU disponible: {gpu_name}")
            return 'cuda'
    except Exception:
        pass
    print("⚠️  No se detectó GPU. Usando CPU (más lento).")
    return 'cpu'


def get_drive_base():
    """Retorna la ruta base de Google Drive si está montado."""
    candidates = [
        '/content/drive/MyDrive',
        '/content/drive/My Drive',
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


# ─────────────────────────────────────────────────────────────────────────────
# CLASE DEL MODELO (heredada de ForestDiffusion)
# ─────────────────────────────────────────────────────────────────────────────
class CheckpointForestDiffusionModel:
    """
    Inicializa el modelo Forest Diffusion sin entrenar.
    Guarda solo metadata y scaler para poder reanudar entrenamiento.
    """
    def __init__(self, X, n_t=50):
        from sklearn.preprocessing import MinMaxScaler

        assert isinstance(X, np.ndarray), "Input debe ser numpy array"
        np.random.seed(666)

        obs_to_remove = np.isnan(X).any(axis=1)
        X = X[~obs_to_remove]
        if obs_to_remove.sum() > 0:
            print(f"   ⚠️  Se eliminaron {obs_to_remove.sum()} filas con NaN")

        self.X_min = np.nanmin(X, axis=0, keepdims=True)
        self.X_max = np.nanmax(X, axis=0, keepdims=True)
        self.cat_indexes = []
        self.int_indexes = []

        self.scaler = MinMaxScaler(feature_range=(-1, 1))
        X = self.scaler.fit_transform(X)

        self.b, self.c = X.shape
        self.c_all = self.c
        self.n_t = n_t
        self.duplicate_K = 1
        self.model = 'xgboost'
        self.n_estimators = 100
        self.max_depth = 7
        self.seed = 666
        self.eta = 0.1
        self.gpu_hist = False
        self.label_y = None
        self.n_jobs = 1
        self.p_in_one = True

        self.y_probs = np.array([1.0])
        self.y_uniques = np.array([0])
        self.diffusion_type = 'flow'
        self.n_batch = 1
        self.regr = [[None for _ in range(n_t)]]


# ─────────────────────────────────────────────────────────────────────────────
# BENCHMARK: mide velocidad real en GPU para calibrar n_t
# ─────────────────────────────────────────────────────────────────────────────
def run_benchmark(X_scaled, device, n_features, n_samples):
    """
    Entrena 1 paso completo y mide el tiempo real.
    Calcula cuántos pasos caben en 20 horas de sesión Colab.
    """
    from xgboost import XGBRegressor
    from joblib import Parallel, delayed

    print("\n" + "="*60)
    print("  🔬 BENCHMARK — Midiendo velocidad real en GPU")
    print("="*60)
    print(f"  Dimensiones: {n_samples:,} muestras × {n_features:,} features")
    print(f"  Dispositivo: {device.upper()}")
    print(f"  Entrenando 1 paso completo ({n_features} XGBoosts)...\n")

    xgb_kwargs = {
        'n_estimators': 100,
        'max_depth': 7,
        'learning_rate': 0.3,
        'tree_method': 'hist',
        'device': device,
        'n_jobs': 1
    }

    def train_single(X_input, y_single, kw):
        mdl = XGBRegressor(**kw)
        mdl.fit(X_input, y_single)
        return mdl

    alpha = 0.5
    noise = np.random.normal(0, 1, X_scaled.shape).astype(np.float32)
    X_t = (1 - alpha) * X_scaled + alpha * noise
    Y_t = noise - X_scaled

    t_start = time.time()
    Parallel(n_jobs=-1, verbose=0)(
        delayed(train_single)(X_t, Y_t[:, k], xgb_kwargs)
        for k in range(n_features)
    )
    duration_min = (time.time() - t_start) / 60

    SESSION_HOURS = 20
    session_minutes = SESSION_HOURS * 60
    max_steps_in_session = int(session_minutes / duration_min * 0.85)  # 15% margen de seguridad

    print(f"\n{'='*60}")
    print(f"  📊 RESULTADO DEL BENCHMARK")
    print(f"{'='*60}")
    print(f"  ⏱  Tiempo por paso:          {duration_min:.1f} minutos")
    print(f"  🕐 Sesión disponible:        {SESSION_HOURS} horas")
    print(f"  📈 Pasos en 20h (con 15% margen): {max_steps_in_session}")
    print(f"\n  ✅ RECOMENDACIÓN:")

    if max_steps_in_session >= 50:
        print(f"     n_t=50 ← puede completarse en UNA sesión ✨")
    elif max_steps_in_session >= 30:
        print(f"     n_t=50 en 2 sesiones, o n_t={max_steps_in_session} en una sola")
    else:
        print(f"     n_t=50 en múltiples sesiones (checkpoints lo manejan)")
        print(f"     O usar n_t={min(max_steps_in_session, 30)} para terminar en una sesión")

    print(f"{'='*60}\n")
    return duration_min, max_steps_in_session


# ─────────────────────────────────────────────────────────────────────────────
# ENSAMBLAJE FINAL
# ─────────────────────────────────────────────────────────────────────────────
def assemble_model(steps_dir, shell_path, final_model_path, n_t):
    """
    Ensambla el modelo final desde los archivos de pasos individuales.
    Funciona tanto en Colab como en local (con pasos descargados de Drive).
    """
    existing_steps = sorted([
        int(f.split('_')[1].split('.')[0])
        for f in os.listdir(steps_dir)
        if f.startswith('step_') and f.endswith('.joblib')
    ])

    print(f"\n🔍 Pasos encontrados: {len(existing_steps)}/{n_t}")

    if len(existing_steps) < n_t:
        missing = [t for t in range(n_t) if t not in existing_steps]
        print(f"❌ Faltan {len(missing)} pasos: {missing[:10]}{'...' if len(missing) > 10 else ''}")
        print(f"   Vuelve a ejecutar el script para entrenar los pasos faltantes.")
        return False

    print(f"✅ Todos los pasos presentes. Ensamblando modelo final...")
    print(f"   📦 Destino: {final_model_path}\n")

    model = joblib.load(shell_path)
    n_features = model.c

    # Estructura requerida: regr_[y_class][timestep][feature_k]
    model.regr_ = [[[None for _ in range(n_features)] for _ in range(n_t)] for _ in range(1)]

    t_start = time.time()
    for t in range(n_t):
        step_file = os.path.join(steps_dir, f"step_{t}.joblib")
        feature_models = joblib.load(step_file)
        for k in range(n_features):
            model.regr_[0][t][k] = feature_models[k]
        del feature_models
        gc.collect()
        elapsed = time.time() - t_start
        eta = (elapsed / (t + 1)) * (n_t - t - 1)
        print(f"   📥 [{t+1:>2}/{n_t}] cargado — ETA restante: {eta/60:.1f} min    ", end="\r")

    model.p_in_one = False

    print(f"\n\n💾 Guardando modelo maestro (compress=3, puede tardar varios minutos)...")
    joblib.dump(model, final_model_path, compress=3)

    elapsed_total = (time.time() - t_start) / 60
    size_gb = os.path.getsize(final_model_path) / 1e9
    print(f"\n🎉 ¡ENSAMBLAJE COMPLETADO en {elapsed_total:.1f} min!")
    print(f"📦 Tamaño final: {size_gb:.1f} GB")
    print(f"📂 Ruta: {final_model_path}")
    return True


# ─────────────────────────────────────────────────────────────────────────────
# ENTRENAMIENTO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Forest Diffusion — Colab GPU Training",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--drive_base', type=str, default=None,
                        help="Ruta base de Google Drive\n"
                             "Default: auto-detectado (/content/drive/MyDrive)")
    parser.add_argument('--data_subpath', type=str,
                        default='datasets/results/elite_borda_training_table.parquet',
                        help="Sub-ruta dentro de Drive al archivo parquet\n"
                             "Default: datasets/results/elite_borda_training_table.parquet")
    parser.add_argument('--checkpoint_subpath', type=str,
                        default='datasets/results/checkpoints',
                        help="Sub-ruta dentro de Drive para checkpoints\n"
                             "Default: datasets/results/checkpoints")
    parser.add_argument('--dataset', type=str, default='elite_borda',
                        help="Nombre del dataset (default: elite_borda)")
    parser.add_argument('--n_t', type=int, default=50,
                        help="Número de pasos de difusión (default: 50)")
    parser.add_argument('--max_steps', type=int, default=None,
                        help="Máximo de pasos en esta sesión\n"
                             "Si no se especifica, corre hasta completar n_t o agotar la sesión")
    parser.add_argument('--mode', type=str, default='both',
                        choices=['train', 'assemble', 'both'],
                        help="Modo: train | assemble | both (default: both)")
    parser.add_argument('--benchmark', action='store_true',
                        help="Correr benchmark de 1 paso antes de entrenar\n"
                             "Recomendado en la primera sesión para calibrar n_t")
    parser.add_argument('--device', type=str, default='auto',
                        choices=['auto', 'cpu', 'cuda'],
                        help="Dispositivo: auto (detecta GPU) | cpu | cuda")
    args = parser.parse_args()

    # ── Detectar dispositivo ─────────────────────────────────────────────────
    if args.device == 'auto':
        device = detect_device()
    else:
        device = args.device

    # ── Detectar Google Drive ────────────────────────────────────────────────
    drive_base = args.drive_base or get_drive_base()
    if drive_base is None:
        print("⚠️  Google Drive no detectado. Usando rutas locales.")
        drive_base = '.'

    input_path     = os.path.join(drive_base, args.data_subpath)
    checkpoint_dir = os.path.join(drive_base, args.checkpoint_subpath)
    steps_dir      = os.path.join(checkpoint_dir, f'steps_{args.dataset}')
    shell_path     = os.path.join(checkpoint_dir, f'fd_shell_{args.dataset}.joblib')
    final_model_path = os.path.join(checkpoint_dir, f'forest_diffusion_model_{args.dataset}.joblib')

    os.makedirs(steps_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Forest Diffusion — Colab GPU Training")
    print(f"{'='*60}")
    print(f"  Modo:       {args.mode.upper()}")
    print(f"  n_t:        {args.n_t} pasos")
    print(f"  Dispositivo:{device.upper()}")
    print(f"  Drive base: {drive_base}")
    print(f"  Input:      {input_path}")
    print(f"  Steps dir:  {steps_dir}")
    print(f"{'='*60}\n")

    # ── MODO: solo ensamblaje ────────────────────────────────────────────────
    if args.mode == 'assemble':
        assemble_model(steps_dir, shell_path, final_model_path, args.n_t)
        return

    # ── Cargar datos ─────────────────────────────────────────────────────────
    print(f"📂 Cargando dataset desde Drive...")
    if not os.path.exists(input_path):
        print(f"❌ Archivo no encontrado: {input_path}")
        print(f"   Verifica que master_training_table.parquet está en Drive.")
        sys.exit(1)

    df = pd.read_parquet(input_path)
    df_train = df.drop(columns=['GSE_ID']) if 'GSE_ID' in df.columns else df
    X_train = df_train.to_numpy().astype(np.float32)
    print(f"   ✅ {X_train.shape[0]:,} muestras × {X_train.shape[1]:,} features")

    # ── Inicializar o reanudar modelo ────────────────────────────────────────
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
        joblib.dump(model, shell_path, compress=3)
        print(f"   💾 Shell guardado en Drive: {shell_path}")

    X_scaled   = model.scaler.transform(X_train)
    n_features = X_scaled.shape[1]
    n_samples  = X_scaled.shape[0]

    # ── Benchmark opcional ───────────────────────────────────────────────────
    if args.benchmark:
        duration_min, max_steps = run_benchmark(X_scaled, device, n_features, n_samples)
        print(f"💡 Puedes continuar con --n_t {min(50, max_steps * 2)} si hay múltiples sesiones")
        print(f"   o con --n_t {max_steps} --max_steps {max_steps} para terminar en esta sesión.\n")
        resp = input("¿Continuar con el entrenamiento? (s/n): ").strip().lower()
        if resp != 's':
            print("Benchmark completado. Saliendo.")
            return

    # ── Configuración XGBoost ────────────────────────────────────────────────
    xgb_kwargs_single = {
        'n_estimators': 100,
        'max_depth': 7,
        'learning_rate': 0.3,
        'tree_method': 'hist',
        'device': device,
        'n_jobs': 1
    }

    from xgboost import XGBRegressor
    from joblib import Parallel, delayed

    def train_single_feature(X_input, y_single, kw):
        mdl = XGBRegressor(**kw)
        mdl.fit(X_input, y_single)
        return mdl

    session_start = time.time()
    steps_done = 0

    print(f"\n🧬 Iniciando entrenamiento ({n_features} XGBoosts/paso en paralelo)\n")

    for t in range(start_step, args.n_t):

        if args.max_steps is not None and steps_done >= args.max_steps:
            print(f"\n🛑 Límite de sesión alcanzado ({args.max_steps} pasos). Deteniendo.")
            break

        step_file = os.path.join(steps_dir, f"step_{t}.joblib")
        if os.path.exists(step_file):
            print(f"⏭️  [Paso {t+1:>2}/{args.n_t}] Ya existe en Drive, saltando...")
            continue

        step_start = time.time()
        print(f"⏳ [Paso {t+1:>2}/{args.n_t}] Entrenando {n_features} XGBoosts...", flush=True)

        # Matemática CFM
        alpha = (t + 1) / args.n_t
        noise = np.random.normal(0, 1, X_scaled.shape).astype(np.float32)
        X_t = (1 - alpha) * X_scaled + alpha * noise
        Y_t = noise - X_scaled

        feature_models = Parallel(n_jobs=-1, verbose=0)(
            delayed(train_single_feature)(X_t, Y_t[:, k], xgb_kwargs_single)
            for k in range(n_features)
        )

        # Guardar en Drive (compress=0 = instantáneo)
        joblib.dump(feature_models, step_file, compress=0)

        del noise, X_t, Y_t, feature_models
        gc.collect()

        duration_min = (time.time() - step_start) / 60
        size_mb = os.path.getsize(step_file) / 1e6
        steps_done += 1

        elapsed = time.time() - session_start
        avg = elapsed / steps_done
        remaining = args.n_t - t - 1
        eta_h = (avg * remaining) / 3600

        print(f"   ✅ {duration_min:.1f} min | {size_mb:.0f} MB en Drive | ETA restante: {eta_h:.1f}h")

    # ── Resumen ──────────────────────────────────────────────────────────────
    completed = sorted([
        int(f.split('_')[1].split('.')[0])
        for f in os.listdir(steps_dir)
        if f.startswith('step_') and f.endswith('.joblib')
    ])

    print(f"\n{'='*60}")
    print(f"📊 PROGRESO: {len(completed)}/{args.n_t} pasos completados en Drive")

    if len(completed) < args.n_t:
        missing = [t for t in range(args.n_t) if t not in completed]
        print(f"⏸️  Faltan {len(missing)} pasos")
        print(f"\n▶️  Para continuar en la próxima sesión de Colab, ejecuta el mismo comando.")
        print(f"   El script detectará los {len(completed)} pasos en Drive y reanudará.")
        return

    # ── Ensamblaje final ─────────────────────────────────────────────────────
    if args.mode == 'both':
        assemble_model(steps_dir, shell_path, final_model_path, args.n_t)
        print(f"\n💡 El modelo ensamblado está en tu Drive.")
        print(f"   Descarga solo ese archivo para generar sintéticos en local:")
        print(f"   {final_model_path}")
    else:
        print(f"\n✅ Todos los pasos completados.")
        print(f"   Para ensamblar: agrega --mode assemble al comando.")


if __name__ == "__main__":
    main()
