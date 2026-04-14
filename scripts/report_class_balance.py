import pandas as pd
import os

def generate_report():
    if not os.path.exists("results/verified_samples.csv"):
        print("No verified_samples.csv found. Run verify_metadata.py first.")
        return
        
    df = pd.read_csv("results/verified_samples.csv")
    
    # Group by GSE and category to calculate counts
    report_data = []
    
    for gse_id, group in df.groupby("GSE"):
        total = len(group)
        tech = group['Technology'].iloc[0] if 'Technology' in group.columns else 'Unknown'
        counts = group['Category'].value_counts()
        normal = counts.get('Normal', 0)
        tumor = counts.get('Tumor', 0)
        unknown = counts.get('Unknown', 0)
        
        report_data.append({
            'GSE_ID': gse_id,
            'Technology': tech,
            'Total_Samples': total,
            'Normal_Count': normal,
            'Tumor_Count': tumor,
            'Unknown_Count': unknown,
            'Tumor_to_Normal_Ratio': round(tumor/normal, 2) if normal > 0 else float('inf')
        })
        
    report_df = pd.DataFrame(report_data)
    report_df = report_df.sort_values(by="Total_Samples", ascending=False)
    
    report_df.to_csv("results/class_balance_report.csv", index=False)
    
    # Also generate a markdown report
    markdown_report = "# Class Balance Report for New Datasets\n\n"
    markdown_report += "| GSE ID | Technology | Total Samples | Normal | Tumor | Ratio (Tumor:Normal) |\n"
    markdown_report += "|--------|------------|---------------|--------|-------|----------------------|\n"
    
    for _, row in report_df.iterrows():
        markdown_report += f"| {row['GSE_ID']} | {row['Technology']} | {row['Total_Samples']} | {row['Normal_Count']} | {row['Tumor_Count']} | {row['Tumor_to_Normal_Ratio']} |\n"
        
    with open("results/class_balance_report.md", "w") as f:
        f.write(markdown_report)
        
    print("Class balance report generated at results/class_balance_report.csv and .md!")
    
    if 'Technology' in report_df.columns:
        rna_c = len(report_df[report_df['Technology'] == 'RNA-seq'])
        arr_c = len(report_df[report_df['Technology'] == 'Microarray'])
        print(f"Total datasets passing the filter: {len(report_df)} (RNA-seq: {rna_c}, Microarray: {arr_c})")
    else:
        print(f"Total datasets passing the filter: {len(report_df)}")
        
    if len(report_df) > 0:
        print(f"Total novel normal samples: {report_df['Normal_Count'].sum()}")
        print(f"Total novel tumor samples: {report_df['Tumor_Count'].sum()}")

if __name__ == "__main__":
    generate_report()
