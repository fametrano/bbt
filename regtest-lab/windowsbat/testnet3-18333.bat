if not exist "..\bitcoin-data" mkdir "..\bitcoin-data"
start bin\bitcoin-qt.exe -testnet -server -rpcallowip=127.0.0.1 -addresstype=bech32 -walletrbf
::start cmd /k cd bin