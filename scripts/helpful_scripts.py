from brownie import network,config,accounts,MockAggregatorV3
from web3 import Web3
import eth_utils

decimals=8
startingPrice=200000000
FORKED_BLOCKCHAIN=['mainnet-fork','mainnet-fork-dev']
LOCAL_BLOCKCHAIN=['development','ganache-loacl']

def get_accounts():
    if network.show_active() in LOCAL_BLOCKCHAIN:
        return accounts[0]
    else:
       return accounts.add(config["wallets"]["from_key"])



def deploy_mocks():
    print(f'Active Networks {network.show_active}')
    print('deploying Mock')
    if len(MockAggregatorV3)<=0:
     MockAggregatorV3.deploy(decimals,Web3.toWei(startingPrice,'ethers'),{'from ': account})
     
     
    
def encode_function_data(initializer = None ,*args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_byte(hexstring="ox")
    return initializer.encode_input(*args)


def upgrade (account ,
             proxy,
             new_implementation_address,
             proxy_admin_contract,
             initializer,
             *args):
 transaction =  None
 if proxy_admin_contract :
    if initializer:
        encode_function_call = encode_function_data(initializer,*args)
        transaction = proxy_admin_contract.upgradeAndCall(
            proxy.address,
            new_implementation_address,
            encode_function_call,
            {'from':account}
        )
    else:
        transaction = proxy_admin_contract.upgrade(
            proxy.address,
            new_implementation_address,
            {'from':account}
            )
    if initializer:
       encode_function_call = encode_function_data(initializer,*args)
       proxy.upgradeToAndCall(
               new_implementation_address,
               encode_function_call,
               {"from":account}
               )
    else:
        transaction = proxy.upgradeTo(new_implementation_address,{"from":account})
        
    return transaction