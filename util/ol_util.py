import os
import re
from typing import AnyStr


def is_slow_wallet(address: AnyStr) -> bool:
    """
    Checks if a given address is a flagged as 'slow' wallet.
    :param address: the address to check
    :return: Boolean True if the wallet is a slow wallet, else False
    """
    # check if the address is valid
    regex_out = re.search("[a-fA-F0-9]{32}$", address)
    if not regex_out:
        return False

    # We are checking both 'SlowWallet' and 'Community' occurence in the query output
    with os.popen(f"ol -a {address} query -r | sed -n '/SlowWallet/,/StructTag/p'") as f:
        for elem in f.readlines():
            print(elem)
            if 'SlowWallet' in elem:
                return True
    
    return False


if __name__ == "__main__":
    
    test_list = [
        "5F8AC83A9B3BF2EFF20A6C16CD05C111", # basic wallet >> SLOW
        "2BFD96D8A674A360B733D16C65728D72", # basic wallet
        "1367B68C86CB27FA7215D9F75A26EB8F", # community wallet
        "5335039ab7908dc38d328685dc3b9141", # miner wallet
        "7e56b29cb23a49368be593e5cfc9712e", # validator wallet >> SLOW
        "82a1097c4a173e7941e2c34b4cbf15b4", # miner wallet
        "5e358589da97d5f08bf3a7462a112ae6", # miner wallet
        "19E966BFA4B32CE9B7E23721B37B96D2", # community wallet
        "cd0fa23141e9e5e348b33c5da51f211d", # miner wallet
        "f100a2878d61bab8554aed256feb8001", # miner wallet
        "4be425e5306776a0bd9e2db152b856e6", # miner wallet >> SLOW
        "7103da7bb5bb15eb7e72b6db16147f56", # miner wallet
        "74745f89883134d270d0a57c6c854b4b", # miner wallet
    ]

    for addr in test_list:
        if is_slow_wallet(addr):
            print(f"{addr} is a slow wallet!")
    