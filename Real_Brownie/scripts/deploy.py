from brownie import accounts
import os


def deploy_simple_storage():
    # account = accounts.load("prosper-account") #best way to keep private key methond 1
    # print(account)
    
    account = accounts.add(os.environ.get("PRIVATE_KEY"))
    print(account)


def main():
    deploy_simple_storage()