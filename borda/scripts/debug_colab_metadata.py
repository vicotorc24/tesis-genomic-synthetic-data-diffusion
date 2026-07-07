import os
import time
import hashlib
import pandas as pd

def get_md5(path):
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

path = 'results/synthetic_samples_elite_borda_5000.parquet'
if os.path.exists("datasets/" + path):
    path = "datasets/" + path

if os.path.exists(path):
    stat = os.stat(path)
    print(f"File: {path}")
    print(f"  Size: {stat.st_size} bytes")
    print(f"  Modified: {time.ctime(stat.st_mtime)}")
    print(f"  MD5 Hash: {get_md5(path)}")
    df = pd.read_parquet(path)
    print(f"  Shape: {df.shape}")
    target_col = 'Category' if 'Category' in df.columns else 'target'
    print(f"  Target counts:\n{df[target_col].value_counts()}")
    print(f"  SDHA first 5 values:\n{df['SDHA'].head(5).values}")
else:
    print(f"❌ File not found at {path}")
