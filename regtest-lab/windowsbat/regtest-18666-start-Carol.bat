if not exist "..\bitcoin-data" mkdir "..\bitcoin-data"
if not exist "..\bitcoin-data\_Bob" mkdir "..\bitcoin-data\_Carol"
"bin\bitcoin-qt.exe" -regtest -datadir="..\bitcoin-data\_Carol" -addresstype=bech32 -walletrbf=1 -port=18666 -addnode=localhost:18444
