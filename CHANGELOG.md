# CHANGELOG

- **2025-04-27 - Commit v0.2.0**

  - **Hinzugefügt:**  
    - [x] Ausgabe der Anzahl gescannter Verzeichnisse und Dateien nach Abschluss
    - [x] Mehrsprachigkeit für Abschlussmeldung vorbereitet (Deutsch/Englisch)

---

- **2025-04-26 – Commit v0.1.0**

  - **Geändert:**  
    - [x] `scan_directory()`: Platzhalter `<und …>` wird jetzt mit Datei-Icon und korrektem Connector (`├──`/`└──`) ausgegeben.  
    - [x] `main()`: CLI-Parameterunterstützung via `argparse` implementiert (`-h/--help`, `-n/--max-files-per-dir`, `-d/--max-depth`, `--no-align-comments`).  
    - [x] [README.md](./README.md) überarbeitet  

  - **Hinzugefügt:**  
    - [x] Vollständige Google-Style Docstrings für alle Klassen, Methoden und Funktionen.  
    - [x] Umfangreiche Inline-Kommentare zur Erläuterung von Logik und Parametern.  

  - **Geprüft:**  
    - [x] Ausgabe von `<und …>` mit Icon und Connector validiert.  
    - [x] CLI-Parameterhandling und Hilfe (`-h`) getestet.  
    - [x] Google-Style Docstrings in VS Code-Tooltips überprüft.

---

- **2025-04-25 - initial commit**

  - **Geändert:**  
    - [x] `scanner.py` umgebaut zu kombinierter Modul- und Standalone-Version  
    - [x] Konfigurationsklasse `TreeScannerConfig` eingebaut  
    - [x] Klasse `TreeScanner` erstellt und bestehende Logik dorthin verschoben  

  - **Hinzugefügt:**  
    - [x] `test_usage.py` als **Beispiel** für modulare Verwendung  
    - [x] `README.md` erstellt mit Anleitung für Standalone- und Modulnutzung (Template)  
    - [x] `pyproject.toml` erstellt für spätere Paketinstallation mit PEP 621  
    - [X] `TODO.md` ist eingefügt aber wird vorerst noch nicht versioniert.
    - [x] `LICENSE.md` eingefügt und vorerst MIT Lizensiert.

  - **Geprüft:**  
    - [x] `scanner.py` solo in ein Verzeichnis kopieren und ausführen mit `python scanner.py`  
    - [x] Import und Nutzung als Modul aus `test_usage.py`  

---
