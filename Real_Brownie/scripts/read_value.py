from brownie import SimpleStorage, accounts, config, network


def read_contract():
    ss = SimpleStorage[-1]
    print(ss.retrieve())


def main():
    read_contract()
