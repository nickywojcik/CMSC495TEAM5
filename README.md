# CMSC495TEAM5
A neural network evaluation application

## Overview

## Installation

[!Note]
These instructions assume that Git, Python 3.12.0, and Pip are already installed.

### Clone Repository
```bash
git clone https://github.com/nickywojcik/CMSC495TEAM5
```

Setup Python Virtual Environment
#### Windows
```PowerShell
# Download virtualenv module
& python -m pip install virtualenv

# Create Virtual Environment in current directory
& python -m virtualenv .venv

# Start Virtual Environment
& <ParentDirectory>\.venv\Scripts\Activate.ps1

# Install project requirements
& python -m pip install -r requirements.txt
```

[!Tip]
If an error related to ".venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system." occurs, run the below command in an Administrator PowerShell Console.
```PowerShell
Set-ExecutionPolicy Unrestricted -Force
```
#### Linux
```bash
#TODO
```
## Usage

### Start Virtual Environment
See [Installation](#installation) for Instructions

### Start Flask Server
```python
flask --app neural_network_evaluator run
```