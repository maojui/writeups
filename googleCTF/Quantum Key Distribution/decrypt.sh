# echo ./decrypt.sh key flag
echo $1 > /tmp/plain.key; xxd -r -p /tmp/plain.key > /tmp/enc.key
echo $2 | openssl enc -d -aes-256-cbc -pbkdf2 -md sha1 -base64 --pass file:/tmp/enc.key