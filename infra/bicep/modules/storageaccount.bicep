@description('Name of the storage account')
param storageAccountName string

@description('Specifies the location of the Azure Machine Learning workspace and dependent resources.')
param location string

@description('The SKU of the storage')
param storageSkuName string

@description('Name of Key Vault to store the secrets')
param keyVaultName string


resource storageAccount 'Microsoft.Storage/storageAccounts@2022-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: storageSkuName
  }
  kind: 'StorageV2'
  properties: {
    publicNetworkAccess: 'Disabled'
    allowBlobPublicAccess: false
    encryption: {
      keySource: 'Microsoft.Storage'
      services: {
        blob: {
          enabled: true
        }
        file: {
          enabled: true
        }
      }
    }
    isHnsEnabled: false
    isNfsV3Enabled: false
    keyPolicy: {
      keyExpirationPeriodInDays: 7
    }
    minimumTlsVersion: 'TLS1_2'
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Deny'
    }
    supportsHttpsTrafficOnly: true
    routingPreference: {
      routingChoice: 'MicrosoftRouting'
    }
  }
}

// Adding secrets to the Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2024-04-01-preview' existing = {
  name: keyVaultName
}

resource storageAccountEndpoint 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  name: 'AZURE-STORAGE-NAME'
  parent: keyVault
  properties: {
    value: storageAccountName
  }
}

resource storageAccountKey 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  name: 'AZURE-STORAGE-KEY'
  parent: keyVault
  properties: { 
    value: storageAccount.listKeys().keys[0].value
  }
}

output storageAccountId string = storageAccount.id
