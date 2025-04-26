
# config.py
# Beispielconfig:
#
# from .config import TreeScannerConfig
#

class TreeScannerConfig:
    def __init__(self,
                 root_path=".",
                 folder_icon="📁",
                 file_icon="📄",
                 max_files_per_dir=2,
                 max_depth=None,
                 align_comments=True):
        self.root_path = root_path
        self.folder_icon = folder_icon
        self.file_icon = file_icon
        self.max_files_per_dir = max_files_per_dir
        self.max_depth = max_depth
        self.align_comments = align_comments
