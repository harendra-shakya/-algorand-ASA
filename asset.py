import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, wait_for_confirmation


addr1 = "7AKZKSQZR5TVUB53IV3NWAGKWQYT7EH2NBSRDIFWJXLR2JFQHNT5LUHCD4"
passphrase = "absorb close review toe spice fragile length shiver achieve merge magnet snap satoshi early print spell misery glad vocal air evidence funny avocado about ten"

addr2 = "LKFGWMWNHMGOM5SFEPMJVFG65RXKOBDGRBSERIY33DVFYUFA7QHBLIWLQU"
passphrase1 = "priority such quality aware diagram oil salon stay warm puppy sentence blush police gym razor double umbrella oil network piece feel chaos casino abandon solar"

addr3 = "IG67UGBS5Z5ONGKSV6RX3QC5F2VQ6CADIYIDP6WM7F6W4YJ4YLBCIIOXP4"
passphrase2 = "busy mechanic three casual hard relax toe visit essence risk key method area cram omit knee catch asthma cover glare inform lawn color absorb miss"

private_key = mnemonic.to_private_key(passphrase)
private_key1 = mnemonic.to_private_key(passphrase1)
private_key2 = mnemonic.to_private_key(passphrase2)

asset_id=148931662

algod_client = algod.AlgodClient('','https://testnet-api.algonode.cloud')


account_info = algod_client.account_info(addr1)
print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")
def assetCreation():
    # CREATE ASSET
    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    # Account 1 creates an asset called latinum and
    # sets Account 2 as the manager, reserve, freeze, and clawback address.
    # Asset Creation transaction
    txn = AssetConfigTxn(
        sender=addr1,
        sp=params,
        total=10000,
        default_frozen=False,
        unit_name="NF",
        asset_name="Algo Token",
        manager=addr1,
        reserve=addr1,
        freeze=addr1,
        clawback=addr1,
        url="https://path/to/my/asset/details", 
        decimals=0)
    # Sign with secret key of creator
    stxn = txn.sign(private_key)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))  
        print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4))) 
    except Exception as err:
        print(err)
       
        # print("Decoded note: {}".format(base64.b64decode(
        #     confirmed_txn["txn"]["txn"]["note"]).decode()))
        try:
            ptx = algod_client.pending_transaction_info(txid)
            asset_id = ptx["asset-index"]
            print("Asset ID: ",asset_id)
        except Exception as e:
            print(e)


def modifyAsset():
    # CHANGE MANAGER
    # The current manager(Account 2) issues an asset configuration transaction that assigns Account 1 as the new manager.
    # Keep reserve, freeze, and clawback address same as before, i.e. account 2
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    txn = AssetConfigTxn(
        sender=addr1,
        sp=params,
        index=asset_id, 
        manager=addr2,
        reserve=addr1,
        freeze=addr1,
        clawback=addr1)
    # sign by the current manager - Account 2
    stxn = txn.sign(private_key)
    # txid = algod_client.send_transaction(stxn)
    # print(txid)
    # Wait for the transaction to be confirmed
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
    except Exception as err:
        print(err)
        
def receiveAsset():
    params = algod_client.suggested_params()
    txn = AssetTransferTxn(
        sender=addr3,
        sp=params,
        receiver=addr3,
        amt=0,
        index=asset_id
    )
    stxn = txn.sign(private_key2)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))    
    except Exception as err:
        print(err)

def transferAsset():
    # TRANSFER ASSET
    # transfer asset of 10 from account 1 to account 3
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    txn = AssetTransferTxn(
        sender=addr1,
        sp=params,
        receiver=addr3,
        amt=110,
        index=asset_id
    )
    stxn = txn.sign(private_key)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)
             

def assetFreeze():
    # FREEZE ASSET
    params = algod_client.suggested_params()
    txn = AssetFreezeTxn(
        sender=addr1,
        sp=params,
        index=asset_id,
        target=addr3,
        new_freeze_state=True   
    )
    stxn = txn.sign(private_key)
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))    
    except Exception as err:
        print(err)
  
def assetRevoke():
    # REVOKE ASSET
    params = algod_client.suggested_params()
    txn = AssetTransferTxn(
        sender=addr1,
        sp=params,
        receiver=addr1,
        amt=105,
        index=asset_id,
        revocation_target=addr3
    )
    stxn = txn.sign(private_key)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))      
    except Exception as err:
        print(err)


def assetDestroy():
    params = algod_client.suggested_params()
    txn = AssetConfigTxn(
        sender=addr2,
        sp=params,
        index=asset_id,
        strict_empty_address_check=False
    )
    # Sign with secret key of creator
    stxn = txn.sign(private_key1)
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))     
    except Exception as err:
        print(err)

assetCreation()