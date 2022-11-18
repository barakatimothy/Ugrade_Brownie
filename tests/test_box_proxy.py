from script.helpful_scripts import get_account,encode_function_data
from brownie import Box,ProxyAdmin,transparent_upgradable_proxy,Contract
def test_proxy_delegates_calls():
    acccount = get_account()
    box = Box.deploy({"from":acccount})
    proxy_admin = ProxyAdmin.deploy({'from':acccount})
    box_encoded_initializer_function = encode_function_data()
    proxy = transparent_upgradable_proxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from":acccount ,"gaslimit":1000000}
    )
    proxy_box = Contract.from_abi("Box",proxy.address,Box.abi)
    assert proxy_box.retrieve( ) == 0
    proxy_box.store (1, {"from":account})
    assert proxy_box.retrieve == 1