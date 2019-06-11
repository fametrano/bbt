if not exist "%APPDATA%\Bitcoin\regtestBob" mkdir "%APPDATA%\Bitcoin\regtestBob"
"bin\bitcoin-qt.exe" -regtest -txindex=1 -addresstype=bech32 -walletrbf=1 -uacomment=Bob -addnode=localhost:18444 -port=18555 -datadir="%APPDATA%\Bitcoin\regtestBob"
start cmd /k cd bin
