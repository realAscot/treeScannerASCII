#!/usr/bin/env python3

from scanner import TreeScanner, TreeScannerConfig

# Beispielkonfiguration
config = TreeScannerConfig(
    root_path=".",
    max_depth=2,
    align_comments=True
)

scanner = TreeScanner(config)
baum = scanner.generate_tree()
print(baum)
