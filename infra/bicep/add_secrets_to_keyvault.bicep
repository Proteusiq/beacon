@description('Name of the secret to add to the Key Vault')
param SecretName string

@description('Value of the secret to add to the Key Vault')
@secure()
param SecretValue string

@description('Name of Key Vault to store the secrets')
param keyVaultName string


// Adding secrets to the Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2024-04-01-preview' existing = {
  name: keyVaultName
}

resource secretToKeyVault 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  name: SecretName
  parent: keyVault
  properties: {
    value: SecretValue
  }
}
