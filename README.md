# Data Integration

This repository contains all finance projects.

## Repository structure 

```bash

data-integration-finance/
├── .azuredevops/                # Azure DevOps configuration and templates
├── finance/                      # Demand asset bundle
│   ├── bundle/                  # Reusable notebooks source
│   ├── src/                     # Reusable notebooks source
│       ├── topic/               # topic ex. sec quarterly files
            ├── sql/             # sql files to execute
            ├── notebooks/       # python files executed as notebooks
├── shared/
│   ├── notebooks/               # Reusable notebooks source
│   └── packout/                 # Packout library
├── templates/                   # Reusable template for new DABs
└── README.md                    # Project documentation
```