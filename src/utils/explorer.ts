// Blockchain explorer utilities

export const getExplorerUrl = (chainId: number): string => {
  switch (chainId) {
    case 1328: // Sei Testnet
      return 'https://testnet.seistream.app'
    default:
      return 'https://testnet.seistream.app' // Sei Testnet
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
    case 1328: return 'Sei Testnet'
    default: return `Chain ${chainId}`
  }
}
