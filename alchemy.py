#!/usr/bin/env python

import os
import subprocess
import json
import requests

# Replace with your Alchemy API key
ALCHEMY_API_KEY = "29nzuCqD2p0bmSrmn_vr50peUq-pQmjy"

# Function to generate a crypto private key
def generate_private_key():
    private_key = subprocess.check_output(["openssl", "rand", "-hex", "32"]).decode("utf-8").strip()
    return private_key

# Function to derive wallet address from private key
def derive_wallet_address(private_key):
    from eth_account import Account
    account = Account.from_key(private_key)
    return account.address

# Function to check balance of a wallet address using Alchemy API (for Ethereum)
def check_wallet_balance(wallet_address):
    url = f"https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"jsonrpc": "2.0", "method": "eth_getBalance", "params": [wallet_address, "latest"], "id": 1}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    response_json = response.json()
    if "error" in response_json:
        raise Exception(f"Alchemy API error - {response_json['error']}")
    return int(response_json["result"], 16)

# Main script logic
print("Generating crypto private key and checking wallet balance...")

while True:
    private_key = generate_private_key()
    print(f"Private Key: {private_key}")

    wallet_address = derive_wallet_address(private_key)
    print(f"Wallet Address: {wallet_address}")

    balance = check_wallet_balance(wallet_address)
    print(f"Balance: {balance}")

    if balance > 0:
        print("Positive balance found!")
        break

print("Script executed successfully.")