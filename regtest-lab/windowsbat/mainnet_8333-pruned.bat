if not exist "..\bitcoin-pruneddata" mkdir "..\bitcoin-pruneddata"
"bin\bitcoin-qt.exe" -datadir="..\bitcoin-pruneddata" -addresstype=bech32 -walletrbf=1 -server -prune=550