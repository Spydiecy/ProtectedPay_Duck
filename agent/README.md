# ProtectedPay Agent - DuckChain

This agent provides complete interaction with the ProtectedPay smart contract on DuckChain, including both read and write operations.

## Features

### 🔑 Private Key Management
- **Set Private Key**: Store your private key securely for transaction signing
- **Get Wallet Info**: View your wallet address and status
- **Clear Private Key**: Remove stored private key for security

### 🌐 Network Management
- **Set Network Preference**: Choose DuckChain mainnet (Chain ID 5545)
- **Network Status**: Check contract deployment status on different networks

### 💰 Balance Operations
- **Check TON Balance**: Get TON balance on mainnet
- **Multi-Network Balance**: Compare balances across networks

### 📝 Username System
- **Register Username**: Register a memorable username for your wallet (executes transaction)
- **Lookup by Username**: Find wallet address associated with a username
- **Lookup by Address**: Find username associated with a wallet address

### 💸 Transfer Operations
- **Send to Address**: Transfer TON to any wallet address (executes transaction)
- **Send to Username**: Transfer TON to a registered username (executes transaction)
- **Transaction History**: View all transfers for a wallet

### 👥 Group Payments
- **Create Group Payment**: Set up a shared payment pool (executes transaction)
- **Contribute to Payment**: Add funds to an existing group payment (executes transaction)

### 🏦 Savings Pots
- **Create Savings Pot**: Create a savings goal with target amount (executes transaction)
- **Contribute to Pot**: Add funds to an existing savings pot (executes transaction)

### 🔄 Transaction Management
- **Claim Transfers**: Claim pending transfers sent to you
- **Refund Transfers**: Refund unclaimed transfers you sent

## Quick Start

### 1. Set Up Your Private Key
```python
from agent import root_agent

# Set your private key (replace with your actual key)
result = root_agent.run("Set my private key to 0x1234...")
print(result)
```

### 2. Configure Network
```python
# Set network preference (testnet recommended for testing)
result = root_agent.run("Set my network preference to testnet")
print(result)
```

### 3. Check Your Balance
```python
# Check your TON balance
result = root_agent.run("What's my TON balance?")
print(result)
```

### 4. Register a Username
```python
# Register a username (executes blockchain transaction)
result = root_agent.run("Register the username 'myusername' for my wallet")
print(result)
```

### 5. Send TON
```python
# Send TON to an address (executes blockchain transaction)
result = root_agent.run("Send 0.001 TON to 0x742d35Cc6686C8d0C5bfBf1EB96aeDB8ee03Cb8F with message 'payment for services'")
print(result)

# Send TON to a username (executes blockchain transaction)
result = root_agent.run("Send 0.001 TON to username 'alice' with message 'lunch money'")
print(result)
```

## Network Configuration

### DuckChain Mainnet
- **Chain ID**: 5545
- **Currency**: TON
- **RPC URL**: https://rpc.duckchain.io
- **Explorer**: https://duckchain.io
- **Contract**: 0xf8Bc82B8184BDd37bF0226aca6e2a81c337bA076
- **Contract**: Not yet deployed

## Security Notes

⚠️ **Important Security Considerations**:

1. **Never share your private key** or commit it to version control
2. **Use testnet for development** and testing
3. **Clear your private key** when done: `root_agent.run("Clear my private key")`
4. **Verify transaction details** before confirming
5. **Start with small amounts** when testing

## Example Usage

See `example_usage.py` for a complete example showing all major features.

## Transaction Execution

When you perform write operations (transfers, registrations, etc.), the agent will:

1. ✅ Validate all parameters
2. ✅ Check network availability
3. ✅ Build the transaction
4. ✅ Sign with your private key
5. ✅ Send to the blockchain
6. ✅ Wait for confirmation
7. ✅ Return transaction hash and receipt

## Error Handling

The agent provides detailed error messages for common issues:
- Invalid addresses
- Insufficient balance
- Network connectivity problems
- Contract interaction errors
- Invalid private keys

## Support

For questions or issues:
- Check the transaction on the block explorer using the returned transaction hash
- Ensure you have sufficient TON for gas fees on mainnet
- Verify your private key is correct and has the necessary permissions
