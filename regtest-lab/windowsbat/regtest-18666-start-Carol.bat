if not exist "%APPDATA%\Bitcoin\regtestCarol" mkdir "%APPDATA%\Bitcoin\regtestCarol"
"bin\bitcoin-qt.exe" -regtest -uacomment=Carol -txindex=1 -datadir="%APPDATA%\Bitcoin\regtestCarol" -addresstype=bech32 -walletrbf=1 -port=18555 -addnode=localhost:18444
start cmd /k cd bin
