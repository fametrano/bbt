if not exist "%APPDATA%\Bitcoin\regtestCarol" mkdir "%APPDATA%\Bitcoin\regtestCarol"
"bin\bitcoin-qt.exe" -regtest -txindex=1 -addresstype=bech32 -walletrbf=1 -uacomment=Carol -addnode=localhost:18444 -port=18555 -datadir="%APPDATA%\Bitcoin\regtestCarol"
start cmd /k cd bin
