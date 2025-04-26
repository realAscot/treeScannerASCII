# CHANGELOG

- 2025-04-25 - initial commit

  - **Geändert:**  
    - [x] `treescanner.py` umgebaut zu kombinierter Modul- und Standalone-Version  
    - [x] Konfigurationsklasse `TreeScannerConfig` eingebaut  
    - [x] Klasse `TreeScanner` erstellt und bestehende Logik dorthin verschoben  

  - **Hinzugefügt:**  
    - [x] `test_usage.py` als __Beispiel__ für modulare Verwendung  
    - [x] `README.md` erstellt mit Anleitung für Standalone- und Modulnutzung (Template)  
    - [x] `pyproject.toml` erstellt für spätere Paketinstallation mit PEP 621  
    - [ ] `TODO.md` ist eingefügt aber wird vorerst noch nicht versioniert.

  - **Geprüft:**  
    - [x] `scanner.py` solo in ein Verzeichnis kopieren und ausführen mit `python scanner.py`  
    - [x] Import und Nutzung als Modul aus `test_usage.py`  
