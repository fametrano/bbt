# Bitcoin Core - regtest lab session

## Install Bitcoin Core

Please install and run Bitcoin Core for your platform, following the instructions provided in
[windows.md](https://github.com/dginst/BitcoinBlockchainTechnology/blob/master/regtest-lab/windows.md),
[linux.md](https://github.com/dginst/BitcoinBlockchainTechnology/blob/master/regtest-lab/linux.md), or
[mac-os.md](https://github.com/dginst/BitcoinBlockchainTechnology/blob/master/regtest-lab/mac-os.md).

## The `bitcoin-cli` Command Line Tool

In general any command line must starts with `bitcoin-cli -regtest [...]` to use the _regtest_ daemon process. In the GUI console environment `bitcoin-cli -regtest` is already assumed and can be skipped, typing only the `[...]` part.

* connect to one peculiar node of the network  

  ```shell
  $ bitcoin-cli -regtest addnode “ipaddress-to-be-comunicated-in-class” “add”
  ```

* generate 101 blocks to an address of yours

  ```shell
  $ bitcoin-cli -regtest getnewaddress
  bcrt1q26dwxdz0ht62gpy4py6jukc4qm7yvkw22hadar
  $ bitcoin-cli -regtest generatetoaddress 101 bcrt1q26dwxdz0ht62gpy4py6jukc4qm7yvkw22hadar
  ```

## Digital Signature Using `bitcoin-cli`

* generate a _legacy_ (non _p2sh-segwit_ or _bech32_) address, optionally labelled with "used to sign", then use it to sign the message _"Hello, World"_ with the corresponding private key, finally verify the signature

  ```shell
  $ bitcoin-cli -regtest getnewaddress "used to sign" legacy
  mpXZvfkgYhpH2JR7bSrVMjxji3KnJi2s8s

  $ bitcoin-cli -regtest signmessage mpXZvfkgYhpH2JR7bSrVMjxji3KnJi2s8s "Hello, world!"
  H6dXIhm+8cWKhYPv3e2zOba8+Nsnkh8osrZZGh4OPRR3MJk/HyzcaelHnhakg/YkUIWiFz73eY/klLgeCke8WwQ=

  $ bitcoin-cli -regtest verifymessage mpXZvfkgYhpH2JR7bSrVMjxji3KnJi2s8s H6dXIhm+8cWKhYPv3e2zOba8+Nsnkh8osrZZGh4OPRR3MJk/HyzcaelHnhakg/YkUIWiFz73eY/klLgeCke8WwQ= "Hello, world!"
  true
  ```

## A Simple Bitcoin Transaction

* send 99.0 regtest-bitcoins to bcrt1qry4w50spgegfaemv7kl8q5efkfk3gpc5zvxnrd and inspect the transaction

  ```shell
  $ bitcoin-cli -regtest sendtoaddress bcrt1qry4w50spgegfaemv7kl8q5efkfk3gpc5zvxnrd 99
  88548ee355c4d97064fa6182581bbff19421e67227838215669df2611b756f32
  
  $ bitcoin-cli -regtest gettransaction 88548ee355c4d97064fa6182581bbff19421e67227838215669df2611b756f32
  {
  "amount": -99.00000000,
  "fee": -0.00004160,
  "confirmations": 0,
  "trusted": true,
  "txid": "88548ee355c4d97064fa6182581bbff19421e67227838215669df2611b756f32",
  "walletconflicts": [
  ],
  "time": 1558777289,
  "timereceived": 1558777289,
  "bip125-replaceable": "yes",
  "details": [
    {
      "address": "bcrt1qry4w50spgegfaemv7kl8q5efkfk3gpc5zvxnrd",
      "category": "send",
      "amount": -99.00000000,
      "vout": 0,
      "fee": -0.00004160,
      "abandoned": false
    }
  ],
  "hex": "020000000001021249e7589bd0256a0ff35125b1f7f0c5734d4a800ce359aebfbf311b87a61ed60000000000fdffffff23a40c9014d434732d6d0748b71648a5c09f074e04b66bbfe506acc20696b1320000000000fdffffff020003164e02000000160014192aea3e0146509ee76cf5be705329b26d140714c0d0f50500000000160014271c282275084366c27e22b0bcbabf1e903d1dee024730440220704277085c41de0aa4a424552f4fbd12b3a8714a6c1592f4332e07471015813f022026442e9e55fad4752d8e3fc012a19489a4bdc71ea1932b27f6e712892c21116a01210221e944abb462400f7d64af8e141acf4757d6a5257aa8e100167a11a151df3efa02473044022020521904785a65a266d06a831d085965d12882e92a5b354286cc0f7ee5362afe02201b41a91a9ae1f498540cdeb545f60adcbea36ddc917e6ab31e24c79265c1860f01210221e944abb462400f7d64af8e141acf4757d6a5257aa8e100167a11a151df3efa6f000000"
  }
  ```

* no confirmation yet; now generate one block and notice that the trasaction has been confirmed

  ```shell
  $ bitcoin-cli -regtest generatetoaddress 1 bcrt1q26dwxdz0ht62gpy4py6jukc4qm7yvkw22hadar
  $ bitcoin-cli -regtest gettransaction 88548ee355c4d97064fa6182581bbff19421e67227838215669df2611b756f32
  {
  "amount": -99.00000000,
  "fee": -0.00004160,
  "confirmations": 1,
  "blockhash": "42dffd4b2a023d9080ac2f557e1e9869b81708c3a94a81f10d8d1bf6bfe9716d",
  "blockindex": 1,
  "blocktime": 1558777455,
  "txid": "88548ee355c4d97064fa6182581bbff19421e67227838215669df2611b756f32",
  "walletconflicts": [
  ],
  "time": 1558777289,
  "timereceived": 1558777289,
  "bip125-replaceable": "no",
  "details": [
    {
      "address": "bcrt1qry4w50spgegfaemv7kl8q5efkfk3gpc5zvxnrd",
      "category": "send",
      "amount": -99.00000000,
      "vout": 0,
      "fee": -0.00004160,
      "abandoned": false
    }
  ],
  "hex": "020000000001021249e7589bd0256a0ff35125b1f7f0c5734d4a800ce359aebfbf311b87a61ed60000000000fdffffff23a40c9014d434732d6d0748b71648a5c09f074e04b66bbfe506acc20696b1320000000000fdffffff020003164e02000000160014192aea3e0146509ee76cf5be705329b26d140714c0d0f50500000000160014271c282275084366c27e22b0bcbabf1e903d1dee024730440220704277085c41de0aa4a424552f4fbd12b3a8714a6c1592f4332e07471015813f022026442e9e55fad4752d8e3fc012a19489a4bdc71ea1932b27f6e712892c21116a01210221e944abb462400f7d64af8e141acf4757d6a5257aa8e100167a11a151df3efa02473044022020521904785a65a266d06a831d085965d12882e92a5b354286cc0f7ee5362afe02201b41a91a9ae1f498540cdeb545f60adcbea36ddc917e6ab31e24c79265c1860f01210221e944abb462400f7d64af8e141acf4757d6a5257aa8e100167a11a151df3efa6f000000"
  }
  ```

* stop the daemon (and the GUI) with the command

  ```shell
  $ bitcoin-cli -regtest stop
  ```

## Further Material

For a [full command list](https://bitcoincore.org/en/doc/0.17.0/):

  ```
  $ bitcoin-cli help
  ```

For help about a peculiar command (e.g. [generatetoaddress](https://bitcoincore.org/en/doc/0.18.0/rpc/generating/generatetoaddress/)):

  ```
  $ bitcoin-cli generatetoaddress
  ```

To go beyond this short lab class, please see <https://github.com/dginst/Learning-Bitcoin-from-the-Command-Line>
