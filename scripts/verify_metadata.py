import os
import pandas as pd
import GEOparse
import time

def classify_sample(characteristics_list):
    text = " ".join(characteristics_list).lower()
    
    normal_strict = ['normal', 'healthy', 'control', 'non-tumor', 'non-malignant', 'adjacent', 'unaffected', 'benign', 'wt', 'wild type', 'wild-type']
    tumor_strict = ['tumor', 'tumour', 'cancer', 'carcinoma', 'adenocarcinoma', 'malignant', 'melanoma', 'sarcoma', 'leukemia', 'lymphoma', 'glioma', 'metastasis', 'metastatic', 'patient']
    
    is_normal = False
    is_tumor = False
    
    for kw in normal_strict:
        if kw in text:
            is_normal = True
            break
            
    for kw in tumor_strict:
        # Avoid matching 'non-tumor' as 'tumor'
        if kw in text and 'non-'+kw not in text and 'non '+kw not in text:
            is_tumor = True
            break

    # Resolve conflicts
    if is_normal and is_tumor:
        # e.g., "adjacent normal tissue from cancer patient"
        # We explicitly check for dominant normal phrasing
        dominant_normal = ['adjacent', 'non-tumor', 'non-malignant', 'normal', 'control', 'healthy', 'unaffected']
        if any(k in text for k in dominant_normal):
            return 'Normal'
        return 'Tumor'
        
    if is_normal:
        return 'Normal'
    if is_tumor:
        return 'Tumor'
        
    return 'Unknown'

def verify_datasets():
    if not os.path.exists("results/geo_candidates.csv"):
        print("No geo_candidates.csv found. Run find_geo_candidates.py first.")
        return
        
    df = pd.read_csv("results/geo_candidates.csv")
    os.makedirs("results/soft", exist_ok=True)
    GEOparse.logger.set_verbosity("ERROR")
    
    verified_data = []
    processed_gses = set()
    
    if os.path.exists("results/verified_samples.csv"):
        v_df = pd.read_csv("results/verified_samples.csv")
        verified_data = v_df.to_dict('records')
        processed_gses = set(v_df['GSE'].unique())
        print(f"Resuming... {len(processed_gses)} datasets already processed.")
    
    for _, row in df.iterrows():
        gse_id = row['GSE']
        if gse_id in processed_gses:
            continue
            
        if gse_id == 'GSE151101':
            print("Skipping GSE151101 due to known FTP freeze issue...")
            # We add it so we don't spam skip messages if we run again
            processed_gses.add(gse_id)
            continue
            
        tech = row.get('Technology', 'Unknown')
        print(f"Processing {gse_id}...")
        try:
            # silent=True prevents downloading logs
            gse = GEOparse.get_GEO(geo=gse_id, destdir="results/soft", silent=True)
            
            normal_count = 0
            tumor_count = 0
            sample_records = []
            
            for gsm_name, gsm in gse.gsms.items():
                chars = gsm.metadata.get('characteristics_ch1', [])
                source_name = gsm.metadata.get('source_name_ch1', [])
                title = gsm.metadata.get('title', [])
                
                # Combine all descriptive hints specifically for older Microarrays
                combined = chars + source_name + title
                
                category = classify_sample(combined)
                sample_records.append({
                    'GSE': gse_id,
                    'GSM': gsm_name,
                    'Category': category,
                    'Characteristics': " | ".join(combined),
                    'Technology': tech
                })
                
                if category == 'Normal':
                    normal_count += 1
                elif category == 'Tumor':
                    tumor_count += 1
                    
            # Check if this dataset actually compares Normal vs Tumor
            if normal_count >= 1 and tumor_count >= 1:
                print(f"  -> Verified: {normal_count} Normal, {tumor_count} Tumor")
                verified_data.extend(sample_records)
            else:
                print(f"  -> Rejected: Lacks both classes ({normal_count} Normal, {tumor_count} Tumor)")
                
                
        except Exception as e:
            print(f"  -> Error fetching {gse_id}: {e}")
            
        # Intermediate snapshot check
        v_df = pd.DataFrame(verified_data)
        if not v_df.empty:
            v_df.to_csv("results/verified_samples.csv", index=False)
            
    print("Done scanning candidates.")
    v_df = pd.DataFrame(verified_data)
    if not v_df.empty:
        print("Saved detailed sample metadata to results/verified_samples.csv")
    else:
        print("No datasets were successfully verified with both classes.")
        
if __name__ == "__main__":
    verify_datasets()
