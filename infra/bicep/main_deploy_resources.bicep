@description('Specifies the name of the deployment.')
@minLength(3)
@maxLength(16)
param name string 

@description('Specifies the name of the environment.')
@allowed([
  'dev'
  'tst'
  'prd'
])
param environment string 

@description('Specifies the location of the Azure Machine Learning workspace and dependent resources.')
param location string = 'westeurope'

@description('Specifies the SKU of the storage')
param storageSkuName string


var lowercasedName = toLower(name)
var storageAccountName = 'st${lowercasedName}${environment}' // fx: stbeaconprd
var keyVaultName = 'kv-${lowercasedName}-${environment}' // fx: kv-beacon-prd


module storageAccount './modules/storageaccount.bicep' = {
  name: 'storageaccountDeploy'
  params: {
    location: location
    storageAccountName: storageAccountName
    storageSkuName: storageSkuName
    keyVaultName: keyVaultName // param used to store the secrets
  }
}

module keyvault './modules/keyvault.bicep' = {
  name: 'keyvaultDeploy'
  params: {
    location: location
    keyVaultName: keyVaultName
  }
}

