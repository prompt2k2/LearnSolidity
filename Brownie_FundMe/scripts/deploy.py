from brownie import FundMe, config, network, MockV3Aggregator
from scripts.helpful_script import (
    get_account,
    deploy_mock,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()

    # pass pricefeed address to the fundme address contract
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]

    else:
        deploy_mock()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e",
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )  # publish source uses the etherscan token(API) in environment key

    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
