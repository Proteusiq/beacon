# Infrastructure as Code (IaC) with GitHub Actions

This document outlines the best practices for managing Infrastructure as Code using GitHub Actions and Bicep templates.

## Directory Structure

```text
infra/
├── bicep/
│   ├── main_deploy_resources.bicep          # Main deployment template
│   └── modules/                             # Reusable modules
│       ├── keyvault.bicep
│       └── storageaccount.bicep
├── params/                                  # Environment-specific parameters
│   ├── dev_params.json
│   ├── tst_params.json
│   └── prd_params.json
└── scripts/                                 # Infrastructure-related scripts
```

## GitHub Actions Workflow Structure

### Main Deployment Workflow
The main deployment workflow (`main_deploy_resources.yml`) implements a multi-environment deployment strategy:

- Development (DEV) - triggered by merges to `main`
- Testing (TST) - triggered by merges to `staging`
- Production (PRD) - triggered by merges to `release`

### Reusable Workflows
We implement reusable workflows to maintain DRY (Don't Repeat Yourself) principles and ensure consistent deployment across environments.

## Environment-Specific Parameters
Each environment (DEV, TST, PRD) has its own parameter file containing environment-specific configurations. These parameter files should be used to store all environment-specific values, avoiding any hardcoding in workflows or Bicep templates.

Example parameter file structure:
```json
{
    "parameters": {
        "environment": {
            "value": "dev"
        },
        "location": {
            "value": "westeurope"
        },
        "keyVaultName": {
            "value": "kv-myapp-dev"
        },
        "storageAccountSku": {
            "value": "Standard_LRS"
        },
    }
}
```

Usage in workflows:
```yaml
- name: 'Extract Resource Group Name'
 id: get-rg
 run: |
    NAME=$(jq -r '.parameters.name.value' ${{ inputs.parameters-file }})
    ENV=$(jq -r '.parameters.environment.value' ${{ inputs.parameters-file }})
    RG_NAME=rg-${NAME}-${ENV}
    echo "rg_name=$RG_NAME" >> $GITHUB_OUTPUT ### rg_name is used in the 'Add Secrets to Key Vault' step
    echo "Resource Group Name: $RG_NAME"

- name: Deploy Infrastructure
  run: |
    az deployment group create \
      --resource-group ${{ steps.get-rg.outputs.rg_name }} \ ### rg_name variable defined in the 'Extract Resource Group Name' step
      --template-file infra/bicep/main_deploy_resources.bicep \
      --parameters @params/${{ vars.ENVIRONMENT }}_params.json
```

Usage in Bicep:
```bicep
param environment string
param location string
param keyVaultName string
param storageAccountSku string
```

## Security Best Practices

1. **Network Security**
   - Private network access only
   - Azure Services bypass enabled
   - Reference implementation:

2. **Secrets Management**
   - Azure-related secrets should be stored in Azure Key Vault during resource deployment, eg.
     - Connection strings
     - Storage account keys
     - Database credentials
     - Service principal credentials
   - External secrets flow:
     1. Store external secrets in GitHub Secrets (e.g., third-party API keys, external service credentials)
     2. Use GitHub Actions workflow to securely transfer these secrets to Azure Key Vault
     3. Applications access all secrets (both Azure-related and external) from Key Vault
   
   Application Configuration:
   - Only Key Vault URL needs to be stored in application's .env file
   - Applications must be granted RBAC access to Key Vault (e.g., "Key Vault Secrets User" role)
   - Applications can then fetch all required secrets using Azure SDK with managed identity

   Example .env file:
   ```env
   AZURE_KEY_VAULT_URL=https://kv-myapp-dev.vault.azure.net
   ```

## Deployment Strategy

### 1. Environment Progression
- Changes flow from DEV → TST → PRD
- Each environment is triggered by specific branch merges
- Manual triggers available through `workflow_dispatch`

### 2. Resource Naming Convention
Resources follow a consistent naming pattern:
- Key Vault: `kv-{name}-{environment}`
- Storage Account: `st{name}{environment}`
