'use client'

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useParams, useRouter } from 'next/navigation'
import { useAccount } from 'wagmi'
import { 
  CheckCircleIcon,
  ExclamationTriangleIcon,
  CurrencyDollarIcon,
  UserIcon,
  CalendarIcon,
  ChatBubbleLeftRightIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'
import { shortenAddress, isValidAddress } from '../../../../../utils/address'
import { claimTransferByAddress, getUserTransfers } from '../../../../../utils/contract'
import { useWallet } from '../../../../../context/WalletContext'
import ConnectWallet from '../../../../../components/ConnectWallet'

// Floating emoji animation variants
const floatingEmojis = ['💰', '🎉', '✨', '🚀', '💎', '🌟', '🎊', '💰']

const emojiVariants = {
  animate: {
    y: [0, -10, 0],
    x: [0, 5, -5, 0],
    rotate: [0, 10, -10, 0],
    scale: [1, 1.1, 1],
    transition: {
      duration: 2,
      repeat: Infinity,
      repeatType: "reverse" as const,
      ease: "easeInOut"
    }
  }
}

const pageVariants = {
  initial: { opacity: 0, y: 50 },
  animate: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.8, ease: "easeOut" }
  }
}

const buttonVariants = {
  hover: { 
    scale: 1.05,
    boxShadow: "0 20px 40px rgba(0, 255, 157, 0.3)",
    transition: { duration: 0.3 }
  },
  tap: { scale: 0.95 }
}

interface TransferDetails {
  id: string;
  sender: string;
  receiver: string;
  amount: string;
  timestamp: number;
  remarks: string;
  status: number;
  claimed: boolean;
}

export default function ClaimPage() {
  const params = useParams()
  const router = useRouter()
  const { address, isConnected } = useAccount()
  const { signer } = useWallet()
  
  const [transferDetails, setTransferDetails] = useState<TransferDetails | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isClaiming, setIsClaiming] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const sender = Array.isArray(params.sender) ? params.sender[0] : params.sender
  const receiver = Array.isArray(params.receiver) ? params.receiver[0] : params.receiver
  const amount = Array.isArray(params.amount) ? params.amount[0] : params.amount

  // Fetch transfer details
  useEffect(() => {
    const fetchTransferDetails = async () => {
      if (!sender || !receiver || !amount) {
        setError('Invalid transfer parameters')
        setIsLoading(false)
        return
      }

      try {
        // Validate addresses
        if (!isValidAddress(sender) || !isValidAddress(receiver)) {
          setError('Invalid wallet addresses in the link')
          setIsLoading(false)
          return
        }

        // If no signer, just wait for wallet connection (don't show error)
        if (!signer) {
          setIsLoading(false)
          return
        }

        // Fetch real transfers from the smart contract
        const senderTransfers = await getUserTransfers(signer, sender)
        
        // Find the specific transfer that matches our URL parameters
        const matchingTransfer = senderTransfers.find(transfer => {
          // Check if this transfer matches our URL parameters
          const isCorrectReceiver = transfer.recipient.toLowerCase() === receiver.toLowerCase()
          const isCorrectAmount = transfer.amount === amount
          const isPending = transfer.status === 0 // Unclaimed
          
          return isCorrectReceiver && isCorrectAmount && isPending
        })

        if (!matchingTransfer) {
          setError('Transfer not found or already claimed')
          setIsLoading(false)
          return
        }

        // Convert the contract transfer to our TransferDetails interface
        const transferDetails: TransferDetails = {
          id: `${matchingTransfer.sender}-${matchingTransfer.recipient}-${matchingTransfer.amount}-${matchingTransfer.timestamp}`,
          sender: matchingTransfer.sender,
          receiver: matchingTransfer.recipient,
          amount: matchingTransfer.amount,
          timestamp: matchingTransfer.timestamp * 1000, // Convert to milliseconds
          remarks: matchingTransfer.remarks || 'Transfer for you! 🎉',
          status: matchingTransfer.status,
          claimed: matchingTransfer.status !== 0
        }

        setTransferDetails(transferDetails)
      } catch (err) {
        console.error('Error fetching transfer details:', err)
        setError('Failed to load transfer details from the blockchain')
      } finally {
        setIsLoading(false)
      }
    }

    fetchTransferDetails()
  }, [sender, receiver, amount, signer])

  // Check if connected user is the intended receiver
  const isAuthorizedReceiver = address && transferDetails && 
    address.toLowerCase() === transferDetails.receiver.toLowerCase()

  const handleClaim = async () => {
    if (!signer || !transferDetails || !isAuthorizedReceiver || !sender) return

    setIsClaiming(true)
    setError(null)
    
    try {
      // Call the actual claim function from the smart contract
      await claimTransferByAddress(signer, sender)
      
      setSuccess(true)
      
      // Redirect to dashboard after successful claim
      setTimeout(() => {
        router.push('/dashboard/history')
      }, 3000)
    } catch (err) {
      console.error('Error claiming transfer:', err)
      setError('Failed to claim transfer. Please try again.')
      setSuccess(false)
    } finally {
      setIsClaiming(false)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center"
        >
          <div className="w-16 h-16 border-4 border-green-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading transfer details...</p>
        </motion.div>
      </div>
    )
  }

  // Show wallet connection prompt if no wallet is connected and no errors
  if (!isConnected && !error) {
    return (
      <div className="min-h-screen bg-black text-white relative overflow-hidden">
        {/* Background effects */}
        <div className="absolute inset-0 bg-gradient-to-br from-green-900/20 via-black to-blue-900/20"></div>
        
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative z-10 container mx-auto px-4 py-16"
        >
          <div className="max-w-2xl mx-auto">
            {/* Header */}
            <div className="text-center mb-12">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2 }}
                className="w-20 h-20 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-6"
              >
                <CurrencyDollarIcon className="w-10 h-10 text-white" />
              </motion.div>
              <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
                You've Received a Transfer!
              </h1>
              <p className="text-xl text-gray-300">Connect your wallet to view and claim your transfer</p>
            </div>

            {/* Preview Info */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-700/50 mb-8"
            >
              <div className="text-center mb-8">
                <div className="text-5xl font-bold text-green-400 mb-2">
                  {amount} tBNB
                </div>
                <div className="text-gray-400">Transfer Amount</div>
              </div>

              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <UserIcon className="w-6 h-6 text-green-400" />
                    <span className="text-gray-300">From</span>
                  </div>
                  <span className="text-white font-mono">{shortenAddress(sender)}</span>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <UserIcon className="w-6 h-6 text-blue-400" />
                    <span className="text-gray-300">To</span>
                  </div>
                  <span className="text-white font-mono">{shortenAddress(receiver)}</span>
                </div>
              </div>
            </motion.div>

            {/* Connection Section */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="text-center"
            >
              <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-700/50 flex flex-col items-center">
                <h3 className="text-2xl font-bold text-white mb-4 text-center">Connect Your Wallet</h3>
                <p className="text-gray-400 mb-6 text-center">Connect your wallet to view full transfer details and claim your funds</p>
                <div className="flex justify-center w-full">
                  <ConnectWallet />
                </div>
              </div>
            </motion.div>

            {/* Footer */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
              className="text-center mt-12"
            >
              <p className="text-gray-500 text-sm">
                Powered by <span className="text-green-400 font-semibold">ProtectedPay</span> on BNB Smart Chain
              </p>
            </motion.div>
          </div>
        </motion.div>
      </div>
    )
  }

  if (error || (!transferDetails && isConnected)) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center max-w-md mx-auto p-8"
        >
          <ExclamationTriangleIcon className="w-24 h-24 text-red-400 mx-auto mb-6" />
          <h1 className="text-2xl font-bold text-white mb-4">Transfer Not Found</h1>
          <p className="text-gray-400 mb-8">{error || 'The transfer link appears to be invalid or expired.'}</p>
          <button
            onClick={() => router.push('/')}
            className="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-xl font-semibold transition-colors"
          >
            Go to Homepage
          </button>
        </motion.div>
      </div>
    )
  }

  // If we have transferDetails, render the main claim interface
  if (!transferDetails) {
    // This should not happen based on our logic above, but TypeScript safety
    return null
  }

  if (success) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center relative overflow-hidden">
        {/* Floating emojis */}
        {floatingEmojis.map((emoji, index) => (
          <motion.div
            key={`floating-emoji-${emoji}-${index}`}
            className="absolute text-4xl"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            variants={emojiVariants}
            animate="animate"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ delay: index * 0.2 }}
          >
            {emoji}
          </motion.div>
        ))}

        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center z-10"
        >
          <CheckCircleIcon className="w-32 h-32 text-green-400 mx-auto mb-6" />
          <h1 className="text-4xl font-bold text-white mb-4">Transfer Claimed! 🎉</h1>
          <p className="text-xl text-gray-300 mb-2">{amount} tBNB</p>
          <p className="text-gray-400">Redirecting to dashboard...</p>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-gradient-to-br from-green-900/20 via-black to-blue-900/20"></div>
      
      {/* Floating emojis around claim button area */}
      <div className="absolute inset-0 pointer-events-none">
        {floatingEmojis.map((emoji, index) => (
          <motion.div
            key={`background-emoji-${emoji}-${index}`}
            className="absolute text-2xl opacity-70"
            style={{
              left: `${20 + (index * 10)}%`,
              top: `${40 + Math.sin(index) * 20}%`,
            }}
            variants={emojiVariants}
            animate="animate"
            transition={{ delay: index * 0.3 }}
          >
            {emoji}
          </motion.div>
        ))}
      </div>

      <motion.div
        variants={pageVariants}
        initial="initial"
        animate="animate"
        className="relative z-10 container mx-auto px-4 py-16"
      >
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2 }}
              className="w-20 h-20 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <CurrencyDollarIcon className="w-10 h-10 text-white" />
            </motion.div>
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
              You've Received a Transfer!
            </h1>
            <p className="text-xl text-gray-300">Someone sent you cryptocurrency on ProtectedPay</p>
          </div>

          {/* Transfer Details Card */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-700/50 mb-8"
          >
            {/* Amount */}
            <div className="text-center mb-8">
              <div className="text-5xl font-bold text-green-400 mb-2">
                {amount} tBNB
              </div>
              <div className="text-gray-400">Transfer Amount</div>
            </div>

            {/* Details */}
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <UserIcon className="w-6 h-6 text-green-400" />
                  <span className="text-gray-300">From</span>
                </div>
                <span className="text-white font-mono">{shortenAddress(transferDetails.sender)}</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <UserIcon className="w-6 h-6 text-blue-400" />
                  <span className="text-gray-300">To</span>
                </div>
                <span className="text-white font-mono">{shortenAddress(transferDetails.receiver)}</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <CalendarIcon className="w-6 h-6 text-purple-400" />
                  <span className="text-gray-300">Sent</span>
                </div>
                <span className="text-white">
                  {new Date(transferDetails.timestamp).toLocaleString()}
                </span>
              </div>

              {transferDetails.remarks && (
                <div className="flex items-start space-x-3">
                  <ChatBubbleLeftRightIcon className="w-6 h-6 text-yellow-400 mt-1" />
                  <div>
                    <span className="text-gray-300">Message</span>
                    <p className="text-white mt-1">{transferDetails.remarks}</p>
                  </div>
                </div>
              )}
            </div>
          </motion.div>

          {/* Connection and Claim Section */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="text-center"
          >
            {!isConnected ? (
              <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-700/50 flex flex-col items-center">
                <h3 className="text-2xl font-bold text-white mb-4 text-center">Connect Your Wallet</h3>
                <p className="text-gray-400 mb-6 text-center">Connect your wallet to claim this transfer</p>
                <div className="flex justify-center w-full">
                  <ConnectWallet />
                </div>
              </div>
            ) : (
              <>
                {!isAuthorizedReceiver ? (
                  <div className="bg-red-900/20 backdrop-blur-xl rounded-2xl p-8 border border-red-700/50">
                    <ExclamationTriangleIcon className="w-16 h-16 text-red-400 mx-auto mb-4" />
                    <h3 className="text-2xl font-bold text-white mb-4">Wrong Wallet</h3>
                    <p className="text-gray-400 mb-4">
                      This transfer is intended for {shortenAddress(transferDetails.receiver)}
                    </p>
                    <p className="text-gray-400">
                      You're connected as {shortenAddress(address!)}
                    </p>
                  </div>
                ) : (
                  <div className="space-y-6">
                    <div className="bg-green-900/20 backdrop-blur-xl rounded-2xl p-6 border border-green-700/50">
                      <CheckCircleIcon className="w-12 h-12 text-green-400 mx-auto mb-3" />
                      <h3 className="text-xl font-bold text-white mb-2">Wallet Verified!</h3>
                      <p className="text-gray-400">You're authorized to claim this transfer</p>
                    </div>

                    <motion.button
                      variants={buttonVariants}
                      whileHover="hover"
                      whileTap="tap"
                      onClick={handleClaim}
                      disabled={isClaiming}
                      className="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-4 px-8 rounded-2xl font-bold text-xl disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden"
                    >
                      {isClaiming ? (
                        <div className="flex items-center justify-center space-x-3">
                          <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                          <span>Claiming...</span>
                        </div>
                      ) : (
                        <div className="flex items-center justify-center space-x-3">
                          <SparklesIcon className="w-6 h-6" />
                          <span>Claim Transfer</span>
                          <SparklesIcon className="w-6 h-6" />
                        </div>
                      )}
                    </motion.button>
                  </div>
                )}
              </>
            )}
          </motion.div>

          {/* Footer */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="text-center mt-12"
          >
            <p className="text-gray-500 text-sm">
              Powered by <span className="text-green-400 font-semibold">ProtectedPay</span> on BNB Smart Chain
            </p>
          </motion.div>
        </div>
      </motion.div>
    </div>
  )
}
