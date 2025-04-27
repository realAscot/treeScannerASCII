import os
import argparse
from typing import Optional, List

class TreeScannerConfig:
    def __init__(self, root_path: str = ".", folder_icon: str = "\U0001F4C1", file_icon: str = "\U0001F4C4", max_files_per_dir: int = 2, max_depth: Optional[int] = None, align_comments: bool = True, language: str = "de"):
        self.root_path = root_path
        self.folder_icon = folder_icon
        self.file_icon = file_icon
        self.max_files_per_dir = max_files_per_dir
        self.max_depth = max_depth
        self.align_comments = align_comments
        self.language = language

class TreeScanner:
    def __init__(self, config: TreeScannerConfig):
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
        max_length = max(len(line.rstrip()) for line in lines)
        aligned: List[str] = []
        for line in lines:
            text = line.rstrip()
            padding = " " * (max_length - len(text) + 2)
            aligned.append(text + padding + "#  ")
        return aligned

    def generate_tree(self) -> str:
        root_name = os.path.basename(os.path.abspath(self.config.root_path)) or self.config.root_path
        lines = [f"{self.config.folder_icon} {root_name}/"]
        lines += self.scan_directory(self.config.root_path)
        if self.config.align_comments:
            lines = self.align_lines_with_comments(lines)
        return "\n".join(lines)

    def print_summary(self, output_file: str) -> None:
        message_template = self.messages.get(self.config.language, self.messages["de"])
        print(message_template["summary"].format(folders=self.folder_count, files=self.file_count, file=output_file))

def main():
    parser = argparse.ArgumentParser(description="Generiert eine ASCII-Baumstruktur eines Verzeichnisses.")
    parser.add_argument("root_path", nargs="?", default=".", help="Pfad des Stammverzeichnisses (default: aktuelles Verzeichnis).")
    parser.add_argument("-n", "--max-files-per-dir", type=int, default=2, help="Maximale Anzahl Dateien pro Verzeichnis (default: 2).")
    parser.add_argument("-d", "--max-depth", type=int, help="Maximale Rekursionstiefe; unbegrenzt, wenn nicht gesetzt.")
    parser.add_argument("--no-align-comments", action="store_false", dest="align_comments", help="Deaktiviert das Ausrichten der Kommentare am Zeilenende.")
    parser.add_argument("-l", "--language", type=str, default="de", choices=["de", "en"], help="Sprache der Programmausgabe (de oder en).")
    args = parser.parse_args()

    config = TreeScannerConfig(
        root_path=args.root_path,
        max_files_per_dir=args.max_files_per_dir,
        max_depth=args.max_depth,
        align_comments=args.align_comments,
        language=args.language
    )
    scanner = TreeScanner(config)
    tree_output = scanner.generate_tree()

    output_file = "tree.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(tree_output + "\n")

    scanner.print_summary(output_file)

if __name__ == "__main__":
    main()
