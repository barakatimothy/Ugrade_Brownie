from scripts.helpful_scripts import get_accounts,encode_function_data,upgrade
from brownie import Box,BoxV2,exceptions,ProxyAdmin,transparent_upgradable_proxy,Contract
import pytest


def test_proxy_upgrades():
    account = get_account()
    box = Box.deploy({"from":account},publish_source=True)
    proxy_admin = ProxyAdmin.deploy({"from":account},publish_source=True)
    box_encoded_initializer_function= encode_function_data()
    proxy = transparent_upgradable_proxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from":account,"gaslimt":100000}
    )
    boxv2 = Box2.deploy({"from":account},publish_source=True)
    proxy_box = Contract.from_abi("BoxV2",proxy.address,BoxV2.abi)
    with pytest.raises(exception.VirtualMachineError):
        proxy_box.increment({"from":account},publish_source=True)
    upgrade(account ,proxy,boxv2,proxy_admin_contract = proxy_admin)
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from":account},publish_source=True)
    assert proxy_box.retrieve() == 1