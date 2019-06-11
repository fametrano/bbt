if not exist "..\bitcoin-data" mkdir "..\bitcoin-data"
if not exist "..\bitcoin-data\_Bob" mkdir "..\bitcoin-data\_Bob"
"bin\bitcoin-qt.exe" -regtest -datadir="..\bitcoin-data\_Bob" -addresstype=bech32 -walletrbf=1 -port=18555 -addnode=localhost:18444
