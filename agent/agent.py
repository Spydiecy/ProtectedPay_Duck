import os
import requests
from web3 import Web3
from google.adk.agents import Agent
from typing import Dict, Any, List

# Sei Network configurations
SEI_TESTNET_RPC = "https://evm-rpc-testnet.sei-apis.com"
SEI_MAINNET_RPC = "https://evm-rpc.sei-apis.com"

# ProtectedPay contract addresses for different networks
PROTECTEDPAY_CONTRACTS = {
    "testnet": "0x6bDda54ee2Fb802aC85E88B2cBE4B93767Ef8D1e",
    "mainnet": "0x0000000000000000000000000000000000000000"
}

# Initialize Web3 (default to testnet)
w3 = Web3(Web3.HTTPProvider(SEI_TESTNET_RPC))

# User session state to remember network preference
user_network_preference = None

# Network configurations for balance checking
NETWORK_CONFIG = {
    "testnet": {
        "rpc_url": SEI_TESTNET_RPC,
        "name": "Sei Testnet",
        "chain_id": 1328,
        "currency_symbol": "SEI"
    },
    "mainnet": {
        "rpc_url": SEI_MAINNET_RPC,
        "name": "Sei Mainnet", 
        "chain_id": 1329,
        "currency_symbol": "SEI"
    }
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
        "name": "contributeToPot",
        "outputs": [],
        "stateMutability": "payable",
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
                "internalType": "bytes32",
                "name": "_potId",
                "type": "bytes32"
            },
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
                "name": "_user",
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
    }
]

# Initialize contract (default to testnet)
def get_contract_for_network(network: str = "testnet"):
    """Get contract instance for specified network."""
    if network not in PROTECTEDPAY_CONTRACTS:
        raise ValueError(f"Invalid network: {network}")
    
    rpc_url = SEI_TESTNET_RPC if network == "testnet" else SEI_MAINNET_RPC
    network_w3 = Web3(Web3.HTTPProvider(rpc_url))
    contract_address = PROTECTEDPAY_CONTRACTS[network]
    
    return network_w3.eth.contract(address=contract_address, abi=CONTRACT_ABI), network_w3

# Default contract for testnet
contract, _ = get_contract_for_network("testnet")

def set_user_network_preference(network: str) -> dict:
    """Set the user's preferred network for ProtectedPay transactions.
    
    Args:
        network (str): Either "testnet" or "mainnet"
        
    Returns:
        dict: status and result or error msg.
    """
    global user_network_preference
    
    try:
        network = network.lower().strip()
        
        if network not in ["testnet", "mainnet"]:
            return {
                "status": "error",
                "error_message": "Invalid network. Please choose 'testnet' or 'mainnet'"
            }
        
        user_network_preference = network
        
        if network == "mainnet":
            return {
                "status": "success",
                "report": f"Network preference set to {network}. Note: Mainnet ProtectedPay contract is not yet deployed (using 0x0 address)",
                "network": network,
                "contract_address": PROTECTEDPAY_CONTRACTS[network]
            }
        else:
            return {
                "status": "success", 
                "report": f"Network preference set to {network}",
                "network": network,
                "contract_address": PROTECTEDPAY_CONTRACTS[network]
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error setting network preference: {str(e)}"
        }

def get_user_network_preference() -> dict:
    """Get the current user's network preference.
    
    Returns:
        dict: status and current network preference.
    """
    global user_network_preference
    
    if user_network_preference is None:
        return {
            "status": "no_preference",
            "report": "No network preference set. Please specify 'testnet' or 'mainnet' for ProtectedPay transactions.",
            "network": None
        }
    
    return {
        "status": "success",
        "report": f"Current network preference: {user_network_preference}",
        "network": user_network_preference,
        "contract_address": PROTECTEDPAY_CONTRACTS[user_network_preference]
    }

def check_network_for_transaction(specified_network: str = None) -> dict:
    """Check which network to use for a transaction.
    
    Args:
        specified_network (str): Network specified in current request (optional)
        
    Returns:
        dict: status and network to use, or request for network specification.
    """
    global user_network_preference
    
    # If network is specified in current request, use it and remember it
    if specified_network:
        specified_network = specified_network.lower().strip()
        if specified_network not in ["testnet", "mainnet"]:
            return {
                "status": "error",
                "error_message": "Invalid network specified. Please choose 'testnet' or 'mainnet'"
            }
        
        user_network_preference = specified_network
        return {
            "status": "success",
            "network": specified_network,
            "contract_address": PROTECTEDPAY_CONTRACTS[specified_network]
        }
    
    # If user has a saved preference, use it
    if user_network_preference:
        return {
            "status": "success", 
            "network": user_network_preference,
            "contract_address": PROTECTEDPAY_CONTRACTS[user_network_preference]
        }
    
    # No preference set and no network specified
    return {
        "status": "need_network",
        "error_message": "Please specify which network to use: 'testnet' or 'mainnet'",
        "available_networks": ["testnet", "mainnet"]
    }

def explain_protectedpay_networks() -> dict:
    """Explains the status of ProtectedPay contract on different Sei networks.
    
    Returns:
        dict: Information about ProtectedPay contract deployment status
    """
    return {
        "status": "success",
        "report": "ProtectedPay Network Status:\n\n" +
                  "🧪 SEI TESTNET:\n" +
                  f"- Contract Address: {PROTECTEDPAY_CONTRACTS['testnet']}\n" +
                  "- Status: FULLY DEPLOYED ✅\n" +
                  "- Features: All ProtectedPay functions available (usernames, transfers, group payments, savings pots)\n\n" +
                  "🌐 SEI MAINNET:\n" +
                  f"- Contract Address: {PROTECTEDPAY_CONTRACTS['mainnet']} (placeholder)\n" +
                  "- Status: NOT YET DEPLOYED ⚠️\n" +
                  "- Features: Only balance checking available, no ProtectedPay features\n\n" +
                  "📝 Important Notes:\n" +
                  "- Usernames registered on testnet are NOT available on mainnet\n" +
                  "- Each network has separate user registrations and transaction history\n" +
                  "- For ProtectedPay features, please use testnet until mainnet deployment",
        "testnet_contract": PROTECTEDPAY_CONTRACTS['testnet'],
        "mainnet_contract": PROTECTEDPAY_CONTRACTS['mainnet'],
        "testnet_status": "deployed",
        "mainnet_status": "not_deployed"
    }

def get_token_price(token_symbol: str) -> dict:
    """Retrieves the current price of a cryptocurrency token in USD.

    Args:
        token_symbol (str): The symbol of the cryptocurrency token (e.g., 'BTC', 'ETH', 'SEI').

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Convert common token names to symbols
        token_mappings = {
            'bitcoin': 'BTC',
            'ethereum': 'ETH',
            'sei': 'SEI',
            'usdc': 'USDC',
            'usdt': 'USDT',
            'bnb': 'BNB',
            'cardano': 'ADA',
            'solana': 'SOL',
            'polkadot': 'DOT',
            'chainlink': 'LINK',
            'litecoin': 'LTC',
            'dogecoin': 'DOG',
            'sei': 'SEI' 
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

def register_username(username: str, user_address: str, network: str = None) -> dict:
    """Register a username for a user address on ProtectedPay.

    Args:
        username (str): The username to register
        user_address (str): The user's wallet address
        network (str): Network to use ("testnet" or "mainnet", optional if preference set)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Check which network to use
        network_check = check_network_for_transaction(network)
        if network_check["status"] == "need_network":
            return network_check
        elif network_check["status"] == "error":
            return network_check
        
        selected_network = network_check["network"]
        contract_address = network_check["contract_address"]
        
        if not w3.is_address(user_address):
            return {
                "status": "error",
                "error_message": f"Invalid address format: {user_address}"
            }
        
        # Check if mainnet contract is available
        if selected_network == "mainnet" and contract_address == "0x0000000000000000000000000000000000000000":
            return {
                "status": "error",
                "error_message": "ProtectedPay contract is not yet deployed on mainnet. Please use testnet for now."
            }
        
        return {
            "status": "success",
            "report": f"To register username '{username}' for address {user_address} on {selected_network}, call contract function 'registerUsername'",
            "function": "registerUsername",
            "params": {"username": username},
            "from_address": user_address,
            "network": selected_network,
            "contract_address": contract_address
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing username registration: {str(e)}"
        }

def send_to_address(recipient_address: str, amount_sei: str, remarks: str, sender_address: str, network: str = None) -> dict:
    """Send SEI tokens to a specific address.

    Args:
        recipient_address (str): The recipient's wallet address
        amount_sei (str): Amount of SEI to send
        remarks (str): Message or remarks for the transfer
        sender_address (str): The sender's wallet address
        network (str): Network to use ("testnet" or "mainnet", optional if preference set)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Check which network to use
        network_check = check_network_for_transaction(network)
        if network_check["status"] == "need_network":
            return network_check
        elif network_check["status"] == "error":
            return network_check
        
        selected_network = network_check["network"]
        contract_address = network_check["contract_address"]
        
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
        
        # Check if mainnet contract is available
        if selected_network == "mainnet" and contract_address == "0x0000000000000000000000000000000000000000":
            return {
                "status": "error",
                "error_message": "ProtectedPay contract is not yet deployed on mainnet. Please use testnet for now."
            }
        
        amount_wei = w3.to_wei(float(amount_sei), 'ether')
        
        return {
            "status": "success",
            "report": f"To send {amount_sei} SEI to {recipient_address} with message '{remarks}' on {selected_network}, call contract function 'sendToAddress'",
            "function": "sendToAddress",
            "params": {
                "_recipient": recipient_address,
                "_remarks": remarks
            },
            "value": amount_wei,
            "from_address": sender_address,
            "amount_sei": amount_sei,
            "network": selected_network,
            "contract_address": contract_address
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing send transaction: {str(e)}"
        }

def send_to_username(username: str, amount_sei: str, remarks: str, sender_address: str, network: str = None) -> dict:
    """Send SEI tokens to a user by their username.

    Args:
        username (str): The recipient's username
        amount_sei (str): Amount of SEI to send
        remarks (str): Message or remarks for the transfer
        sender_address (str): The sender's wallet address
        network (str): Network to use ("testnet" or "mainnet", optional if preference set)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Check which network to use
        network_check = check_network_for_transaction(network)
        if network_check["status"] == "need_network":
            return network_check
        elif network_check["status"] == "error":
            return network_check
        
        selected_network = network_check["network"]
        contract_address = network_check["contract_address"]
        
        if not w3.is_address(sender_address):
            return {
                "status": "error",
                "error_message": f"Invalid sender address: {sender_address}"
            }
        
        # Check if mainnet contract is available
        if selected_network == "mainnet" and contract_address == "0x0000000000000000000000000000000000000000":
            return {
                "status": "error",
                "error_message": "ProtectedPay contract is not yet deployed on mainnet. Please use testnet for now."
            }
        
        amount_wei = w3.to_wei(float(amount_sei), 'ether')
        
        return {
            "status": "success",
            "report": f"To send {amount_sei} SEI to username '{username}' with message '{remarks}' on {selected_network}, call contract function 'sendToUsername'",
            "function": "sendToUsername",
            "params": {
                "_username": username,
                "_remarks": remarks
            },
            "value": amount_wei,
            "from_address": sender_address,
            "amount_sei": amount_sei,
            "network": selected_network,
            "contract_address": contract_address
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing send to username transaction: {str(e)}"
        }

def get_user_by_username(username: str, network: str = None) -> dict:
    """Get the address associated with a username.

    Args:
        username (str): The username to look up
        network (str): Network to use ("testnet" or "mainnet", optional if preference set)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Check which network to use
        network_check = check_network_for_transaction(network)
        if network_check["status"] == "need_network":
            return network_check
        elif network_check["status"] == "error":
            return network_check
        
        selected_network = network_check["network"]
        contract_address = network_check["contract_address"]
        
        # Check if mainnet contract is available
        if selected_network == "mainnet" and contract_address == "0x0000000000000000000000000000000000000000":
            return {
                "status": "error",
                "error_message": f"ProtectedPay contract is not yet deployed on mainnet (using placeholder address 0x0). Username lookups are only available on testnet. Please use testnet or wait for mainnet deployment."
            }
        
        # Get contract instance for the selected network
        network_contract, _ = get_contract_for_network(selected_network)
        
        address = network_contract.functions.getUserByUsername(username).call()
        
        if address == "0x0000000000000000000000000000000000000000":
            return {
                "status": "error",
                "error_message": f"Username '{username}' is not registered on {selected_network}"
            }
        
        return {
            "status": "success",
            "report": f"Username '{username}' is registered to address: {address} on {selected_network}",
            "username": username,
            "address": address,
            "network": selected_network,
            "contract_address": contract_address
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error looking up username '{username}': {str(e)}"
        }

def get_user_by_address(user_address: str, network: str = None) -> dict:
    """Get the username associated with an address.

    Args:
        user_address (str): The wallet address to look up
        network (str): Network to use ("testnet" or "mainnet", optional if preference set)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Check which network to use
        network_check = check_network_for_transaction(network)
        if network_check["status"] == "need_network":
            return network_check
        elif network_check["status"] == "error":
            return network_check
        
        selected_network = network_check["network"]
        contract_address = network_check["contract_address"]
        
        if not w3.is_address(user_address):
            return {
                "status": "error",
                "error_message": f"Invalid address format: {user_address}"
            }
        
        # Check if mainnet contract is available
        if selected_network == "mainnet" and contract_address == "0x0000000000000000000000000000000000000000":
            return {
                "status": "error",
                "error_message": "ProtectedPay contract is not yet deployed on mainnet. Please use testnet for now."
            }
        
        # Get contract instance for the selected network
        network_contract, _ = get_contract_for_network(selected_network)
        
        username = network_contract.functions.getUserByAddress(user_address).call()
        
        if not username:
            return {
                "status": "error",
                "error_message": f"No username registered for address {user_address} on {selected_network}"
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

def get_user_transfers(user_address: str, network: str = None) -> dict:
    """Get all transfers for a specific user address.

    Args:
        user_address (str): The user's wallet address
        network (str): Network to use ("testnet" or "mainnet", optional if preference set)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Check which network to use
        network_check = check_network_for_transaction(network)
        if network_check["status"] == "need_network":
            return network_check
        elif network_check["status"] == "error":
            return network_check
        
        selected_network = network_check["network"]
        contract_address = network_check["contract_address"]
        
        if not w3.is_address(user_address):
            return {
                "status": "error",
                "error_message": f"Invalid address format: {user_address}"
            }
        
        # Check if mainnet contract is available
        if selected_network == "mainnet" and contract_address == "0x0000000000000000000000000000000000000000":
            return {
                "status": "error",
                "error_message": "ProtectedPay contract is not yet deployed on mainnet. Please use testnet for now."
            }
        
        # Get contract instance for the selected network
        network_contract, network_w3 = get_contract_for_network(selected_network)
        
        transfers = network_contract.functions.getUserTransfers(user_address).call()
        
        if not transfers:
            return {
                "status": "success",
                "report": f"No transfers found for address {user_address} on {selected_network}",
                "transfers": [],
                "network": selected_network,
                "contract_address": contract_address
            }
        
        transfer_list = []
        status_map = {0: "Pending", 1: "Completed", 2: "Cancelled"}
        
        for transfer in transfers:
            transfer_list.append({
                "sender": transfer[0],
                "recipient": transfer[1], 
                "amount_wei": transfer[2],
                "amount_sei": network_w3.from_wei(transfer[2], 'ether'),
                "timestamp": transfer[3],
                "status": status_map.get(transfer[4], "Unknown"),
                "remarks": transfer[5]
            })
        
        return {
            "status": "success",
            "report": f"Found {len(transfer_list)} transfers for address {user_address} on {selected_network}",
            "transfers": transfer_list,
            "count": len(transfer_list),
            "network": selected_network,
            "contract_address": contract_address
        }
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Error fetching transfers for {user_address}: {str(e)}"
        }

def create_group_payment(payment_id: str, recipient_address: str, num_participants: int, remarks: str, total_amount_sei: str, creator_address: str, network: str = None) -> dict:
    """Create a group payment.

    Args:
        payment_id (str): Unique payment ID (32-byte hex string)
        recipient_address (str): The recipient's wallet address
        num_participants (int): Number of participants expected
        remarks (str): Payment description
        total_amount_sei (str): Total amount in SEI
        creator_address (str): The creator's wallet address
        network (str): Network to use ("testnet" or "mainnet", optional if preference set)

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Check which network to use
        network_check = check_network_for_transaction(network)
        if network_check["status"] == "need_network":
            return network_check
        elif network_check["status"] == "error":
            return network_check
        
        selected_network = network_check["network"]
        contract_address = network_check["contract_address"]
        
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
        
        # Check if mainnet contract is available
        if selected_network == "mainnet" and contract_address == "0x0000000000000000000000000000000000000000":
            return {
                "status": "error",
                "error_message": "ProtectedPay contract is not yet deployed on mainnet. Please use testnet for now."
            }
        
        # Convert payment_id to bytes32 if it's a string
        if payment_id.startswith('0x'):
            payment_id_bytes = bytes.fromhex(payment_id[2:])
        else:
            payment_id_bytes = payment_id.encode('utf-8')[:32].ljust(32, b'\0')
        
        total_amount_wei = w3.to_wei(float(total_amount_sei), 'ether')
        
        return {
            "status": "success",
            "report": f"To create group payment with ID {payment_id} for {total_amount_sei} SEI to {recipient_address} with {num_participants} participants on {selected_network}, call 'createGroupPayment'",
            "function": "createGroupPayment",
            "params": {
                "_paymentId": payment_id_bytes.hex(),
                "_recipient": recipient_address,
                "_numParticipants": num_participants,
                "_remarks": remarks
            },
            "value": total_amount_wei,
            "from_address": creator_address,
            "network": selected_network,
            "contract_address": contract_address
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing group payment: {str(e)}"
        }

def create_savings_pot(pot_id: str, name: str, target_amount_sei: str, remarks: str, creator_address: str, network: str = None) -> dict:
    """Create a savings pot.

    Args:
        pot_id (str): Unique pot ID (32-byte hex string)
        name (str): Name of the savings pot
        target_amount_sei (str): Target amount in SEI
        remarks (str): Pot description
        creator_address (str): The creator's wallet address

    Returns:
        dict: status and result or error msg.
    """
    try:
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
        
        target_amount_wei = w3.to_wei(float(target_amount_sei), 'ether')
        
        return {
            "status": "success",
            "report": f"To create savings pot '{name}' with target {target_amount_sei} SEI, call 'createSavingsPot'",
            "function": "createSavingsPot",
            "params": {
                "_potId": pot_id_bytes.hex(),
                "_name": name,
                "_targetAmount": target_amount_wei,
                "_remarks": remarks
            },
            "from_address": creator_address
        }
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


def get_sei_balance(address: str, network: str = "testnet") -> dict:
    """Get SEI balance for an address on Sei Testnet or Mainnet.

    Args:
        address (str): The wallet address to check balance for
        network (str): Either "testnet" or "mainnet" (default: testnet)

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
        
        # Validate network
        if network not in NETWORK_CONFIG:
            return {
                "status": "error",
                "error_message": f"Invalid network. Choose 'testnet' or 'mainnet'. Got: {network}"
            }
        
        # Get network configuration
        network_info = NETWORK_CONFIG[network]
        
        # Create Web3 instance for the specified network
        network_w3 = Web3(Web3.HTTPProvider(network_info["rpc_url"]))
        
        # Check connection
        if not network_w3.is_connected():
            return {
                "status": "error",
                "error_message": f"Unable to connect to {network_info['name']} at {network_info['rpc_url']}"
            }
        
        # Get balance in Wei
        balance_wei = network_w3.eth.get_balance(address)
        
        # Convert to SEI (ETH units)
        balance_sei = Web3.from_wei(balance_wei, 'ether')
        
        # Get checksummed address
        checksum_address = Web3.to_checksum_address(address)
        
        return {
            "status": "success",
            "report": f"Balance on {network_info['name']}: {balance_sei} {network_info['currency_symbol']}",
            "address": checksum_address,
            "network": network_info['name'],
            "chain_id": network_info['chain_id'],
            "balance_wei": balance_wei,
            "balance_sei": float(balance_sei),
            "currency_symbol": network_info['currency_symbol'],
            "rpc_url": network_info['rpc_url']
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching balance for {address} on {network}: {str(e)}"
        }

def get_multiple_balances(address: str) -> dict:
    """Get SEI balance for an address on both Testnet and Mainnet.

    Args:
        address (str): The wallet address to check balance for

    Returns:
        dict: status and results for both networks or error msg.
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
        results = {}
        
        # Get balance on both networks
        for network_name in ["testnet", "mainnet"]:
            balance_result = get_sei_balance(address, network_name)
            results[network_name] = balance_result
        
        # Check if both were successful
        testnet_success = results["testnet"]["status"] == "success"
        mainnet_success = results["mainnet"]["status"] == "success"
        
        if testnet_success and mainnet_success:
            report = f"Balances for {checksum_address}:\n"
            report += f"• Testnet: {results['testnet']['balance_sei']} SEI\n"
            report += f"• Mainnet: {results['mainnet']['balance_sei']} SEI"
            
            return {
                "status": "success",
                "report": report,
                "address": checksum_address,
                "balances": results
            }
        elif testnet_success or mainnet_success:
            # At least one succeeded
            successful_networks = [net for net, result in results.items() if result["status"] == "success"]
            failed_networks = [net for net, result in results.items() if result["status"] == "error"]
            
            report = f"Partial success for {checksum_address}:\n"
            for net in successful_networks:
                report += f"• {net.title()}: {results[net]['balance_sei']} SEI\n"
            for net in failed_networks:
                report += f"• {net.title()}: Error - {results[net]['error_message']}"
            
            return {
                "status": "partial_success",
                "report": report,
                "address": checksum_address,
                "balances": results
            }
        else:
            # Both failed
            return {
                "status": "error",
                "error_message": f"Failed to fetch balances on both networks for {checksum_address}",
                "address": checksum_address,
                "balances": results
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

def contribute_to_group_payment(payment_id: str, contribution_sei: str, contributor_address: str) -> dict:
    """Contribute to a group payment.

    Args:
        payment_id (str): The group payment ID
        contribution_sei (str): Amount to contribute in SEI
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
        
        contribution_wei = w3.to_wei(float(contribution_sei), 'ether')
        
        return {
            "status": "success",
            "report": f"To contribute {contribution_sei} SEI to group payment {payment_id}, call 'contributeToGroupPayment'",
            "function": "contributeToGroupPayment",
            "params": {
                "_paymentId": payment_id_bytes.hex()
            },
            "value": contribution_wei,
            "from_address": contributor_address,
            "contribution_sei": contribution_sei
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error preparing group payment contribution: {str(e)}"
        }

def contribute_to_savings_pot(pot_id: str, contribution_sei: str, contributor_address: str) -> dict:
    """Contribute to a savings pot.

    Args:
        pot_id (str): The savings pot ID
        contribution_sei (str): Amount to contribute in SEI
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
        
        contribution_wei = w3.to_wei(float(contribution_sei), 'ether')
        
        return {
            "status": "success",
            "report": f"To contribute {contribution_sei} SEI to savings pot {pot_id}, call 'contributeToSavingsPot'",
            "function": "contributeToSavingsPot",
            "params": {
                "_potId": pot_id_bytes.hex()
            },
            "value": contribution_wei,
            "from_address": contributor_address,
            "contribution_sei": contribution_sei
        }
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
        "You can handle various token symbols like BTC, ETH, SEI, USDC, USDT, and many others. "
        "You can also understand common token names like 'bitcoin' for BTC, 'ethereum' for ETH, etc. "
        "For web3 operations, always provide clear explanations of the conversions and calculations.\n\n"
        "5. Interact with the ProtectedPay smart contract on Sei Testnet and Mainnet:\n"
        "- Set network preference (testnet/mainnet) - will remember your choice\n"
        "- Register usernames\n"
        "- Send SEI to addresses or usernames\n" 
        "- Look up users by username or address\n"
        "- Get user transfer history\n"
        "- Create and manage group payments\n"
        "- Create and manage savings pots\n"
        "- Claim transfers, contribute to payments/pots, and handle refunds\n"
        "- Note: Mainnet contract is not yet deployed (using 0x0 address)\n\n"
        "6. Check SEI balances:\n"
        "- Get SEI balance on Sei Testnet or Mainnet for any address\n"
        "- Compare balances across both networks\n"
        "- Validate addresses and provide checksummed versions\n\n"
        "Before any ProtectedPay transaction, I will ask you to specify the network (testnet/mainnet) unless you've already told me your preference."
    ),
    tools=[
        get_token_price, 
        convert_eth_wei, 
        validate_ethereum_address, 
        calculate_gas_cost,
        get_sei_balance,
        get_multiple_balances,
        set_user_network_preference,
        get_user_network_preference,
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