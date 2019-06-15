if not exist "%APPDATA%\Bitcoin\testnet_pruned" mkdir "%APPDATA%\Bitcoin\testnet_pruned"
start bin\bitcoin-qt.exe -testnet -prune=550 -datadir="%APPDATA%\Bitcoin\testnet_pruned" -server -rpcallowip=127.0.0.1 -addresstype=bech32 -walletrbf
::start cmd /k cd bin