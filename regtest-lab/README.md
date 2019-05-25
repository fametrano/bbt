# Bitcoin Core: `regtest` Lab Session

## Install and Run Bitcoin Core

Please install and run Bitcoin Core in `regtest` mode, following the instructions provided for your platform:

* [windows.md](https://github.com/dginst/bbt/blob/master/regtest-lab/windows.md)
* [linux.md](https://github.com/dginst/bbt/blob/master/regtest-lab/linux.md)
* [mac-os.md](https://github.com/dginst/bbt/blob/master/regtest-lab/mac-os.md)

## The `bitcoin-cli` Command Line Tool

In general any command line must starts with `bitcoin-cli -regtest [...]` to use the _regtest_ daemon process. In the GUI console environment `bitcoin-cli -regtest` is already assumed and can be skipped, typing only the `[...]` part.

* get the block count (zero if you have not generated blocks yet or joined other nodes which might have)

  ```shell
  $ bitcoin-cli -regtest getblockcount
  0
  ```

## Digital Signature Using `bitcoin-cli`

* get a new _legacy_ (non _p2sh-segwit_ or _bech32_) address to be used for signatures, optionally labelling it with "used to sign":

  ```shell
  $ bitcoin-cli -regtest getnewaddress "used to sign" legacy
  mpXZvfkgYhpH2JR7bSrVMjxji3KnJi2s8s
  ```

* use this new address (not the `mpXZvfkgYhpH2JR7bSrVMjxji3KnJi2s8s` above!) to sign a message (e.g. `Hello, world!`). Note that `bitcoin-cli` uses the address to retrieve in background the corresponding private key actually used to sign:

  ```shell
  $ bitcoin-cli -regtest signmessage your_signing_address "Hello, world!"
  H6dXIhm+8cWKhYPv3e2zOba8+Nsnkh8osrZZGh4OPRR3MJk/HyzcaelHnhakg/YkUIWiFz73eY/klLgeCke8WwQ=
  ```

* verify the just generated signature (not the `H6dXIhm+8cWKhYPv3e2zOba8+Nsnkh8osrZZGh4OPRR3MJk/HyzcaelHnhakg/YkUIWiFz73eY/klLgeCke8WwQ=` above!):

  ```shell
  $ bitcoin-cli -regtest verifymessage your_signing_address your_signature "Hello, world!"
  true
  ```

* finally, verify this exogenously generated signature `IG+uGUUJ7VJ7tNBxhyBR92BF3PeMTQmqTBvPpxZAHxuRT938ehUmXfh7eORd/XiCARQbbKFlDew1O7nJiggdx7c=` for the message `Yes, it's me` signed by the address `mkiZWnZyaYTyv6Z6frLibmNuBRwnnXTZTY`

  ```shell
  $ bitcoin-cli -regtest verifymessage mkiZWnZyaYTyv6Z6frLibmNuBRwnnXTZTY IG+uGUUJ7VJ7tNBxhyBR92BF3PeMTQmqTBvPpxZAHxuRT938ehUmXfh7eORd/XiCARQbbKFlDew1O7nJiggdx7c= "Yes, it's me"
  true
  ```

## Block Generation

* optionally, connect to at least one node of the lab network to synchronize your node with the common blockchain, then check the updated block count, which is now probably greater than zero:

  ```shell
  $ bitcoin-cli -regtest addnode ipaddress_to_be_comunicated_in_lab add
  $ bitcoin-cli -regtest getblockcount
  412
  ```

* get a new address, that will be used to receive coins:

  ```shell
  $ bitcoin-cli -regtest getnewaddress
  bcrt1q26dwxdz0ht62gpy4py6jukc4qm7yvkw22hadar
  ```

* generate 101 blocks, sending the coinbase reward to your new address (not the `bcrt1q26dwxdz0ht62gpy4py6jukc4qm7yvkw22hadar` above!):

  ```shell
  $ bitcoin-cli -regtest generatetoaddress 101 your_address
  [
    "5512774c20aec78eb14ac584bc767fb9464491b64c5dc61ea485fc772daac3bd",
    "..."
    "496e7640439f08d45674d394c5b4818344b2e391cd19496daa1d9380a9fe1016"
  ]
  ```

## A Simple Transaction

* generating 101 blocks has created a spendable balance associated to your wallet:

  ```shell
  $ bitcoin-cli -regtest getbalance
  50.00000000
  ```

* send part of your balance (e.g. 0.99 coins) to `bcrt1qry4w50spgegfaemv7kl8q5efkfk3gpc5zvxnrd` (or any alternative address provided by a lab member) and note the returned transaction ID (`txid`)

  ```shell
  $ bitcoin-cli -regtest sendtoaddress bcrt1qry4w50spgegfaemv7kl8q5efkfk3gpc5zvxnrd 0.99
  3b11a2372173c4344edd0040a2a15d429c994287cc9cc0b9702546384c4ad4a1
  ```

* inspect the transaction (of course replacing the `3b11a2372173c4344edd0040a2a15d429c994287cc9cc0b9702546384c4ad4a1` below with your `txid`)

  ```shell
  $ bitcoin-cli -regtest gettransaction 3b11a2372173c4344edd0040a2a15d429c994287cc9cc0b9702546384c4ad4a1
  {
  "amount": -0.99000000,
  "fee": -0.00002820,
  "confirmations": 0,
  "trusted": true,
  "txid": "3b11a2372173c4344edd0040a2a15d429c994287cc9cc0b9702546384c4ad4a1",
  "walletconflicts": [
  ],
  "time": 1558782133,
  "timereceived": 1558782133,
  "bip125-replaceable": "yes",
  "details": [
    {
      "address": "bcrt1qry4w50spgegfaemv7kl8q5efkfk3gpc5zvxnrd",
      "category": "send",
      "amount": -0.99000000,
      "vout": 1,
      "fee": -0.00002820,
      "abandoned": false
    }
  ],
  "hex": "020000000001014afe8327a68faf8764a6eb9bbc5df55e0242a729f7d251a0db4cdb6b3406261b0000000000fdffffff023c481f240100000016001417a7b41a0168cf2f666d5a92f040fa93c37975efc09ee60500000000160014192aea3e0146509ee76cf5be705329b26d140714024730440220699fd7ea4c7bfac5652aa9e1d6d3cf6a697e5758c2b8cc1814cf1f8836b92baa02204c121a29feb851db8f9d4b0b4c9986c6c34ec7d749ec8fa59316e1eb20ca32ab01210397a0a9c8659f83cc3273ddc28da0eb27f74632d4d3421de3d6e4705ccad4dc8d65000000"
  }
  ```

* no confirmation yet; now generate one more block and notice that the trasaction has been confirmed (again: replace the `3b11a2372173c4344edd0040a2a15d429c994287cc9cc0b9702546384c4ad4a1` below with your `txid`):

  ```shell
  $ bitcoin-cli -regtest generatetoaddress 1 your_address
  [
    "642c3c401d0f15509647eadcd4d6c331e54747880264e72a07e3e2afbb3b74a9"
  ]
  $ bitcoin-cli -regtest gettransaction 3b11a2372173c4344edd0040a2a15d429c994287cc9cc0b9702546384c4ad4a1
  {
  "amount": -0.99000000,
  "fee": -0.00002820,
  "confirmations": 1,
  "blockhash": "642c3c401d0f15509647eadcd4d6c331e54747880264e72a07e3e2afbb3b74a9",
  "blockindex": 1,
  "blocktime": 1558782231,
  "txid": "3b11a2372173c4344edd0040a2a15d429c994287cc9cc0b9702546384c4ad4a1",
  "walletconflicts": [
  ],
  "time": 1558782133,
  "timereceived": 1558782133,
  "bip125-replaceable": "no",
  "details": [
    {
      "address": "bcrt1qry4w50spgegfaemv7kl8q5efkfk3gpc5zvxnrd",
      "category": "send",
      "amount": -0.99000000,
      "vout": 1,
      "fee": -0.00002820,
      "abandoned": false
    }
  ],
  "hex": "020000000001014afe8327a68faf8764a6eb9bbc5df55e0242a729f7d251a0db4cdb6b3406261b0000000000fdffffff023c481f240100000016001417a7b41a0168cf2f666d5a92f040fa93c37975efc09ee60500000000160014192aea3e0146509ee76cf5be705329b26d140714024730440220699fd7ea4c7bfac5652aa9e1d6d3cf6a697e5758c2b8cc1814cf1f8836b92baa02204c121a29feb851db8f9d4b0b4c9986c6c34ec7d749ec8fa59316e1eb20ca32ab01210397a0a9c8659f83cc3273ddc28da0eb27f74632d4d3421de3d6e4705ccad4dc8d65000000"
  }
  ```

* stop the daemon (and the GUI) with the command

  ```shell
  $ bitcoin-cli -regtest stop
  ```

## Further Material

For a [full command list](https://bitcoincore.org/en/doc/0.18.0/):

  ```
  $ bitcoin-cli help
  ```

For help about a peculiar command (e.g. [generatetoaddress](https://bitcoincore.org/en/doc/0.18.0/rpc/generating/generatetoaddress/)):

  ```
  $ bitcoin-cli generatetoaddress
  ```

To go beyond this short lab, please see <https://github.com/ChristopherA/Learning-Bitcoin-from-the-Command-Line>
