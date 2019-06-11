if not exist "%APPDATA%\Bitcoin\regtestBob" mkdir "%APPDATA%\Bitcoin\regtestBob"
"bin\bitcoin-qt.exe" -regtest -uacomment=Bob -txindex=1 -datadir="%APPDATA%\Bitcoin\regtestBob" -addresstype=bech32 -walletrbf=1 -port=18555 -addnode=localhost:18444
start cmd /k cd bin
