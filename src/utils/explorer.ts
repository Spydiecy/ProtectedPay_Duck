// Blockchain explorer utilities

export const getExplorerUrl = (chainId: number): string => {
  switch (chainId) {
    case 2810: // Morph Holesky Testnet
      return 'https://explorer-holesky.morphl2.io'
    default:
      return 'https://explorer-holesky.morphl2.io' // Morph Holesky Testnet
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
    case 2810: return 'Morph Holesky'
    default: return `Chain ${chainId}`
  }
}
