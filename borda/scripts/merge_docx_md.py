import os
import re

def main():
    base_dir = "/Users/gary.velasquez/Documents/Repos/latamxp/datasets/REPORTS/documentos_tesis"
    
    # Paths
    master_path = os.path.join(base_dir, "20164065_GaryVelasquez_EdwinVillanueva_2026.md")
    cap1_path = os.path.join(base_dir, "CAPITULO_1_INTRODUCCION.md")
    cap4_path = os.path.join(base_dir, "CAPITULO_4_RESULTADOS.md")
    cap5_path = os.path.join(base_dir, "CAPITULO_5_RESULTADOS_ESPERADOS.md")
    cap6_path = os.path.join(base_dir, "CAPITULO_6_CONCLUSIONES_Y_TRABAJOS_FUTUROS.md")
    out_path = os.path.join(base_dir, "20164065_GaryVelasquez_EdwinVillanueva_2026_ACTUALIZADO.md")
    
    # Read files
    with open(master_path, "r", encoding="utf-8") as f:
        master_lines = f.readlines()
        
    with open(cap1_path, "r", encoding="utf-8") as f:
        cap1_content = f.read()
        
    with open(cap4_path, "r", encoding="utf-8") as f:
        cap4_content = f.read()
        
    with open(cap5_path, "r", encoding="utf-8") as f:
        cap5_content = f.read()
        
    with open(cap6_path, "r", encoding="utf-8") as f:
        cap6_content = f.read()
        
    # Find indices dynamically
    idx_generalidades = None
    idx_marco = None
    idx_desarrollo = None
    idx_presentacion = None
    idx_conclusiones = None
    idx_references = None
    
    for idx, line in enumerate(master_lines):
        clean_line = line.strip()
        if re.match(r"^#\s*Generalidades\s*$", clean_line, re.IGNORECASE):
            idx_generalidades = idx
        elif re.match(r"^#\s*Marco Conceptual\s*$", clean_line, re.IGNORECASE):
            idx_marco = idx
        elif re.match(r"^#\s*Desarrollo y Resultados\s*$", clean_line, re.IGNORECASE):
            idx_desarrollo = idx
        elif re.match(r"^#\s*Presentación de los resultados esperados\s*$", clean_line, re.IGNORECASE):
            idx_presentacion = idx
        elif re.match(r"^#\s*Conclusiones y trabajos futuros\s*$", clean_line, re.IGNORECASE):
            idx_conclusiones = idx
        elif re.match(r"^#\s*\{\s*#section\s*\.Title\s*\}\s*$", clean_line):
            idx_references = idx

    # Validation
    print("Dynamically found indices:")
    print(f"Generalidades: line {idx_generalidades + 1 if idx_generalidades is not None else 'NOT FOUND'}")
    print(f"Marco Conceptual: line {idx_marco + 1 if idx_marco is not None else 'NOT FOUND'}")
    print(f"Desarrollo y Resultados: line {idx_desarrollo + 1 if idx_desarrollo is not None else 'NOT FOUND'}")
    print(f"Presentacion: line {idx_presentacion + 1 if idx_presentacion is not None else 'NOT FOUND'}")
    print(f"Conclusiones: line {idx_conclusiones + 1 if idx_conclusiones is not None else 'NOT FOUND'}")
    print(f"References: line {idx_references + 1 if idx_references is not None else 'NOT FOUND'}")
    
    if any(x is None for x in [idx_generalidades, idx_marco, idx_desarrollo, idx_presentacion, idx_conclusiones, idx_references]):
        raise ValueError("One or more chapter headers were not found in the master document. Check regular expressions.")
    
    # Adjust relative paths in master_lines
    for idx in range(len(master_lines)):
        master_lines[idx] = master_lines[idx].replace("REPORTS/documentos_tesis/media/", "media/")
    
    cap1_content = cap1_content.replace("REPORTS/documentos_tesis/media/", "media/")
    cap4_content = cap4_content.replace("REPORTS/documentos_tesis/media/", "media/")
    cap5_content = cap5_content.replace("REPORTS/documentos_tesis/media/", "media/")
    cap6_content = cap6_content.replace("REPORTS/documentos_tesis/media/", "media/")
    
    # Construct updated content
    # Part 0: From beginning to the line before Generalidades
    part0 = "".join(master_lines[:idx_generalidades])
    
    # Part 1: Chapter 1 content
    part1 = cap1_content + "\n\n"
    
    # Part 2: Chapter 2 and 3 (from Marco Conceptual to the line before Desarrollo y Resultados)
    part2 = "".join(master_lines[idx_marco:idx_desarrollo])
    
    # Part 3: Chapter 4 content
    part3 = cap4_content + "\n\n"
    
    # Part 5: Chapter 5 content
    part5 = cap5_content + "\n\n"
    
    # Part 6: Chapter 6 content
    part6 = cap6_content + "\n\n"
    
    # Part 7: From References to end
    part7 = "".join(master_lines[idx_references:])
    
    # Assemble
    final_content = part0 + part1 + part2 + part3 + part5 + part6 + part7
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print("Successfully wrote updated markdown to", out_path)

if __name__ == "__main__":
    main()
