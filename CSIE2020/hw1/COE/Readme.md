# COR

題目中把三個 LFSR 的輸出混在一起，混合的方法就是上課舉的例子 `(x1 & x2) ^ ((not x1) & x3)`

[Correlation Attack script](./solve1.py)

可以用 Correlation Attack，分別暴搜三個 LFSR 的 init，只要搜到正確的答案，產出的輸出就會跟混合的輸出有大約 75% 的吻合率，三個各需要暴搜 65536 次，總共 196608 次。

[z3-script](./solve2.py)

或是直接用 z3 炸他。
