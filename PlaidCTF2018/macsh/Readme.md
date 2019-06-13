## PCTF 2018 Macsh (Crypto 125pt)

```
Forget ssh, this is a much more secure shell. 
Server running at macsh.chal.pwning.xxx:64791
```

This Challenge need you bypass the MAC check.

```python
mac, cmdline = input().split('<|>')
cmd, *args = cmdline.split()
```

What you need to send is like `MAC<|>COMMAND`

And the MAC check is ...

```
if cmd == "tag" or bytes.hex(fmac(k0, k1, encode(cmdline))) == mac:
    eval(cmd)(*args)
```

If you want server executes your command :
1. cmd == 'tag'
2. The right MAC, encode by cmdline.

[Full Writeup](https://maojui.github.io/CTF-Writeups-2018/Plaid-2018-Macsh/)
