# __main__.py
# (leer) Optional: erlaubt spätere Ausführung mit `python -m treescannerASCII`

try:
    # Für Paket-Ausführung mit `python -m treeScannerASCII`
    from .scanner import main
except ImportError:
    # Für direkte Ausführung mit `python scanner.py`
    from scanner import main

if __name__ == "__main__":
    main()
