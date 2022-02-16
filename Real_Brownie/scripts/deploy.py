from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    #account_ganache = accounts[0]
    # prints the first account on the local ganache chain.
    # account = accounts.load("prosper-account") #best way to keep private key methond 1
    # print(account)

    # account = accounts.add(os.environ.get("PRIVATE_KEY")) #method 1
    # account = accounts.add(config["wallets"]["from_key"]) #Save method 2
    # print("current workspace account is: ", account)
    
    account_ganache = get_account()

    print("Deploying Contract...")
    ss = SimpleStorage.deploy({"from": account_ganache})

    stored_value = ss.retrieve()

    transaction = ss.store(99, {"from": account_ganache})
    transaction.wait(1)

    new_stored_value = ss.retrieve()

    print("---------------------------------------")
    print("Current Value: ", stored_value, "|", "New value: ", new_stored_value)
    print("---------------------------------------")

    print("...Deployed!!!")

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    
def main():
    deploy_simple_storage()
