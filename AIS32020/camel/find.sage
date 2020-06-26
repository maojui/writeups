
# flag = "AIS3{Curv3_Mak3_M3_Th1nK_Ab0Ut_CaME1_A_P}"
# k = bytes( map(ord,flag) )
# n = k.hex()



# def cal(x, a,b, p) :
#     return int(mod(pow(x,3,p) + a*x + b ,p).sqrt())


# for i in range(len(n)): 
#     try :
#         if is_prime(int(n[-i:],16)) and i % 2 == 0: 
#             print(i) 
#             r = (i//2) % 2
#             print(r)
#             a = int(n[:(i//2)+r],16)
#             b = int(n[(i//2)+r:-i],16)
#             p = int(n[-i:], 16)

#             if p > b and p > a :
#                 print(bytes.fromhex(hex(a)[2:]))
#                 print(bytes.fromhex(hex(b)[2:]))
#                 print(bytes.fromhex(hex(p)[2:]))
#             x1 = p-1
#             y1 = cal(p-1,a,b,p) # sqrt( sqrt( -1 - a +b) - kp )
#             print(p,a,b)
#             print("1")

#             x2 = p+1
#             y2 = cal(p+1,a,b,p) # sqrt( sqrt(  1 + a +b) - kp )
#             print("2")

#             x3 = p-3
#             y3 = cal(x3,a,b,p) # sqrt( sqrt( -9 -3a +b) - kp )
#             print("3")

#             x4 = p+3
#             y4 = cal(x4,a,b,p)# sqrt( sqrt( 9 + 3a +b) - kp )
#             print("4")

#             x6 = p-2
#             y6 = cal(x6,a,b,p)# sqrt( sqrt( 125 + 5a +b) - kp )
#             print("6")
            
#             x6 = p+2
#             y6 = cal(x6,a,b,p)# sqrt( sqrt( 125 + 5a +b) - kp )
#             print("6")

#             x7 = p+7
#             y7 = cal(x7,a,b,p)# sqrt( sqrt( 125 + 5a +b) - kp )
#             print("7")

#             x7 = p-7
#             y7 = cal(x7,a,b,p)# sqrt( sqrt( 125 + 5a +b) - kp )
#             print("7")
#     except :
#         print(i, 'break')
#         pass

# exit()
