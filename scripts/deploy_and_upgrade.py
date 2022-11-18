from scripts.helpful_scripts import get_account ,encode_function_data,upgrade
from brownie import network,ProxyAdmin ,Box,transparent_upgradable_proxy,Contract,Box2

def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account})
    
    proxy_admin = ProxyAdmin.deploy({"from":account})
    
    initializer = box.store ,1
    box_encoded_initializer_function = encode_function_data(initializer)
    
    proxy = TransparentUpgradableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {'from':account,'gaslimit':1000000}
    )
    print(f'Proxy Deployed {proxy} you can now upgrade to V2')
    proxy_box = contract.from_abi("Box",proxy.address,Box.abi)
    proxy_box.store(1,{"from":account})
    print(proxy_box.retrieve())
    
    #upgrade
    box_V2 = Box2.deploy({"from":account})
    upgrade_tx = upgrade(account,
                         proxy,
                         box_V2.address,
                         proxy_admin_contract =proxy_admin)
    
    print("Proxy has been Upgraded")
    proxy_box = Contract.from_abi("BoxV2",proxy.address,Box2.abi)
    proxy_box.increment({'from':account})
    print(proxy_box.retrieve())