from secret import FLAG

a = int(FLAG.hex()[:20],16)
b = int(FLAG.hex()[20:44],16)
p = int(FLAG.hex()[44:],16)
print(a,b,p)
a = 308306428974966359881267 
b = 29494623268190324519574202417
p = 2459647807017753197447615947630064170310783101 
print(p)
ec = EllipticCurve(GF(p), [a,b])

def cal(x,p) :
    return int(mod(pow(x,3,p) + a*x + b ,p).sqrt())

x1 = p-1
y1 = cal(x1,p) #  sqrt( -1 - a +b) - kp 
print(f"ecc.point(p-1,{y1})")

x2 = p+1
y2 = cal(x2,p) # sqrt( sqrt(  1 + a +b) - kp )
print(f"ecc.point(p+1,{y2})")

x3 = p+2
y3 = cal(x3, p) # sqrt( sqrt( -9 -3a +b) - kp )
print(f"ecc.point(p+2,{y3})")

x4 = p-3
y4 = cal(x4, p) # sqrt( sqrt( -9 -3a +b) - kp )
print(f"ecc.point(p-3,{y4})")

x5 = p+3
y5 = cal(x5, p) # sqrt( sqrt( 9 + 3a +b) - kp )
print(f"ecc.point(p+3,{y5})")

x6 = p-4
y6 = cal(x6, p) # sqrt( sqrt( 9 + 3a +b) - kp )
print(f"ecc.point(p-4,{y6})")

x7 = p-5
y7 = cal(x7, p) # sqrt( sqrt( -125 - 5a +b) - kp )
print(f"ecc.point(p-5,{y7})")

x8 = p+5
y8 = cal(x8, p) # sqrt( sqrt( 125 + 5a +b) - kp )
print(f"ecc.point(p+5,{y8})")

x9 = p-7
y9 = cal(x9, p) # sqrt( sqrt( -125 - 5a +b) - kp )
print(f"ecc.point(p-7,{y9})")

k1p = (y2**2 + y4**2 - 2*y1**2 +24) 
k2p = (y4**2 + y8**2 - 2*y2**2 -96) 
p = gcd(k1p,k2p)

assert k1p % p == 0
assert k2p % p == 0

b = ((y1**2 + y2**2) // 2) % p
a = (y2**2 -1-b) %p




# p1 = ec.point((x1, y1))
# p2 = ec.point((x2, y2))
# p3 = ec.point((x3, y3))
# p4 = ec.point((x4, y4))


# P = (24394320413281288780882544774942921213856811482992711358928931039417, 35723153402211727676145579990898489948330341864453428731829425367597)

# print( factor(2*y1**2 - (y2**2 + y3**2 ) +24) )