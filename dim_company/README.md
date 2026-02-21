# 📊 Dim Company
> _Builds a Dimensional Table describing attributes of publicly traded companies_


## 🚀 Overview
> _Combines several factors including exchange data, CIKs and SP500 flags as core dimensions in describing CIKs_


## 🏗️ Architecture
> _Briefly outline the architecture or include a diagram._

- **Data Sources**: 
- **Processing**: 
- **Storage**: 
- **Visualization**: 


## 🛠️ Tech Stack
> _List the main technologies used._

- Language: 
- Frameworks: 
- Visualization: 
- Deployment: DAB

## 📦 Setup Local Environment
Dependencies:
- Python 3.10+
- uv
- Jdk

```powershell
# Clone the repo
git clone REPO_URL
cd REPO_NAME
# Create a virtual environment
cd my_project
uv venv .venv
# vscode will automatically detect the virtual environment
# If not, you can manually select it in the bottom left corner of VSCode
# If you are using PowerShell, you may need to set the execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Activate the virtual environment
.\.venv\Scripts\activate.ps1
# Install dependencies
uv pip install -r .\src\requirements-dev.txt
```

## 📈 Run Tests
```bash
# Run unit tests
pytest -v
```
