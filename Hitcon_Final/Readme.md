# 封包分析

### Structure

    /pcap 
        - 2017-12-09_14:15:00.pcap.zip  : 當天最後封包
    /attack  : 當時的 Exploit
    /Abandon : 廢棄的 code 
        - analyize.py : tshark 處理速度太慢
        - m_view.py   : 賽前準備的封包視覺化，replay ...

    private.key : privkey
    download.py : 封包爬官方並下載進入 pcap/
    stream.py   : 將 pcap 檔拆開
    view.py     : 輕量化的看封包(無上色) -> 比賽途中嫌 m_view.py 指令難用、太長又複雜 ....
    submit.py   : 一開始寫的小上傳腳本，傳給 exploit 們 import 的
    