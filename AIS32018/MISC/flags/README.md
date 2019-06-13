# Flags 

這題的 flag 藏在圖片中

一開始看到圖片，就很直覺的 binwalk 發現有壓縮檔在裡面

還有加密？！

未看先猜是偽加密，後來發現不是

之後找到裡面的圖檔，用 pkcrack

```
pkcrack -C flag.zip -c 'backup/Avengers_Infinity_War_Poster.jpg' -P test.zip -p 'Avengers_Infinity_war_poster.jpg' -n
```

解出密碼為 `asdfghjkl;`

但是裡面的 flag 是假的 ....

後來發現圖面上的點好像怪怪的 .....

摩斯密碼 =.=|||?

### AIS3{YOUFINDTHEREALFLAGOHYEAH}

