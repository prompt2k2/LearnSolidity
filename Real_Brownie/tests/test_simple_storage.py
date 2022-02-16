from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange with
    account = accounts[0]

    # Act
    ss = SimpleStorage.deploy({"from": account})
    old_value = ss.retrieve()
    expected = 0

    # Assert
    assert old_value == expected


def test_updating_storage():
    # Arrange
    account = accounts[0]
    ss = SimpleStorage.deploy({"from": account})

    # Act
    expected = 99
    ss.store(expected, {"from": account})

    # Assert
    assert expected == ss.retrieve()
