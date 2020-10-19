# POA

上課有講到的 Padding Oracle Attack，唯獨把 Padding 的方式改成 padding 0b10000000 這種格式，一個 bit 的 1 後面剩下的都填 0，解法跟原來的一樣，不過要注意在暴搜最後一個 block 的時候，假設我們設定最後一個 byte 是 0x00，我們預期暴搜倒數第二個 byte 成功時，他會是 0x80，但很有可能其實是 0x00，因為倒數第三個 byte 可能是 0x80 ( 原本正確的 padding 的那個 0x80 )，你可以選擇把正在暴搜的 byte 前面的 bytes 都攪亂就不會出現這個情況了。

by OAlienO