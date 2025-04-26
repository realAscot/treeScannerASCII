#!/usr/bin/env python3
"""
TreeScanner: Verzeichnisbaum-Ausgabe mit ASCII-Art.

Standalone-Ausführung unterstützt folgende CLI-Parameter:
    root_path                Pfad des Stammverzeichnisses (Default: aktuelles Verzeichnis).
    -n, --max-files-per-dir   Maximale Anzahl Dateien pro Verzeichnis (Default: 2).
    -d, --max-depth           Maximale Rekursionstiefe (Default: unbegrenzt).
    --no-align-comments       Deaktiviert das Ausrichten der Kommentare.
    -h, --help                Diese Hilfe anzeigen und Programm beenden.
"""

import os
import argparse
from typing import Optional, List

class TreeScannerConfig:
    """
    Konfigurationsklasse für den TreeScanner.

    Attributes:
        root_path (str): Pfad des Stammverzeichnisses.
        folder_icon (str): Icon für Ordner.
        file_icon (str): Icon für Dateien und Platzhalter.
        max_files_per_dir (int): Maximale Anzahl Dateien, die pro Verzeichnis angezeigt werden.
        max_depth (Optional[int]): Maximale Tiefe der Rekursion (None = unbeschränkt).
        align_comments (bool): Ob Kommentare am Zeilenende ausgerichtet werden sollen.
    """

    def __init__(
        self,
        root_path: str = ".",
        folder_icon: str = "\U0001F4C1",
        file_icon: str = "\U0001F4C4",
        max_files_per_dir: int = 2,
        max_depth: Optional[int] = None,
        align_comments: bool = True,
    ):
        """
        Args:
            root_path (str): Pfad des Stammverzeichnisses.
            folder_icon (str): Icon für Ordner.
            file_icon (str): Icon für Dateien und Platzhalter.
            max_files_per_dir (int): Maximale Anzahl Dateien pro Verzeichnis.
            max_depth (Optional[int]): Maximale Rekursionstiefe, None = unlimitiert.
            align_comments (bool): Kommentare ausrichten, wenn True.
        """
        self.root_path = root_path
        self.folder_icon = folder_icon
        self.file_icon = file_icon
        self.max_files_per_dir = max_files_per_dir
        self.max_depth = max_depth
        self.align_comments = align_comments

class TreeScanner:
    """
    Klasse zum Scannen von Verzeichnissen und Erzeugen einer ASCII-Baumstruktur.
    """

    def __init__(self, config: TreeScannerConfig):
        """
        Args:
            config (TreeScannerConfig): Konfiguration für den Scanner.
        """
        self.config = config

    def scan_directory(self, path: str, depth: int = 0, prefix: str = "") -> List[str]:
        """
        Scannt ein Verzeichnis und gibt eine Liste von ASCII-Zeilen zurück.

        Args:
            path (str): Pfad des zu scannenden Verzeichnisses.
            depth (int): Aktuelle Rekursionstiefe.
            prefix (str): Präfix für Einrückung und Connectoren.

        Returns:
            List[str]: Zeilen mit ASCII-Baumstruktur für dieses Verzeichnis.
        """
        lines: List[str] = []
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            # Zugriff verweigert: Spezielle Rückgabe, kein Rekursionsaufruf
            return [f"{prefix}└── [Zugriff verweigert] {path}"]

        # Aufteilen in Ordner und Dateien
        folders = [e for e in entries if os.path.isdir(os.path.join(path, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(path, e))]

        # 1) Verzeichnisse verarbeiten
        for idx, folder in enumerate(folders):
            folder_path = os.path.join(path, folder)
            # ├──, wenn nicht letzter Ordner oder noch Dateien folgen, sonst └──
            connector = "├── " if idx < len(folders) - 1 or files else "└── "
            lines.append(f"{prefix}{connector}{self.config.folder_icon} {folder}")
            # Rekursive Ausgabe, falls max_depth nicht überschritten
            if self.config.max_depth is None or depth < self.config.max_depth:
                # Verlängerung des Präfixes: '│   ' oder Leerraum
                extension = "│   " if idx < len(folders) - 1 or files else "    "
                lines.extend(self.scan_directory(folder_path, depth + 1, prefix + extension))

        # 2) Dateien plus Platzhalter als kombinierte Liste behandeln
        visible_files = files[: self.config.max_files_per_dir]
        remaining = len(files) - len(visible_files)

        # Kombinieren: echte Dateien + Platzhalter
        combined = visible_files.copy()
        if remaining > 0:
            combined.append(f"<und {remaining} weitere Dateien>")

        # Ausgabe mit Datei-Icon für echte Dateien UND Platzhalter
        for idx, name in enumerate(combined):
            # ├── für alle außer dem letzten Eintrag, sonst └──
            connector = "├── " if idx < len(combined) - 1 else "└── "
            # Icon hinzufügen (auch beim Platzhalter)
            lines.append(f"{prefix}{connector}{self.config.file_icon} {name}")

        return lines

    def align_lines_with_comments(self, lines: List[str]) -> List[str]:
        """
        Richtet alle Zeilen so aus, dass Kommentare am gleichen Spaltenindex stehen.

        Args:
            lines (List[str]): Liste der Baumstruktur-Zeilen ohne Kommentare.

        Returns:
            List[str]: Zeilen mit ausgerichteten Kommentar-Platzhaltern (#).
        """
        # Bestimme Länge der längsten Zeile (ohne Trailing Spaces)
        max_length = max(len(line.rstrip()) for line in lines)
        aligned: List[str] = []
        for line in lines:
            text = line.rstrip()
            # Padding-Breite: definierte Spaltenausrichtung (+2 Leerzeichen)
            padding = " " * (max_length - len(text) + 2)
            aligned.append(text + padding + "#  ")
        return aligned

    def generate_tree(self) -> str:
        """
        Generiert den vollständigen Verzeichnisbaum als String.

        Returns:
            str: Mehrzeiliger String mit Ordner-Icon, Ordner- und Dateienstruktur.
        """
        # Stammverzeichnisname ermitteln
        root_name = os.path.basename(os.path.abspath(self.config.root_path)) or self.config.root_path
        lines = [f"{self.config.folder_icon} {root_name}/"]
        # Baumstruktur dahinter generieren
        lines += self.scan_directory(self.config.root_path)
        # Optional Kommentare ausrichten
        if self.config.align_comments:
            lines = self.align_lines_with_comments(lines)
        return "\n".join(lines)

def main():
    """
    Standalone-Ausführung mit CLI-Parameter-Unterstützung.
    Parse CLI-Argumente und generiere tree.txt.
    """
    # CLI-Parser konfigurieren
    parser = argparse.ArgumentParser(
        description="Generiert eine ASCII-Baumstruktur eines Verzeichnisses."
    )
    # Positionsargument: root_path (optional)
    parser.add_argument(
        "root_path",
        nargs="?",
        default=".",
        help="Pfad des Stammverzeichnisses (default: aktuelles Verzeichnis)."
    )
    # Optionale Flags und Parameter
    parser.add_argument(
        "-n", "--max-files-per-dir",
        type=int,
        default=2,
        help="Maximale Anzahl Dateien pro Verzeichnis (default: 2)."
    )
    parser.add_argument(
        "-d", "--max-depth",
        type=int,
        help="Maximale Rekursionstiefe; unbegrenzt, wenn nicht gesetzt."
    )
    parser.add_argument(
        "--no-align-comments",
        action="store_false",
        dest="align_comments",
        help="Deaktiviert das Ausrichten der Kommentare am Zeilenende."
    )

    # CLI-Argumente einlesen
    args = parser.parse_args()

    # Konfiguration auf Basis der CLI-Argumente erstellen
    config = TreeScannerConfig(
        root_path=args.root_path,
        max_files_per_dir=args.max_files_per_dir,
        max_depth=args.max_depth,
        align_comments=args.align_comments
    )
    scanner = TreeScanner(config)
    tree_output = scanner.generate_tree()

    # Ausgabe in tree.txt schreiben
    with open("tree.txt", "w", encoding="utf-8") as f:
        f.write(tree_output + "\n")

if __name__ == "__main__":
    main()
