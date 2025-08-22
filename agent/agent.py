import requests
from web3 import Web3
from google.adk.agents import Agent
from typing import Optional

# BNB Smart Chain Testnet configuration
BNB_TESTNET_RPC = "https://bsc-testnet-rpc.publicnode.com"

# ProtectedPay contract address (testnet only)
PROTECTEDPAY_CONTRACT_ADDRESS = "0xCa36dD890F987EDcE1D6D7C74Fb9df627c216BF6"

# Initialize Web3 for testnet
w3 = Web3(Web3.HTTPProvider(BNB_TESTNET_RPC))

# User session state for private key
user_private_key = None

# User session state for network preference
user_network_preference = "testnet"

# Network configuration for balance checking (testnet only)
NETWORK_CONFIG = {
    "rpc_url": BNB_TESTNET_RPC,
    "name": "BNB Smart Chain Testnet",
    "chain_id": 97,
    "currency_symbol": "tBNB"
}

# Contract ABI (extracted from frontend)
CONTRACT_ABI = [
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_potId",
				"type": "bytes32"
			}
		],
		"name": "breakPot",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_senderAddress",
				"type": "address"
			}
		],
		"name": "claimTransferByAddress",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_transferId",
				"type": "bytes32"
			}
		],
		"name": "claimTransferById",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_senderUsername",
				"type": "string"
			}
		],
		"name": "claimTransferByUsername",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_paymentId",
				"type": "bytes32"
			}
		],
		"name": "contributeToGroupPayment",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_potId",
				"type": "bytes32"
			}
		],
		"name": "contributeToSavingsPot",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_recipient",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_numParticipants",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_remarks",
				"type": "string"
			}
		],
		"name": "createGroupPayment",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_targetAmount",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_remarks",
				"type": "string"
			}
		],
		"name": "createSavingsPot",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "paymentId",
				"type": "bytes32"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "GroupPaymentCompleted",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "paymentId",
				"type": "bytes32"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "contributor",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "GroupPaymentContributed",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "paymentId",
				"type": "bytes32"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "creator",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "totalAmount",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "numParticipants",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "remarks",
				"type": "string"
			}
		],
		"name": "GroupPaymentCreated",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "potId",
				"type": "bytes32"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "PotBroken",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "potId",
				"type": "bytes32"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "contributor",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "PotContribution",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_transferId",
				"type": "bytes32"
			}
		],
		"name": "refundTransfer",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_username",
				"type": "string"
			}
		],
		"name": "registerUsername",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "potId",
				"type": "bytes32"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "targetAmount",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "remarks",
				"type": "string"
			}
		],
		"name": "SavingsPotCreated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_recipient",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "_remarks",
				"type": "string"
			}
		],
		"name": "sendToAddress",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_username",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_remarks",
				"type": "string"
			}
		],
		"name": "sendToUsername",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "transferId",
				"type": "bytes32"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "TransferClaimed",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "transferId",
				"type": "bytes32"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "remarks",
				"type": "string"
			}
		],
		"name": "TransferInitiated",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "transferId",
				"type": "bytes32"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "TransferRefunded",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "username",
				"type": "string"
			}
		],
		"name": "UserRegistered",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_paymentId",
				"type": "bytes32"
			},
			{
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "getGroupPaymentContribution",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_paymentId",
				"type": "bytes32"
			}
		],
		"name": "getGroupPaymentDetails",
		"outputs": [
			{
				"internalType": "address",
				"name": "creator",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "totalAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "amountPerPerson",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "numParticipants",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "amountCollected",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "enum ProtectedPay.GroupPaymentStatus",
				"name": "status",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "remarks",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_sender",
				"type": "address"
			}
		],
		"name": "getPendingTransfers",
		"outputs": [
			{
				"internalType": "bytes32[]",
				"name": "",
				"type": "bytes32[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_potId",
				"type": "bytes32"
			}
		],
		"name": "getSavingsPotDetails",
		"outputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "targetAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "currentAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "enum ProtectedPay.PotStatus",
				"name": "status",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "remarks",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_transferId",
				"type": "bytes32"
			}
		],
		"name": "getTransferDetails",
		"outputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "enum ProtectedPay.TransferStatus",
				"name": "status",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "remarks",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_userAddress",
				"type": "address"
			}
		],
		"name": "getUserByAddress",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_username",
				"type": "string"
			}
		],
		"name": "getUserByUsername",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_userAddress",
				"type": "address"
			}
		],
		"name": "getUserProfile",
		"outputs": [
			{
				"internalType": "string",
				"name": "username",
				"type": "string"
			},
			{
				"internalType": "bytes32[]",
				"name": "transferIds",
				"type": "bytes32[]"
			},
			{
				"internalType": "bytes32[]",
				"name": "groupPaymentIds",
				"type": "bytes32[]"
			},
			{
				"internalType": "bytes32[]",
				"name": "participatedGroupPayments",
				"type": "bytes32[]"
			},
			{
				"internalType": "bytes32[]",
				"name": "savingsPotIds",
				"type": "bytes32[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_userAddress",
				"type": "address"
			}
		],
		"name": "getUserTransfers",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "sender",
						"type": "address"
					},
					{
						"internalType": "address",
						"name": "recipient",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "amount",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "timestamp",
						"type": "uint256"
					},
					{
						"internalType": "enum ProtectedPay.TransferStatus",
						"name": "status",
						"type": "uint8"
					},
					{
						"internalType": "string",
						"name": "remarks",
						"type": "string"
					}
				],
				"internalType": "struct ProtectedPay.Transfer[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"name": "groupPayments",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "paymentId",
				"type": "bytes32"
			},
			{
				"internalType": "address",
				"name": "creator",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "totalAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "amountPerPerson",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "numParticipants",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "amountCollected",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "remarks",
				"type": "string"
			},
			{
				"internalType": "enum ProtectedPay.GroupPaymentStatus",
				"name": "status",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_paymentId",
				"type": "bytes32"
			},
			{
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "hasContributedToGroupPayment",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "pendingTransfersBySender",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"name": "savingsPots",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "potId",
				"type": "bytes32"
			},
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "targetAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "currentAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "enum ProtectedPay.PotStatus",
				"name": "status",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "remarks",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"name": "transfers",
		"outputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "enum ProtectedPay.TransferStatus",
				"name": "status",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "remarks",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "usernameToAddress",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "users",
		"outputs": [
			{
				"internalType": "string",
				"name": "username",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Initialize contract for testnet
contract = w3.eth.contract(address=PROTECTEDPAY_CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def set_private_key(private_key: str) -> dict:
    """Set the private key for signing transactions.
    
    Args:
        private_key (str): The private key (with or without '0x' prefix)
        
    Returns:
        dict: status and result or error msg.
    """
    global user_private_key
    
    try:
        # Clean the private key
        if private_key.startswith('0x'):
            clean_key = private_key[2:]
        else:
            clean_key = private_key
            
        # Validate private key format (64 hex characters)
        if len(clean_key) != 64:
            return {
                "status": "error",
                "error_message": "Invalid private key format. Private key must be 64 hex characters (32 bytes)."
            }
            
        # Test if the private key is valid by trying to derive an account
        try:
            account = w3.eth.account.from_key('0x' + clean_key)
            user_private_key = '0x' + clean_key
            
            return {
                "status": "success",
                "report": f"Private key set successfully. Wallet address: {account.address}",
                "wallet_address": account.address
            }
        except Exception as key_error:
            return {
                "status": "error", 
                "error_message": f"Invalid private key: {str(key_error)}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error setting private key: {str(e)}"
        }

def get_wallet_info() -> dict:
    """Get information about the currently set wallet.
    
    Returns:
        dict: status and wallet information or error msg.
    """
    global user_private_key
    
    if user_private_key is None:
        return {
            "status": "no_key",
            "report": "No private key set. Please set a private key using set_private_key() to enable transaction signing.",
            "wallet_address": None
        }
    
    try:
        account = w3.eth.account.from_key(user_private_key)
        return {
            "status": "success",
            "report": f"Wallet configured. Address: {account.address}",
            "wallet_address": account.address,
            "has_private_key": True
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error with current private key: {str(e)}"
        }

def clear_private_key() -> dict:
    """Clear the stored private key for security.
    
    Returns:
        dict: status and result.
    """
    global user_private_key
    user_private_key = None
    
    return {
        "status": "success",
        "report": "Private key cleared successfully."
    }

def set_user_network_preference(network: str) -> dict:
    """Set the user's preferred network for transactions. Only testnet is currently supported.
    
    Args:
        network (str): The network preference (must be "testnet")
        
    Returns:
        dict: status and result or error msg.
    """
    global user_network_preference
    
    if network.lower() != "testnet":
        return {
            "status": "error",
            "error_message": "Only testnet is supported. ProtectedPay is not yet available on mainnet."
        }
    
    user_network_preference = network.lower()
    
    return {
        "status": "success",
        "report": f"Network preference set to: {user_network_preference}",
        "network": user_network_preference
    }

def get_user_network_preference() -> dict:
    """Get the user's current network preference.
    
    Returns:
        dict: status and current network preference.
    """
    global user_network_preference
    
    return {
        "status": "success",
        "report": f"Current network preference: {user_network_preference}",
        "network": user_network_preference
    }

def explain_protectedpay_networks() -> dict:
    """Explain the available networks for ProtectedPay.
    
    Returns:
        dict: status and network information.
    """
    return {
        "status": "success",
        "report": """ProtectedPay is currently available on BNB Smart Chain Testnet only.

Network Details:
- BNB Smart Chain Testnet
  - Chain ID: 97
  - RPC URL: https://bsc-testnet-rpc.publicnode.com
  - Currency: tBNB (testnet BNB)
  - Explorer: https://testnet.bscscan.com
  - Contract Address: 0xCa36dD890F987EDcE1D6D7C74Fb9df627c216BF6

To get testnet BNB for transactions, you can use the BNB Smart Chain testnet faucet.""",
        "networks": {
            "testnet": {
                "name": "BNB Smart Chain Testnet",
                "chain_id": 97,
                "rpc_url": "https://bsc-testnet-rpc.publicnode.com",
                "currency": "tBNB",
                "explorer": "https://testnet.bscscan.com",
                "contract_address": "0xCa36dD890F987EDcE1D6D7C74Fb9df627c216BF6",
                "available": True
            }
        }
    }

def check_network_for_transaction(network: Optional[str]) -> dict:
    """Check if the specified network is valid for transactions.
    
    Args:
        network (str): Network to check
        
    Returns:
        dict: validation result
    """
    if network and network.lower() != "testnet":
        return {
            "status": "error",
            "error_message": "ProtectedPay is only available on testnet. Please use 'testnet' or leave network unspecified."
        }
    return {"status": "success"}

def get_contract_for_network(network: str) -> tuple:
    """Get contract instance and Web3 instance for the specified network.
    
    Args:
        network (str): Network name
        
    Returns:
        tuple: (contract, web3_instance)
    """
    if network.lower() != "testnet":
        raise ValueError("Only testnet is supported")
    
    return contract, w3

def execute_contract_transaction(contract, function_name: str, params: dict, value_wei: int, network: str, network_w3) -> dict:
    """Execute a smart contract transaction with the stored private key.
    
    Args:
        contract: Web3 contract instance
        function_name (str): Name of the contract function to call
        params (dict): Parameters for the function
        value_wei (int): Amount of wei to send with transaction
        network (str): Network being used
        network_w3: Web3 instance for the specific network
        
    Returns:
        dict: status and transaction result or error msg.
    """
    global user_private_key
    
    if user_private_key is None:
        return {
            "status": "no_key",
            "error_message": "No private key set. Please set a private key using set_private_key() to enable transaction signing."
        }
    
    try:
        # Get account from private key
        account = network_w3.eth.account.from_key(user_private_key)
        print(f"Account address: {account.address}")
        print(f"Network: {network}")
        print(f"Contract address: {contract.address}")
        print(f"Function: {function_name}")
        print(f"Parameters: {params}")
        
        # Check account balance
        balance = network_w3.eth.get_balance(account.address)
        print(f"Account balance: {network_w3.from_wei(balance, 'ether')} tBNB")
        
        if balance == 0:
            return {
                "status": "error",
                "error_message": f"Account {account.address} has zero balance. Need tBNB for gas fees."
            }
        
        # Get the contract function
        contract_function = getattr(contract.functions, function_name)(**params)
        
        # Build transaction with better gas estimation
        try:
            # First, estimate gas
            gas_estimate = contract_function.estimate_gas({
                'from': account.address,
                'value': value_wei
            })
            # Add 20% buffer to gas estimate
            gas_limit = int(gas_estimate * 1.2)
        except Exception as gas_error:
            # If gas estimation fails, use a higher default
            print(f"Gas estimation failed: {gas_error}, using default gas limit")
            gas_limit = 500000
        
        # Get current gas price
        try:
            gas_price = network_w3.eth.gas_price
            # Increase gas price by 10% to ensure faster confirmation
            gas_price = int(gas_price * 1.1)
        except Exception as price_error:
            print(f"Gas price fetch failed: {price_error}, using default gas price")
            gas_price = network_w3.to_wei('20', 'gwei')
        
        # Build transaction
        transaction = contract_function.build_transaction({
            'from': account.address,
            'value': value_wei,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'nonce': network_w3.eth.get_transaction_count(account.address),
            'chainId': 97  # BNB Smart Chain Testnet chain ID
        })
        
        # Sign transaction
        signed_txn = network_w3.eth.account.sign_transaction(transaction, user_private_key)
        
        # Send transaction
        tx_hash = network_w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        # Wait for transaction receipt
        tx_receipt = network_w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        return {
            "status": "success",
            "report": f"Transaction executed successfully on {network}",
            "transaction_hash": tx_hash.hex(),
            "block_number": tx_receipt.blockNumber,
            "gas_used": tx_receipt.gasUsed,
            "from_address": account.address,
            "network": network
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"Transaction execution error: {error_msg}")
        
        # Provide more specific error messages for common issues
        if "insufficient funds" in error_msg.lower():
            return {
                "status": "error",
                "error_message": f"Insufficient funds for transaction. Error: {error_msg}"
            }
        elif "gas" in error_msg.lower():
            return {
                "status": "error", 
                "error_message": f"Gas-related error. Try increasing gas limit or price. Error: {error_msg}"
            }
        elif "nonce" in error_msg.lower():
            return {
                "status": "error",
                "error_message": f"Nonce error. Transaction may have been sent before. Error: {error_msg}"
            }
        elif "revert" in error_msg.lower():
            return {
                "status": "error",
                "error_message": f"Contract execution reverted. Check contract conditions. Error: {error_msg}"
            }
        else:
            return {
                "status": "error",
                "error_message": f"Transaction execution failed: {error_msg}"
            }

def get_protectedpay_info() -> dict:
    """Get information about the ProtectedPay contract on BNB Smart Chain Testnet.
    
    Returns:
        dict: Information about ProtectedPay contract deployment
    """
    return {
        "status": "success",
        "report": "ProtectedPay Contract Info:\n\n" +
                  "🧪 BNB SMART CHAIN TESTNET:\n" +
                  f"- Contract Address: {PROTECTEDPAY_CONTRACT_ADDRESS}\n" +
                  "- Status: FULLY DEPLOYED ✅\n" +
                  "- Features: All ProtectedPay functions available (usernames, transfers, group payments, savings pots)\n" +
                  "- Chain ID: 97\n" +
                  "- Native Token: tBNB\n\n" +
                  "📝 Note: This agent only supports BNB Smart Chain Testnet.",
        "contract_address": PROTECTEDPAY_CONTRACT_ADDRESS,
        "network": "testnet",
        "chain_id": 97
    }

def get_token_price(token_symbol: str) -> dict:
    """Retrieves the current price of a cryptocurrency token in USD.

    Args:
        token_symbol (str): The symbol of the cryptocurrency token (e.g., 'BTC', 'ETH', 'BNB').

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Convert common token names to symbols
        token_mappings = {
            'bitcoin': 'BTC',
            'ethereum': 'ETH',
            'bnb': 'BNB',
            'binance': 'BNB',
            'usdc': 'USDC',
            'usdt': 'USDT',
            'cardano': 'ADA',
            'solana': 'SOL',
            'polkadot': 'DOT',
            'chainlink': 'LINK',
            'litecoin': 'LTC',
            'dogecoin': 'DOG',
            'tbnb': 'BNB'  # Testnet BNB maps to BNB for pricing
        }
        
        normalized_token = token_symbol.lower().strip()
        if normalized_token in token_mappings:
            token_symbol = token_mappings[normalized_token]
        else:
            token_symbol = token_symbol.upper().strip()
        
        url = f"https://api.coinbase.com/v2/prices/{token_symbol}-USD/spot"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'data' in data and 'amount' in data['data']:
            price = float(data['data']['amount'])
            currency = data['data']['currency']
            
            return {
                "status": "success",
                "report": f"The current price of {token_symbol} is ${price:,.2f} {currency}",
                "token": token_symbol,
                "price": price,
                "currency": currency
            }
        else:
            return {
                "status": "error",
                "error_message": f"Price data not found for token '{token_symbol}'"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch price for '{token_symbol}': {str(e)}"
        }

def register_username(username: str, user_address: str) -> dict:
    """Register a username for a user address on ProtectedPay (testnet only).

    Args:
        username (str): The username to register
        user_address (str): The user's wallet address

    Returns:
        dict: status and result or error msg.
    """
    try:
        if not w3.is_address(user_address):
            return {
                "status": "error",
                "error_message": f"Invalid address format: {user_address}"
            }
        
        # Execute the transaction on testnet
        tx_result = execute_contract_transaction(
            contract=contract,
            function_name="registerUsername", 
            params={
                "_username": username
            },
            value_wei=0,  # No value needed for username registration
            network="testnet",
            network_w3=w3
        )
        
        if tx_result["status"] == "success":
            tx_result["report"] = f"Successfully registered username '{username}' for address {user_address} on testnet"
            tx_result["username"] = username
            tx_result["registered_address"] = user_address
        
        return tx_result
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing username registration: {str(e)}"
        }

def send_to_address(recipient_address: str, amount_bnb: str, remarks: str, sender_address: str) -> dict:
    """Send BNB tokens to a specific address (testnet only).

    Args:
        recipient_address (str): The recipient's wallet address
        amount_bnb (str): Amount of BNB to send
        remarks (str): Message or remarks for the transfer
        sender_address (str): The sender's wallet address

    Returns:
        dict: status and result or error msg.
    """
    try:
        if not w3.is_address(recipient_address):
            return {
                "status": "error",
                "error_message": f"Invalid recipient address: {recipient_address}"
            }
        
        if not w3.is_address(sender_address):
            return {
                "status": "error",
                "error_message": f"Invalid sender address: {sender_address}"
            }
        
        amount_wei = w3.to_wei(float(amount_bnb), 'ether')
        
        # Execute the transaction on testnet
        tx_result = execute_contract_transaction(
            contract=contract,
            function_name="sendToAddress", 
            params={
                "_recipient": recipient_address,
                "_remarks": remarks
            },
            value_wei=amount_wei,
            network="testnet",
            network_w3=w3
        )
        
        if tx_result["status"] == "success":
            tx_result["report"] = f"Successfully sent {amount_bnb} BNB to {recipient_address} with message '{remarks}' on testnet"
            tx_result["amount_bnb"] = amount_bnb
            tx_result["recipient"] = recipient_address
            tx_result["remarks"] = remarks
        
        return tx_result
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing send transaction: {str(e)}"
        }

def send_to_username(username: str, amount_bnb: str, remarks: str, sender_address: str, network: Optional[str] = None) -> dict:
    """Send BNB tokens to a user by their username (testnet only).

    Args:
        username (str): The recipient's username
        amount_bnb (str): Amount of BNB to send
        remarks (str): Message or remarks for the transfer
        sender_address (str): The sender's wallet address
        network (str): Network to use (must be "testnet" or None)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Only testnet is supported
        if network is not None and network.lower() != "testnet":
            return {
                "status": "error",
                "error_message": "Only testnet is supported for ProtectedPay operations."
            }
        
        if not w3.is_address(sender_address):
            return {
                "status": "error",
                "error_message": f"Invalid sender address: {sender_address}"
            }
        
        amount_wei = w3.to_wei(float(amount_bnb), 'ether')
        
        # Execute the transaction on testnet
        tx_result = execute_contract_transaction(
            contract=contract,
            function_name="sendToUsername", 
            params={
                "_username": username,
                "_remarks": remarks
            },
            value_wei=amount_wei,
            network="testnet",
            network_w3=w3
        )
        
        if tx_result["status"] == "success":
            tx_result["report"] = f"Successfully sent {amount_bnb} BNB to username '{username}' with message '{remarks}' on testnet"
            tx_result["amount_bnb"] = amount_bnb
            tx_result["recipient_username"] = username
            tx_result["remarks"] = remarks
        
        return tx_result
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing send to username transaction: {str(e)}"
        }

def get_user_by_username(username: str, network: Optional[str] = None) -> dict:
    """Get the address associated with a username.

    Args:
        username (str): The username to look up
        network (str): Network to use (only "testnet" is supported)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Check which network to use
        network_check = check_network_for_transaction(network)
        if network_check["status"] == "error":
            return network_check
        
        # Get contract instance for testnet
        network_contract, _ = get_contract_for_network("testnet")
        
        address = network_contract.functions.getUserByUsername(username).call()
        
        if address == "0x0000000000000000000000000000000000000000":
            return {
                "status": "error",
                "error_message": f"Username '{username}' is not registered on testnet"
            }
        
        return {
            "status": "success",
            "report": f"Username '{username}' is registered to address: {address} on testnet",
            "username": username,
            "address": address,
            "network": "testnet",
            "contract_address": PROTECTEDPAY_CONTRACT_ADDRESS
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error looking up username '{username}': {str(e)}"
        }

def get_user_by_address(user_address: str, network: Optional[str] = None) -> dict:
    """Get the username associated with an address (testnet only).

    Args:
        user_address (str): The wallet address to look up
        network (str): Network to use (must be "testnet" or None)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Only testnet is supported
        if network is not None and network.lower() != "testnet":
            return {
                "status": "error",
                "error_message": "Only testnet is supported for ProtectedPay operations."
            }
        
        if not w3.is_address(user_address):
            return {
                "status": "error",
                "error_message": f"Invalid address format: {user_address}"
            }
        
        # Use testnet contract
        username = contract.functions.getUserByAddress(user_address).call()
        
        if not username:
            return {
                "status": "error",
                "error_message": f"No username registered for address {user_address} on testnet"
            }
        
        return {
            "status": "success",
            "report": f"Address {user_address} is registered with username: '{username}' on testnet",
            "address": user_address,
            "username": username,
            "network": "testnet",
            "contract_address": PROTECTEDPAY_CONTRACT_ADDRESS
        }
        
        return {
            "status": "success",
            "report": f"Address {user_address} is registered with username: '{username}' on {selected_network}",
            "address": user_address,
            "username": username,
            "network": selected_network,
            "contract_address": contract_address
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error looking up address {user_address}: {str(e)}"
        }

def get_user_transfers(user_address: str, network: Optional[str] = None) -> dict:
    """Get all transfers for a specific user address (testnet only).

    Args:
        user_address (str): The user's wallet address
        network (str): Network to use (must be "testnet" or None)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Only testnet is supported
        if network is not None and network.lower() != "testnet":
            return {
                "status": "error",
                "error_message": "Only testnet is supported for ProtectedPay operations."
            }
        
        if not w3.is_address(user_address):
            return {
                "status": "error",
                "error_message": f"Invalid address format: {user_address}"
            }
        
        # Use testnet contract
        transfers = contract.functions.getUserTransfers(user_address).call()
        
        if not transfers:
            return {
                "status": "success",
                "report": f"No transfers found for address {user_address} on testnet",
                "transfers": [],
                "network": "testnet",
                "contract_address": PROTECTEDPAY_CONTRACT_ADDRESS
            }
        
        transfer_list = []
        status_map = {0: "Pending", 1: "Completed", 2: "Cancelled"}
        
        for transfer in transfers:
            transfer_list.append({
                "sender": transfer[0],
                "recipient": transfer[1], 
                "amount_wei": transfer[2],
                "amount_bnb": w3.from_wei(transfer[2], 'ether'),
                "timestamp": transfer[3],
                "status": status_map.get(transfer[4], "Unknown"),
                "remarks": transfer[5]
            })
        
        return {
            "status": "success",
            "report": f"Found {len(transfer_list)} transfers for address {user_address} on testnet",
            "transfers": transfer_list,
            "count": len(transfer_list),
            "network": "testnet",
            "contract_address": PROTECTEDPAY_CONTRACT_ADDRESS
        }
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Error fetching transfers for {user_address}: {str(e)}"
        }

def create_group_payment(payment_id: str, recipient_address: str, num_participants: int, remarks: str, total_amount_bnb: str, creator_address: str, network: Optional[str] = None) -> dict:
    """Create a group payment (testnet only).

    Args:
        payment_id (str): Unique payment ID (32-byte hex string)
        recipient_address (str): The recipient's wallet address
        num_participants (int): Number of participants expected
        remarks (str): Payment description
        total_amount_bnb (str): Total amount in BNB
        creator_address (str): The creator's wallet address
        network (str): Network to use (must be "testnet" or None)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Only testnet is supported
        if network is not None and network.lower() != "testnet":
            return {
                "status": "error",
                "error_message": "Only testnet is supported for ProtectedPay operations."
            }
        
        if not w3.is_address(recipient_address):
            return {
                "status": "error",
                "error_message": f"Invalid recipient address: {recipient_address}"
            }
        
        if not w3.is_address(creator_address):
            return {
                "status": "error",
                "error_message": f"Invalid creator address: {creator_address}"
            }
        
        # Convert payment_id to bytes32 if it's a string
        if payment_id.startswith('0x'):
            payment_id_bytes = bytes.fromhex(payment_id[2:])
        else:
            payment_id_bytes = payment_id.encode('utf-8')[:32].ljust(32, b'\0')
        
        total_amount_wei = w3.to_wei(float(total_amount_bnb), 'ether')
        
        # Execute transaction on testnet
        
        # Execute the transaction
        tx_result = execute_contract_transaction(
            contract=contract,
            function_name="createGroupPayment", 
            params={
                "_recipient": recipient_address,
                "_numParticipants": num_participants,
                "_remarks": remarks
            },
            value_wei=total_amount_wei,
            network="testnet",
            network_w3=w3
        )
        
        if tx_result["status"] == "success":
            tx_result["report"] = f"Successfully created group payment with ID {payment_id} for {total_amount_bnb} BNB to {recipient_address} with {num_participants} participants on testnet"
            tx_result["payment_id"] = payment_id
            tx_result["recipient"] = recipient_address
            tx_result["num_participants"] = num_participants
            tx_result["total_amount_bnb"] = total_amount_bnb
            tx_result["remarks"] = remarks
        
        return tx_result
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing group payment: {str(e)}"
        }

def create_savings_pot(pot_id: str, name: str, target_amount_bnb: str, remarks: str, creator_address: str, network: Optional[str] = None) -> dict:
    """Create a savings pot (testnet only).

    Args:
        pot_id (str): Unique pot ID (32-byte hex string)
        name (str): Name of the savings pot
        target_amount_bnb (str): Target amount in BNB
        remarks (str): Pot description
        creator_address (str): The creator's wallet address
        network (str): Network to use (must be "testnet" or None)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Only testnet is supported
        if network is not None and network.lower() != "testnet":
            return {
                "status": "error",
                "error_message": "Only testnet is supported for ProtectedPay operations."
            }
        
        if not w3.is_address(creator_address):
            return {
                "status": "error",
                "error_message": f"Invalid creator address: {creator_address}"
            }
        
        # Convert pot_id to bytes32 if it's a string  
        if pot_id.startswith('0x'):
            pot_id_bytes = bytes.fromhex(pot_id[2:])
        else:
            pot_id_bytes = pot_id.encode('utf-8')[:32].ljust(32, b'\0')
        
        target_amount_wei = w3.to_wei(float(target_amount_bnb), 'ether')
        
        # Execute the transaction on testnet
        tx_result = execute_contract_transaction(
            contract=contract,
            function_name="createSavingsPot", 
            params={
                "_name": name,
                "_targetAmount": target_amount_wei,
                "_remarks": remarks
            },
            value_wei=0,  # No value needed for creating savings pot
            network="testnet",
            network_w3=w3
        )
        
        if tx_result["status"] == "success":
            tx_result["report"] = f"Successfully created savings pot '{name}' with target {target_amount_bnb} BNB on testnet"
            tx_result["pot_id"] = pot_id
            tx_result["pot_name"] = name
            tx_result["target_amount_bnb"] = target_amount_bnb
            tx_result["remarks"] = remarks
        
        return tx_result
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing savings pot creation: {str(e)}"
        }

def convert_eth_wei(amount: str, conversion_type: str) -> dict:
    """Converts between ETH and Wei using web3.py utilities.

    Args:
        amount (str): The amount to convert (as string to handle large numbers)
        conversion_type (str): Either 'eth_to_wei' or 'wei_to_eth'

    Returns:
        dict: status and result or error msg.
    """
    try:
        amount = amount.strip()
        conversion_type = conversion_type.lower().strip()
        
        if conversion_type == 'eth_to_wei':
            # Convert ETH to Wei
            eth_amount = float(amount)
            wei_amount = Web3.to_wei(eth_amount, 'ether')
            
            return {
                "status": "success",
                "report": f"{eth_amount} ETH = {wei_amount:,} Wei",
                "original_amount": eth_amount,
                "converted_amount": wei_amount,
                "original_unit": "ETH",
                "converted_unit": "Wei"
            }
            
        elif conversion_type == 'wei_to_eth':
            # Convert Wei to ETH
            wei_amount = int(amount)
            eth_amount = Web3.from_wei(wei_amount, 'ether')
            
            return {
                "status": "success",
                "report": f"{wei_amount:,} Wei = {eth_amount} ETH",
                "original_amount": wei_amount,
                "converted_amount": float(eth_amount),
                "original_unit": "Wei",
                "converted_unit": "ETH"
            }
        else:
            return {
                "status": "error",
                "error_message": "Invalid conversion type. Use 'eth_to_wei' or 'wei_to_eth'"
            }
            
    except ValueError as e:
        return {
            "status": "error",
            "error_message": f"Invalid amount format: {amount}. Please provide a valid number."
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Conversion error: {str(e)}"
        }

def validate_ethereum_address(address: str) -> dict:
    """Validates if a given string is a valid Ethereum address.

    Args:
        address (str): The address to validate

    Returns:
        dict: status and result or error msg.
    """
    try:
        address = address.strip()
        
        # Check if it's a valid Ethereum address
        is_valid = Web3.is_address(address)
        
        if is_valid:
            # Check if it's checksummed
            is_checksummed = Web3.is_checksum_address(address)
            checksum_address = Web3.to_checksum_address(address)
            
            return {
                "status": "success",
                "report": f"Address {address} is valid. Checksummed: {is_checksummed}",
                "is_valid": True,
                "is_checksummed": is_checksummed,
                "checksum_address": checksum_address,
                "original_address": address
            }
        else:
            return {
                "status": "error",
                "error_message": f"Invalid Ethereum address: {address}",
                "is_valid": False
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Address validation error: {str(e)}",
            "is_valid": False
        }

def calculate_gas_cost(gas_limit: str, gas_price_gwei: str) -> dict:
    """Calculates the total gas cost in ETH for a transaction.

    Args:
        gas_limit (str): The gas limit for the transaction
        gas_price_gwei (str): The gas price in Gwei

    Returns:
        dict: status and result or error msg.
    """
    try:
        gas_limit = int(gas_limit.strip())
        gas_price_gwei = float(gas_price_gwei.strip())
        
        # Convert Gwei to Wei
        gas_price_wei = Web3.to_wei(gas_price_gwei, 'gwei')
        
        # Calculate total gas cost in Wei
        total_gas_wei = gas_limit * gas_price_wei
        
        # Convert to ETH
        total_gas_eth = Web3.from_wei(total_gas_wei, 'ether')
        
        return {
            "status": "success",
            "report": f"Gas Cost: {gas_limit:,} gas × {gas_price_gwei} Gwei = {total_gas_eth} ETH ({total_gas_wei:,} Wei)",
            "gas_limit": gas_limit,
            "gas_price_gwei": gas_price_gwei,
            "gas_price_wei": gas_price_wei,
            "total_cost_wei": total_gas_wei,
            "total_cost_eth": float(total_gas_eth)
        }
        
    except ValueError as e:
        return {
            "status": "error",
            "error_message": f"Invalid input format. Please provide valid numbers for gas limit and gas price."
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Gas calculation error: {str(e)}"
        }


def get_bnb_balance(address: str, network: str = "testnet") -> dict:
    """Get BNB balance for an address on BNB Smart Chain Testnet.

    Args:
        address (str): The wallet address to check balance for
        network (str): Must be "testnet" (default: testnet)

    Returns:
        dict: status and result or error msg.
    """
    try:
        address = address.strip()
        network = network.lower().strip()
        
        # Validate address format
        if not Web3.is_address(address):
            return {
                "status": "error",
                "error_message": f"Invalid address format: {address}"
            }
        
        # Validate network - only testnet supported
        if network != "testnet":
            return {
                "status": "error",
                "error_message": f"Only testnet is supported. Got: {network}"
            }
        
        # Use testnet configuration
        network_w3 = w3
        
        # Check connection
        if not network_w3.is_connected():
            return {
                "status": "error",
                "error_message": f"Unable to connect to BNB Smart Chain Testnet at {BNB_TESTNET_RPC}"
            }
        
        # Get balance in Wei
        balance_wei = network_w3.eth.get_balance(address)
        
        # Convert to BNB (ETH units)
        balance_bnb = Web3.from_wei(balance_wei, 'ether')
        
        # Get checksummed address
        checksum_address = Web3.to_checksum_address(address)
        
        return {
            "status": "success",
            "report": f"Balance on BNB Smart Chain Testnet: {balance_bnb} tBNB",
            "address": checksum_address,
            "network": "BNB Smart Chain Testnet",
            "chain_id": 97,
            "balance_wei": balance_wei,
            "balance_bnb": float(balance_bnb),
            "currency_symbol": "tBNB",
            "rpc_url": BNB_TESTNET_RPC
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching balance for {address} on {network}: {str(e)}"
        }

def get_multiple_balances(address: str) -> dict:
    """Get BNB balance for an address on BNB Smart Chain Testnet.

    Args:
        address (str): The wallet address to check balance for

    Returns:
        dict: status and result for testnet or error msg.
    """
    try:
        address = address.strip()
        
        # Validate address format
        if not Web3.is_address(address):
            return {
                "status": "error",
                "error_message": f"Invalid address format: {address}"
            }
        
        checksum_address = Web3.to_checksum_address(address)
        
        # Get balance on testnet only
        balance_result = get_bnb_balance(address, "testnet")
        
        if balance_result["status"] == "success":
            report = f"Balance for {checksum_address} on Testnet: {balance_result['balance_bnb']} tBNB"
            
            return {
                "status": "success",
                "report": report,
                "address": checksum_address,
                "balances": {"testnet": balance_result}
            }
        else:
            return {
                "status": "error",
                "error_message": f"Failed to fetch balance on testnet for {checksum_address}: {balance_result['error_message']}",
                "address": checksum_address,
                "balances": {"testnet": balance_result}
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching balances for {address}: {str(e)}"
        }


def claim_transfer_by_id(transfer_id: int, claimer_address: str) -> dict:
    """Claim a transfer by its ID.

    Args:
        transfer_id (int): The transfer ID to claim
        claimer_address (str): The claimer's wallet address

    Returns:
        dict: status and result or error msg.
    """
    try:
        if not w3.is_address(claimer_address):
            return {
                "status": "error",
                "error_message": f"Invalid claimer address: {claimer_address}"
            }
        
        return {
            "status": "success",
            "report": f"To claim transfer ID {transfer_id}, call contract function 'claimTransferById'",
            "function": "claimTransferById",
            "params": {
                "_transferId": transfer_id
            },
            "from_address": claimer_address
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing claim transfer by ID: {str(e)}"
        }

def claim_transfer_by_username(username: str, claimer_address: str) -> dict:
    """Claim a transfer by username.

    Args:
        username (str): The username to claim transfers for
        claimer_address (str): The claimer's wallet address

    Returns:
        dict: status and result or error msg.
    """
    try:
        if not w3.is_address(claimer_address):
            return {
                "status": "error",
                "error_message": f"Invalid claimer address: {claimer_address}"
            }
        
        return {
            "status": "success",
            "report": f"To claim transfers for username '{username}', call contract function 'claimTransferByUsername'",
            "function": "claimTransferByUsername",
            "params": {
                "_username": username
            },
            "from_address": claimer_address
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing claim transfer by username: {str(e)}"
        }

def contribute_to_group_payment(payment_id: str, contribution_bnb: str, contributor_address: str) -> dict:
    """Contribute to a group payment.

    Args:
        payment_id (str): The group payment ID
        contribution_bnb (str): Amount to contribute in BNB
        contributor_address (str): The contributor's wallet address

    Returns:
        dict: status and result or error msg.
    """
    try:
        if not w3.is_address(contributor_address):
            return {
                "status": "error",
                "error_message": f"Invalid contributor address: {contributor_address}"
            }
        
        # Convert payment_id to bytes32 if it's a string
        if payment_id.startswith('0x'):
            payment_id_bytes = bytes.fromhex(payment_id[2:])
        else:
            payment_id_bytes = payment_id.encode('utf-8')[:32].ljust(32, b'\0')
        
        contribution_wei = w3.to_wei(float(contribution_bnb), 'ether')
        
        # Get contract instance for the selected network
        contract, network_w3 = get_contract_for_network("testnet")  # Using testnet for now since mainnet is not deployed
        
        # Execute the transaction
        tx_result = execute_contract_transaction(
            contract=contract,
            function_name="contributeToGroupPayment", 
            params={
                "_paymentId": payment_id_bytes.hex()
            },
            value_wei=contribution_wei,
            network="testnet",
            network_w3=network_w3
        )
        
        if tx_result["status"] == "success":
            tx_result["report"] = f"Successfully contributed {contribution_bnb} BNB to group payment {payment_id}"
            tx_result["payment_id"] = payment_id
            tx_result["contribution_bnb"] = contribution_bnb
        
        return tx_result
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing group payment contribution: {str(e)}"
        }

def contribute_to_savings_pot(pot_id: str, contribution_bnb: str, contributor_address: str) -> dict:
    """Contribute to a savings pot.

    Args:
        pot_id (str): The savings pot ID
        contribution_bnb (str): Amount to contribute in BNB
        contributor_address (str): The contributor's wallet address

    Returns:
        dict: status and result or error msg.
    """
    try:
        if not w3.is_address(contributor_address):
            return {
                "status": "error",
                "error_message": f"Invalid contributor address: {contributor_address}"
            }
        
        # Convert pot_id to bytes32 if it's a string
        if pot_id.startswith('0x'):
            pot_id_bytes = bytes.fromhex(pot_id[2:])
        else:
            pot_id_bytes = pot_id.encode('utf-8')[:32].ljust(32, b'\0')
        
        contribution_wei = w3.to_wei(float(contribution_bnb), 'ether')
        
        # Get contract instance for the selected network
        contract, network_w3 = get_contract_for_network("testnet")  # Using testnet for now since mainnet is not deployed
        
        # Execute the transaction
        tx_result = execute_contract_transaction(
            contract=contract,
            function_name="contributeToSavingsPot", 
            params={
                "_potId": pot_id_bytes.hex()
            },
            value_wei=contribution_wei,
            network="testnet",
            network_w3=network_w3
        )
        
        if tx_result["status"] == "success":
            tx_result["report"] = f"Successfully contributed {contribution_bnb} BNB to savings pot {pot_id}"
            tx_result["pot_id"] = pot_id
            tx_result["contribution_bnb"] = contribution_bnb
        
        return tx_result
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing savings pot contribution: {str(e)}"
        }

def refund_transfer(transfer_id: int, sender_address: str) -> dict:
    """Refund a transfer by its ID (only the sender can refund).

    Args:
        transfer_id (int): The transfer ID to refund
        sender_address (str): The sender's wallet address (must be the original sender)

    Returns:
        dict: status and result or error msg.
    """
    try:
        if not w3.is_address(sender_address):
            return {
                "status": "error",
                "error_message": f"Invalid sender address: {sender_address}"
            }
        
        return {
            "status": "success",
            "report": f"To refund transfer ID {transfer_id}, call contract function 'refundTransfer' (only original sender can refund)",
            "function": "refundTransfer",
            "params": {
                "_transferId": transfer_id
            },
            "from_address": sender_address
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing transfer refund: {str(e)}"
        }


root_agent = Agent(
    name="crypto_web3_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about cryptocurrency prices, ETH/Wei conversions, address validation, and gas calculations."
    ),
    instruction=(
        "You are a helpful agent specialized in cryptocurrency and blockchain operations. You can:\n"
        "1. Fetch current cryptocurrency prices in USD using the Coinbase API\n"
        "2. Convert between ETH and Wei using web3.py utilities\n"
        "3. Validate Ethereum addresses and provide checksummed versions\n"
        "4. Calculate gas costs for Ethereum transactions\n\n"
        "You can handle various token symbols like BTC, ETH, BNB, USDC, USDT, and many others. "
        "You can also understand common token names like 'bitcoin' for BTC, 'ethereum' for ETH, 'bnb' for BNB, etc. "
        "For web3 operations, always provide clear explanations of the conversions and calculations.\n\n"
        "5. Manage private keys and execute transactions:\n"
        "- Set private key for transaction signing\n"
        "- Get wallet information and address\n"
        "- Clear private key for security\n"
        "- Execute actual blockchain transactions (not just simulate them)\n\n"
        "6. Interact with the ProtectedPay smart contract on BNB Smart Chain Testnet and Mainnet:\n"
        "- Set network preference (testnet/mainnet) - will remember your choice\n"
        "- Register usernames (executes transaction)\n"
        "- Send BNB to addresses or usernames (executes transaction)\n" 
        "- Look up users by username or address\n"
        "- Get user transfer history\n"
        "- Create and manage group payments (executes transaction)\n"
        "- Create and manage savings pots (executes transaction)\n"
        "- Claim transfers, contribute to payments/pots, and handle refunds (executes transaction)\n"
        "- Note: Mainnet contract is not yet deployed (using 0x0 address)\n\n"
        "7. Check BNB balances:\n"
        "- Get BNB balance on BNB Smart Chain Testnet or Mainnet for any address\n"
        "- Compare balances across both networks\n"
        "- Validate addresses and provide checksummed versions\n\n"
        "IMPORTANT: For write operations (transfers, registrations, etc.), you need to set a private key first using set_private_key(). The agent will then execute actual blockchain transactions and return transaction hashes and receipts."
    ),
    tools=[
        get_token_price, 
        convert_eth_wei, 
        validate_ethereum_address, 
        calculate_gas_cost,
        get_bnb_balance,
        get_multiple_balances,
        set_user_network_preference,
        get_user_network_preference,
        set_private_key,
        get_wallet_info,
        clear_private_key,
        explain_protectedpay_networks,
        register_username,
        send_to_address,
        send_to_username,
        get_user_by_username,
        get_user_by_address,
        get_user_transfers,
        create_group_payment,
        create_savings_pot,
        claim_transfer_by_id,
        claim_transfer_by_username,
        contribute_to_group_payment,
        contribute_to_savings_pot,
        refund_transfer
    ],
)