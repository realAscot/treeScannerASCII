#!/usr/bin/env python3
import os
import argparse
from typing import Optional, List

class TreeScannerConfig:
    """Konfigurationsklasse für den TreeScanner.

    Attributes:
        root_path (str): Pfad des Stammverzeichnisses.
        folder_icon (str): Icon für Ordner.
        file_icon (str): Icon für Dateien und Platzhalter.
        max_files_per_dir (int): Maximale Anzahl Dateien pro Verzeichnis.
        max_depth (Optional[int]): Maximale Rekursionstiefe.
        align_comments (bool): Kommentare am Zeilenende ausrichten.
        language (str): Sprache der Programmausgabe (de oder en).
        output_file (str): Pfad und Name der Ausgabedatei.
    """

    def __init__(
        self,
        root_path: str = ".",
        folder_icon: str = "\U0001F4C1",
        file_icon: str = "\U0001F4C4",
        max_files_per_dir: int = 100,
        max_depth: Optional[int] = None,
        align_comments: bool = True,
        language: str = "de",
        output_file: str = "tree.txt"
    ):
        self.root_path = root_path
        self.folder_icon = folder_icon
        self.file_icon = file_icon
        self.max_files_per_dir = max_files_per_dir
        self.max_depth = max_depth
        self.align_comments = align_comments
        self.language = language
        self.output_file = output_file

class TreeScanner:
    """Klasse zum Scannen von Verzeichnissen und Erzeugen einer ASCII-Baumstruktur."""

    def __init__(self, config: TreeScannerConfig):
        """Initialisiert den TreeScanner.

        Args:
            config (TreeScannerConfig): Konfiguration für den Scanner.
        """
        self.config = config
        self.folder_count = 0
        self.file_count = 0
        self.messages = {
            "de": {
                "summary": "Es wurden {folders} Verzeichnisse und {files} Dateien gescannt. Datei {file} geschrieben."
            },
            "en": {
                "summary": "Scanned {folders} folders and {files} files. File {file} written."
            }
        }

    def scan_directory(self, path: str, depth: int = 0, prefix: str = "") -> List[str]:
        """Scannt ein Verzeichnis und gibt eine Liste von ASCII-Zeilen zurück.

        Args:
            path (str): Pfad des zu scannenden Verzeichnisses.
            depth (int): Aktuelle Rekursionstiefe.
            prefix (str): Präfix für Einrückung und Connectoren.

        Returns:
            List[str]: Zeilen der Baumstruktur.
        """
        lines: List[str] = []
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            return [f"{prefix}└── [Zugriff verweigert] {path}"]

        folders = [e for e in entries if os.path.isdir(os.path.join(path, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(path, e))]

        for idx, folder in enumerate(folders):
            self.folder_count += 1
            folder_path = os.path.join(path, folder)
            connector = "├── " if idx < len(folders) - 1 or files else "└── "
            lines.append(f"{prefix}{connector}{self.config.folder_icon} {folder}")
            if self.config.max_depth is None or depth < self.config.max_depth:
                extension = "│   " if idx < len(folders) - 1 or files else "    "
                lines.extend(self.scan_directory(folder_path, depth + 1, prefix + extension))

        visible_files = files[: self.config.max_files_per_dir]
        remaining = len(files) - len(visible_files)
        combined = visible_files.copy()
        if remaining > 0:
            combined.append(f"<und {remaining} weitere Dateien>")

        for idx, name in enumerate(combined):
            if not name.startswith("<und "):
                self.file_count += 1
            connector = "├── " if idx < len(combined) - 1 else "└── "
            lines.append(f"{prefix}{connector}{self.config.file_icon} {name}")

        return lines

    def align_lines_with_comments(self, lines: List[str]) -> List[str]:
        """Richtet alle Zeilen so aus, dass Kommentare am gleichen Spaltenindex stehen.

        Args:
            lines (List[str]): Liste der Baumstruktur-Zeilen ohne Kommentare.

        Returns:
            List[str]: Zeilen mit ausgerichteten Kommentar-Platzhaltern (#).
        """
        max_length = max(len(line.rstrip()) for line in lines)
        aligned: List[str] = []
        for line in lines:
            text = line.rstrip()
            padding = " " * (max_length - len(text) + 2)
            aligned.append(text + padding + "#  ")
        return aligned

    def generate_tree(self) -> str:
        """Generiert den vollständigen Verzeichnisbaum als String.

        Returns:
            str: Mehrzeiliger String mit Ordner-Icon, Ordner- und Dateienstruktur.
        """
        root_name = os.path.basename(os.path.abspath(self.config.root_path)) or self.config.root_path
        lines = [f"{self.config.folder_icon} {root_name}/"]
        lines += self.scan_directory(self.config.root_path)
        if self.config.align_comments:
            lines = self.align_lines_with_comments(lines)
        return "\n".join(lines)

    def print_summary(self, output_file: str) -> None:
        """Gibt eine Zusammenfassung des Scanlaufs aus.

        Args:
            output_file (str): Name der geschriebenen Ausgabedatei.
        """
        message_template = self.messages.get(self.config.language, self.messages["de"])
        print(message_template["summary"].format(folders=self.folder_count, files=self.file_count, file=output_file))

def main():
    """Standalone-Ausführung mit CLI-Parameter-Unterstützung."""
    parser = argparse.ArgumentParser(description="Generiert eine ASCII-Baumstruktur eines Verzeichnisses.")
    parser.add_argument("root_path", nargs="?", default=".", help="Pfad des Stammverzeichnisses (default: aktuelles Verzeichnis).")
    parser.add_argument("-n", "--max-files-per-dir", type=int, default=2, help="Maximale Anzahl Dateien pro Verzeichnis (default: 2).")
    parser.add_argument("-d", "--max-depth", type=int, help="Maximale Rekursionstiefe; unbegrenzt, wenn nicht gesetzt.")
    parser.add_argument("--no-align-comments", action="store_false", dest="align_comments", help="Deaktiviert das Ausrichten der Kommentare am Zeilenende.")
    parser.add_argument("-l", "--language", type=str, default="de", choices=["de", "en"], help="Sprache der Programmausgabe (de oder en).")
    parser.add_argument("-o", "--output", type=str, help="Pfad und Name der Ausgabedatei (Standard: tree.txt)")

    args = parser.parse_args()

    output_file = args.output if args.output else "tree.txt"
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    config = TreeScannerConfig(
        root_path=args.root_path,
        max_files_per_dir=args.max_files_per_dir,
        max_depth=args.max_depth,
        align_comments=args.align_comments,
        language=args.language,
        output_file=output_file
    )
    scanner = TreeScanner(config)
    tree_output = scanner.generate_tree()

    with open(config.output_file, "w", encoding="utf-8") as f:
        f.write(tree_output + "\n")

    scanner.print_summary(config.output_file)

if __name__ == "__main__":
    main()
