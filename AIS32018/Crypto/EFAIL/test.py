from cryptools import *

b64cipher = "Wa0Vn+wFd/UpR0Y26BHiCldxP+8hkcgaKId4j8cGCKHjus9kRX2Z8L7aRGOLgwpyYPzL87avrQSS2KNiECUd8HU7PPkaVte1qRhehtYeJbeOaw2CYAgKKz4puG0Zb8FQUp3anOYl+wevh6OibHcUM12j8YF9kHyXIPksBdXUycPNqP2kiz8HEE4WSBmfRjbSdpykxTEIfXpgCsoGA3i6PhWG3LXECo3DmlAOfFAP67uyaqSEoFj2WerwGKG/F84fAYFir4mGUjjuheDzkE8GsdeF9HFzIOOIRuBa2ybZ5QJrUzHN/KLoBYEUjwlJzJBoXWhaKRFDG8JGMUAK/AK/sXhrHnIpyJv9xUl/rUuctDqQ8lM9XJHvsviVPZtJdjht5/GQGByM3htAVnkmYcR6BBoca6Wec5L1BWomt0IUr1yfR4drGbc8y4ms7eRo8/CJdCGlNDV43uSRnJhBzjfskisPZrrsdDJArW2gjo2ssnAjTiLAph82YP2lCaEemtoTc+CjfAuFyToEMMNNZiaaeoGFkDDLibsR0ug1gfUOEq3C4gxLj0rtWcGBcVYLCZatjH27suTLxQe7tImEBxYpNu48pAEjTcy/LSZV+GZean/UnHfbZNG5rwWZKLL9IteVWe2riWFaXWToxtyo3/mSL7G/MnIvWH129bU2N7JfVU00pZ8CkGGKpZl+wmi7N29UyR7pXJh8ywB5eUo27KfFFYSjy85Te29M8Rc1mSLkALk8UQ3wHZrpOmJO4vTMcpXwev+MIFo7r6e/1YiQ1GumlqtvMAwpBZWtmlzyq3vaFSeU6WCCUaPfrB8hXNBCBC6VvDDxQMje5suoNEV2JrDfoJSfEYEL+5Nhvu8uFTQhdKc="

flag = "{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}"

plaintext = '''
From: thor@ais3.org
To: ctfplayer@ais3.org

--BOUNDARY
Type: text
Welcome to AIS3 pre-exam.

--BOUNDARY
Type: cmd
echo 'This is the blog of oalieno'
web 'https://oalieno.github.io'
echo 'This is the blog of bamboofox team'
web 'https://bamboofox.github.io/'

--BOUNDARY
Type: text
You can find some useful tutorial on there.
And you might be wondering where is the flag?
Just hold tight, and remember that patient is virtue.

--BOUNDARY
Type: text
Here is your flag : {}

--BOUNDARY
Type: text
Hope you like our crypto challenges.
Thanks for solving as always.
I'll catch you guys next time.
See ya!

--BOUNDARY
'''.format(flag).lstrip().encode('utf-8')

cipher = switchBS(b64d(b64cipher))

print( len(plaintext) , len(cipher) )
for i  in range(0,len(cipher),16):
    print(i, plaintext[i:i+16])

print(plaintext[256-16:256])
print(plaintext[256:256+16])
temp = xor_string(cipher[256-16:256] ,"'\n\n--BOUNDARY\nTy")

temp = xor_string(temp ,"\'\nweb\'d.djo6.ml/")

temp2 = xor_string(cipher[512-16:512] ,"\nType: text\nHope")

temp2 = xor_string(temp2 ,"\'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

temp3 = xor_string(cipher[448:512],"kbcd")

cipher = cipher[:256]+ temp + cipher[256:256+16] + temp3 + cipher[448+4:512] + temp2 + cipher[512:]

print(b64e(switchBS(cipher)))
