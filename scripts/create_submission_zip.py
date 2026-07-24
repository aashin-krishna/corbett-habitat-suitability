import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
ZIP_PATH = BASE_DIR / "AashinKrishnaAS_P6.zip"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "Output"

def create_zip():
    print(f"Creating Submission ZIP archive at: {ZIP_PATH}...")
    
    files_to_pack = [
        # (source_path, arcname_inside_zip)
        (BASE_DIR / "AashinKrishnaAS_P6.pdf", "AashinKrishnaAS_P6.pdf"),
        (BASE_DIR / "REPORT.docx", "Project_Report/REPORT.docx"),
        (BASE_DIR / "REPORT.md", "Project_Report/REPORT.md"),
        (BASE_DIR / "REPORT.html", "Project_Report/REPORT.html"),
        (OUTPUT_DIR / "Corbett_Habitat_Suitability_Map.png", "Output_Maps_and_Figures/Corbett_Habitat_Suitability_Map.png"),
        (OUTPUT_DIR / "Habitat_Suitability_Statistics_Chart.png", "Output_Maps_and_Figures/Habitat_Suitability_Statistics_Chart.png"),
        (OUTPUT_DIR / "Habitat_Suitability_Statistics.csv", "Results_and_Statistics/Habitat_Suitability_Statistics.csv"),
        (OUTPUT_DIR / "Habitat_Suitability_Class.tif", "Results_and_Statistics/Habitat_Suitability_Class.tif"),
        (OUTPUT_DIR / "Habitat_Suitability_Index.tif", "Results_and_Statistics/Habitat_Suitability_Index.tif"),
    ]
    
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for src, arc in files_to_pack:
            if src.exists():
                print(f"Adding: {src.name} -> {arc}")
                zipf.write(src, arc)
            else:
                print(f"Warning: File not found: {src}")
                
    print(f"Submission ZIP successfully created! Size: {ZIP_PATH.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    create_zip()
