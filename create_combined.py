import os

# Ordnerpfad mit den .qmd Dateien
input_folder = "erste-schritte"
# Ausgabe-Dateipfad
output_file = os.path.join(input_folder, "combined_output.txt")

# Funktion, um alle .qmd-Dateien im Ordner zu verarbeiten
def combine_qmd_files(input_folder, output_file):
    with open(output_file, "w", encoding="utf-8") as outfile:
        # Name des Kapitels (Ordnername) einfügen
        outfile.write(f"# Kapitel: {os.path.basename(input_folder)}\n\n")
        
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.endswith(".qmd"):
                    file_path = os.path.join(root, file)
                    
                    # Name und Pfad der Datei als Kommentar schreiben
                    outfile.write(f"# Datei: {file}\n")
                    outfile.write(f"# Pfad: {file_path}\n\n")

                    # Inhalt der Datei lesen und schreiben
                    with open(file_path, "r", encoding="utf-8") as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write("\n\n")  # Leerzeile zwischen Dateien

    print(f"Inhalte der .qmd-Dateien wurden erfolgreich in {output_file} zusammengeführt.")

# Funktion aufrufen
combine_qmd_files(input_folder, output_file)
