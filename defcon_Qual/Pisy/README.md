# Easy Pisy - Crypto , Web

Enter `http://5a7f02d0.quals2018.oooverflow.io` 

find `Sign your payload` and `Execute your signed payload` two file upload.

download the `samples.tgz` and test them.

knowing that 

1. Service 

First service : Recognized pdf input via OCR and sign on it. (but reject to sign on EXECUTE command)
Second one : Give the signed value and pdf, this service will execute it.

2. list of directory

```
common.php
execute.php
flag
index.nginx-debian.html
index.php
private_key.pem
public_key.pem
sign.php
```

--------------------------------

Next, look on sign.php `openssl_sign($data, $signature, $privkey)`

We found that this function will sha1(data) before sign.

so we can make a [sha1 collision](https://github.com/maojui/Cryptools/blob/master/cryptools/hash.py)

Therefore, draw two command on picture and collision them.

1. send the picutre 1 (`without EXECUTE`) to first service to `get the signature`

2. pass this signature and sha1-collision picture ( with EXECUTE cat < flag ) to get the flag.

