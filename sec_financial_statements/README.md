# 📊 Project Name
> _Asset Bundle for SEC Financial Statement Data


## 🚀 Overview
> _Asset Bundle that retreives, organizes and generates raw and cleansed data to be used downstream.


## 🏗️ Architecture
> _Builds files from several data sources retreived using primarily http requests. 

- **Data Sources**: 
- **Processing**: 
- **Volumes**: Raw data is stored in Volumes, processed later into the operations.finance_staging schema 
- **Visualization**: 


## 🛠️ Tech Stack
> _List the main technologies used._

- Language: Python, SQL, YAML
- Frameworks: Databricks framework for Data engineering best practice using Data asset bundles. 
- Visualization: 
- Deployment: DAB

## 📦 Setup Local Environment
Dependencies:
- Python 3.10+

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
