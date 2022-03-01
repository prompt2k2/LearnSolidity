from scripts.helpful_script import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import FundMe, network, accounts, exceptions
import pytest

def test_can_transact():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from":account, "value":entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account) == entrance_fee
    
    tx2 = fund_me.withdraw({"from":account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account) == 0
    


def test_owner_only_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for Local testing")
        
    
    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    fund_me.withdraw({"from":bad_actor})
    
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from":bad_actor})
        
        
