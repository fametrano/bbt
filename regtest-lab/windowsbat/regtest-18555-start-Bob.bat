if not exist "%APPDATA%\Bitcoin\regtest_Bob" mkdir "%APPDATA%\Bitcoin\regtest_Bob"
start bin\bitcoin-qt.exe -regtest -datadir="%APPDATA%\Bitcoin\regtest_Bob" -txindex -uacomment=Bob -port=18555 -addnode=localhost:18444 -addresstype=bech32 -walletrbf
