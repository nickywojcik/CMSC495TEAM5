# CMSC495TEAM5
A neural network evaluation application

## Overview

## Installation

[!NOTE]
These instructions assume that Git, Python 3.12.0, and Pip are already installed.

### Clone Repository
```bash
git clone https://github.com/nickywojcik/CMSC495TEAM5
```

### Setup Python Virtual Environment

#### Windows
1. Download virtualenv module
   ```PowerShell
   & python -m pip install virtualenv
   ```
2. Create Virtual Environment in current directory
   ```PowerShell
   & python -m virtualenv .venv
   ```
3. Start Virtual Environment
   ```PowerShell
   & <ParentDirectory>\.venv\Scripts\Activate.ps1
   ```
4. Install project requirements
   ```PowerShell
   & python -m pip install -r requirements.txt
   ```

[!Tip]
   If an error related to ".venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system." occurs, run the below command in an Administrator PowerShell Console.
   ```PowerShell
   Set-ExecutionPolicy Unrestricted -Force
   ```

#### Linux
1. Download virtualenv module
   ```bash
   python3 -m pip install virtualenv
   ```
2. Create Virtual Environment in current directory
   ```bash
   python3 -m virtualenv .venv
   ```
3. Start Virtual Environment
   ```bash
   source <ParentDirectory>/.venv/bin/activate
   ```
4. Install project requirements
   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Usage

### Start Virtual Environment
See [Installation](#installation) for Instructions

### Start Flask Server
```python
flask --app neural_network_evaluator run
```