if not exist "%APPDATA%\Bitcoin\regtest_Carol" mkdir "%APPDATA%\Bitcoin\regtest_Carol"
start bin\bitcoin-qt.exe -regtest -datadir="%APPDATA%\Bitcoin\regtest_Carol" -txindex -uacomment=Carol -port=18666 -addnode=localhost:18444 -addresstype=bech32 -walletrbf
