#!/usr/bin/env python3

"""
Verzeichnisscanner mit strukturierter Ausgabe.
Funktioniert sowohl als Standalone-Skript als auch als einbindbares Modul.
"""

import os
from typing import Optional, List

# === Konfigurationsklasse ===
class TreeScannerConfig:
    def __init__(self,
                 root_path: str = ".",
                 folder_icon: str = "\U0001F4C1",
                 file_icon: str = "\U0001F4C4",
                 max_files_per_dir: int = 100,
                 max_depth: Optional[int] = None,
                 align_comments: bool = True):      # 
        self.root_path = root_path
        self.folder_icon = folder_icon
        self.file_icon = file_icon
        self.max_files_per_dir = max_files_per_dir
        self.max_depth = max_depth
        self.align_comments = align_comments

# === Hauptklasse ===
class TreeScanner:
    def __init__(self, config: TreeScannerConfig):
        self.config = config

    def scan_directory(self, path: str, depth: int = 0, prefix: str = "") -> List[str]:
        lines = []
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            return [f"{prefix}└── [Zugriff verweigert] {path}"]

        folders = [e for e in entries if os.path.isdir(os.path.join(path, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(path, e))]

        for idx, folder in enumerate(folders):
            folder_path = os.path.join(path, folder)
            connector = "├── " if idx < len(folders) - 1 or files else "└── "
            line = f"{prefix}{connector}{self.config.folder_icon} {folder}"
            lines.append(line)
            if self.config.max_depth is None or depth < self.config.max_depth:
                extension = "│   " if idx < len(folders) - 1 or files else "    "
                lines.extend(self.scan_directory(folder_path, depth + 1, prefix + extension))

        for idx, file in enumerate(files[:self.config.max_files_per_dir]):
            connector = "├── " if idx < len(files[:self.config.max_files_per_dir]) - 1 else "└── "
            line = f"{prefix}{connector}{self.config.file_icon} {file}"
            lines.append(line)

        if len(files) > self.config.max_files_per_dir:
            remaining = len(files) - self.config.max_files_per_dir
            lines.append(f"{prefix}└── <und {remaining} weitere Dateien>")

        return lines

    def align_lines_with_comments(self, lines: List[str]) -> List[str]:
        max_length = max(len(line.rstrip()) for line in lines)
        return [
            line.rstrip() + (" " * (max_length - len(line.rstrip()) + 2)) + "#  "
            for line in lines
        ]

    def generate_tree(self) -> str:
        root_name = os.path.basename(os.path.abspath(self.config.root_path)) or self.config.root_path
        lines = [f"{self.config.folder_icon} {root_name}/"]
        lines += self.scan_directory(self.config.root_path)

        if self.config.align_comments:
            lines = self.align_lines_with_comments(lines)

        return "\n".join(lines)

# === Standalone-Ausführung ===
def main():
    config = TreeScannerConfig()
    scanner = TreeScanner(config)
    tree_output = scanner.generate_tree()
    with open("tree.txt", "w", encoding="utf-8") as f:
        f.write(tree_output + "\n")

if __name__ == "__main__":
    main()
