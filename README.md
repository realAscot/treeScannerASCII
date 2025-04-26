# README for TreeScanner

Ein flexibler Verzeichnisscanner für die Kommandozeile und zur Einbindung als Python-Modul.

## Projektstruktur

```plaintext
📁 treescannerASCII/      # Projekt-Root
├── 📁 media              # Bilder/Icons für GitHub, Ausgabe etc.
├── 📄 .gitignore         # Ignorierte Dateien
├── 📄 CHANGELOG.md       # Änderungsprotokoll (Markdown)
├── 📄 LICENSE            # Lizenzdatei (MIT)
├── 📄 README.md          # Diese Anleitung
├── 📄 TODO.md            # Offene Aufgaben
├── 📄 __init__.py        # Modul-Initialisierung
├── 📄 __main__.py        # Einstiegspunkt für `python -m treescanner`
├── 📄 scanner.py         # Hauptimplementierung
└── 📄 test_usage.py      # Beispiel für Modul-Integration
```

## 🔧 Standalone-Ausführung (CLI)

```bash
python scanner.py [root_path] [-n N] [-d DEPTH] [--no-align-comments] [-h]
```

| Parameter               | Beschreibung                                                                                                   |
|-------------------------|---------------------------------------------------------------------------------------------------------------|
| `root_path`             | Optionales Verzeichnis, ab dem gescannt wird (Default: aktueller Pfad).                                      |
| `-n`, `--max-files-per-dir` | Begrenze die Anzahl an Dateien pro Verzeichnis (Default: 2).                                               |
| `-d`, `--max-depth`     | Maximale Tiefe der Rekursion; unbegrenzt, wenn nicht gesetzt.                                                  |
| `--no-align-comments`   | Deaktiviert die Ausrichtung der Kommentar-Platzhalter am Zeilenende.                                         |
| `-h`, `--help`          | Zeigt diese Hilfe an und beendet das Programm.                                                               |

Die Ausgabe wird in die Datei `tree.txt` geschrieben.

## 🧩 Verwendung als Modul

```python
from treescanner import TreeScanner, TreeScannerConfig

# Konfiguration mit Pfad, Auswahl der Maximaltiefe und Ausrichtung
config = TreeScannerConfig(
    root_path="./",          # zu scannender Pfad
    max_depth=3,              # maximale Rekursionstiefe
    max_files_per_dir=5,      # bis zu 5 Dateien pro Ordner anzeigen
    align_comments=True       # Kommentare ausrichten
)
scanner = TreeScanner(config)
output = scanner.generate_tree()
print(output)
```

> Hinweis: Alle Klassen und Methoden sind mit **Google-Style Docstrings** versehen. Moderne IDEs (VS Code, PyCharm) zeigen so direkt Parameter und Rückgabetypen als Tooltip an.

## ⚙️ Konfiguration via `TreeScannerConfig`

| Attribut              | Typ               | Beschreibung                                                           |
|-----------------------|-------------------|-------------------------------------------------------------------------|
| `root_path: str`      | Pfad             | Basisverzeichnis zum Scannen (Default: `.`)                              |
| `folder_icon: str`    | Unicode-Zeichen   | Symbol für Verzeichnisse (Default: 📁)                                    |
| `file_icon: str`      | Unicode-Zeichen   | Symbol für Dateien und Platzhalter (Default: 📄)                          |
| `max_files_per_dir: int` | Ganzzahl       | Maximale angezeigte Dateien pro Verzeichnis (Default: 2)                 |
| `max_depth: Optional[int]` | Ganzzahl/None | Maximale Rekursionstiefe, `None` = unlimitiert                           |
| `align_comments: bool` | Wahr/Falsch     | Kommentare am Zeilenende ausrichten (Default: `True`)                   |

## 📄 Beispielausgabe

```plaintext
📁 treescannerASCII/
├── 📁 media
│   ├── 📄 favicon.ico
│   ├── 📄 logo-bw-1024x1024.png
│   └── 📄 <und 3 weitere Dateien>
├── 📄 .gitignore
├── 📄 CHANGELOG.md
├── 📄 README.md
└── 📄 <und 12 weitere Dateien>
```

## 📄 Lizenz

MIT – siehe [LICENSE](./LICENSE)
