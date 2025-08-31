// Blockchain explorer utilities

export const getExplorerUrl = (chainId: number): string => {
  switch (chainId) {
    case 5545: // DuckChain Mainnet
      return 'https://duckchain.io'
    default:
      return 'https://duckchain.io' // DuckChain Mainnet
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
    case 5545: return 'DuckChain Mainnet'
    default: return `Chain ${chainId}`
  }
}
