# README for TreeScanner

![LOGO](./media/logo-colour-alpha-512x512.png)

Ein flexibler Verzeichnisscanner für die Kommandozeile und zur Einbindung als Python-Modul.

## 📁 Projektstruktur

```plaintext
📁 treescannerASCII/      # Projekt-Root
├── 📁 media              # Bilder/Icons für GitHub, Ausgabe etc.
├── 📄 .gitignore         # Ignorierte Dateien
├── 📄 CHANGELOG.md       # Änderungsprotokoll (Markdown)
├── 📄 LICENSE.md         # Lizenzdatei (MIT)
├── 📄 README.md          # Diese Anleitung
├── 📄 TODO.md            # Offene Aufgaben
├── 📄 scanner.py         # Hauptimplementierung (Standalone und Modul)
├── 📄 __init__.py        # Modul-Initialisierung (optional, vorbereitet)
├── 📄 __main__.py        # Einstiegspunkt für `python -m treescanner` (optional, vorbereitet)
└── 📄 test_usage.py      # Beispiel für Modul-Integration
```

## 🔧 Standalone-Ausführung (CLI)

```bash
python scanner.py [root_path] [-n N] [-d DEPTH] [--no-align-comments] [-l {de,en}] [-h]
```

| Parameter                  | Beschreibung                                                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| `root_path`                 | Optionales Verzeichnis, ab dem gescannt wird (Default: aktueller Pfad).                                       |
| `-n`, `--max-files-per-dir` | Begrenze die Anzahl an Dateien pro Verzeichnis (Default: 2).                                                 |
| `-d`, `--max-depth`         | Maximale Tiefe der Rekursion; unbegrenzt, wenn nicht gesetzt.                                                 |
| `--no-align-comments`       | Deaktiviert die Ausrichtung der Kommentar-Platzhalter am Zeilenende.                                          |
| `-l`, `--language`          | Sprache der Abschlussmeldung (`de` für Deutsch, `en` für Englisch; Default: `de`).                           |
| `-h`, `--help`              | Zeigt diese Hilfe an und beendet das Programm.                                                               |

**Ausgabe:**

- Baumstruktur wird in die Datei `tree.txt` geschrieben.  
- Nach Abschluss erfolgt eine Zusammenfassung (Anzahl Verzeichnisse/Dateien, Name der Ausgabedatei).

## 🧩 Verwendung als Modul

```python
from scanner import TreeScanner, TreeScannerConfig

config = TreeScannerConfig(
    root_path="./",         # zu scannender Pfad
    max_depth=3,             # maximale Rekursionstiefe
    max_files_per_dir=5,     # bis zu 5 Dateien pro Ordner anzeigen
    align_comments=True,    # Kommentare ausrichten
    language="de"            # Sprache der Ausgabe
)
scanner = TreeScanner(config)
output = scanner.generate_tree()
print(output)
```

> Hinweis: Alle Klassen und Methoden sind mit **Google-Style Docstrings** versehen. Moderne IDEs (VS Code, PyCharm) zeigen so direkt Parameter und Rückgabetypen als Tooltip an.

## ⚙️ Konfiguration via `TreeScannerConfig`

| Attribut                   | Typ                | Beschreibung                                                        |
|-----------------------------|--------------------|---------------------------------------------------------------------|
| `root_path: str`            | String             | Basisverzeichnis zum Scannen (Default: `.`)                        |
| `folder_icon: str`          | Unicode-Zeichen    | Symbol für Verzeichnisse (Default: 📁)                               |
| `file_icon: str`            | Unicode-Zeichen    | Symbol für Dateien und Platzhalter (Default: 📄)                     |
| `max_files_per_dir: int`    | Ganzzahl           | Maximale angezeigte Dateien pro Verzeichnis (Default: 2)            |
| `max_depth: Optional[int]`  | Ganzzahl oder None | Maximale Rekursionstiefe; `None` = unbegrenzt                       |
| `align_comments: bool`      | Bool               | Kommentare am Zeilenende ausrichten (Default: `True`)               |
| `language: str`             | String             | Sprache der Zusammenfassung (`de` oder `en`) (Default: `de`)        |

## 📄 Beispielausgabe (tree.txt)

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

## 📋 Aktuelle Funktionen

- Ausgabe einer ASCII-Verzeichnisstruktur
- Begrenzung der Dateiausgabe pro Verzeichnis
- Begrenzung der Rekursionstiefe
- Optionale Ausrichtung der Kommentarzeile am Ende
- Mehrsprachige Abschlussmeldung (Deutsch, Englisch)
- Ausgabe als Textdatei (`tree.txt`)
- Saubere Google-Style Docstrings für IDE-Kompatibilität
- Modularer Aufbau für spätere Erweiterungen

## 🛡️ Geplante Erweiterungen

- Bessere Fehlerbehandlung bei ungültigem Pfad (anstatt Absturz)
- Farbliche Ausgabe der Baumstruktur in der Konsole (optional)
- Konfigurierbare Ausgabe-Datei über CLI
- Vorbereitung für Unicode-optimierte Konsolen

## 📄 Lizenz

MIT – siehe [LICENSE.md](./LICENSE.md)
