if not exist "%APPDATA%\Bitcoin\mainnet_pruned" mkdir "%APPDATA%\Bitcoin\mainnet_pruned"
start bin\bitcoin-qt.exe -prune=550 -datadir="%APPDATA%\Bitcoin\mainnet_pruned" -server -rpcallowip=127.0.0.1 -addresstype=bech32 -walletrbf
::start cmd /k cd bin