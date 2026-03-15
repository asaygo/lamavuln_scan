# lamavuln_scan
Use local ollama model to scan for software vfulnerabilities.

## Source Code Overview

The `src` directory contains the core implementation of the **lamavuln_scan** pipeline. It includes the main components responsible for processing downloaded repositories, identifying Go source files, and running vulnerability checks against them.

The modules in this directory work together to automate the following workflow:

### 1. Repository Processing
Extracts and iterates through downloaded repository archives. Each repository is unpacked and prepared for analysis.

### 2. Source Code Discovery
Recursively scans extracted repositories to locate Go source files (`.go`). Only relevant files are passed to the analysis stage to reduce noise and improve performance.

### 3. Vulnerability Analysis
Each discovered Go file is analyzed using custom scanning logic to detect potentially unsafe patterns, suspicious behavior, or known vulnerability indicators. This analysis is designed to identify issues commonly associated with malicious or vulnerable code.

### 4. Modular Scan Pipeline
The scanning logic is structured in modular components so that new detection rules, analyzers, or processing steps can easily be added without modifying the overall pipeline.

## Goal

The goal of this project is to provide a **lightweight and extensible framework for scannining repositories for potential security issues using a local AI model**, enabling automated analysis across large numbers of projects.
