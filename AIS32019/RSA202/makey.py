from Crypto.Util.number import getPrime, isPrime, inverse 
count = 0
while True :
    count += 1
    print(count)
    p = getPrime(300)
    if isPrime(pow(p,4) + pow(p,3) + pow(p,2) + p + 1) : 
        break

    if isPrime(pow(p,2) + p + 1) : 
        break
