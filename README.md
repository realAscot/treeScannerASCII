# TreeScanner

Ein flexibler Verzeichnisscanner für die Kommandozeile **und** zur Einbindung als Python-Modul.

## Projektstruktur

```plaintext

treescanner/
├── __init__.py
├── __main__.py        # Standalone-Ausführung
├── scanner.py         # Das eigentliche Modul mit Klasse + Logik
├── config.py          # Konfigurationsklasse separat
└── test_usage.py      # Beispielverwendung als Modul
```

## 🔧 Verwendung als Standalone

```bash
python treescanner.py
```

Erzeugt eine Datei `tree.txt` mit der Verzeichnisstruktur ab dem aktuellen Pfad.

## 🧩 Verwendung als Modul

```python
from treescanner import TreeScanner, TreeScannerConfig

config = TreeScannerConfig(root_path=".", max_depth=2)
scanner = TreeScanner(config)
output = scanner.generate_tree()
print(output)
```

## ⚙️ Konfiguration

Die `TreeScannerConfig`-Klasse erlaubt dir u. a.:

- `root_path`: Startverzeichnis
- `max_depth`: maximale Rekursionstiefe
- `max_files_per_dir`: wie viele Dateien pro Ordner angezeigt werden
- `align_comments`: Kommentar-Ausrichtung aktivieren
- `folder_icon` / `file_icon`: Anzeige-Icons

## 📄 Lizenz

MIT (optional anpassen)  
