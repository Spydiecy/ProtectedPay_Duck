// Blockchain explorer utilities

export const getExplorerUrl = (chainId: number): string => {
  switch (chainId) {
    case 97: // BNB Smart Chain Testnet
      return 'https://testnet.bscscan.com'
    default:
      return 'https://testnet.bscscan.com' // BNB Smart Chain Testnet
  }
}

export const getTransactionUrl = (txHash: string, chainId: number): string => {
  const baseUrl = getExplorerUrl(chainId)
  return `${baseUrl}/tx/${txHash}`
}

export const getAddressUrl = (address: string, chainId: number): string => {
  const baseUrl = getExplorerUrl(chainId)
  return `${baseUrl}/address/${address}`
}

export const getChainName = (chainId: number): string => {
  switch (chainId) {
    case 97: return 'BNB Smart Chain Testnet'
    default: return `Chain ${chainId}`
  }
}
