start = 2048
now = 0
while start:
    print ('[+] ', start)
    start_exp = 1 << start
    tmp = now | start_exp
    ret = phi(tmp)
    if ret == tmp:
        # tmp < d
        now |= start_exp
    elif ret == 0:
        # tmp == d
        now |= start_exp
        print ('d = ', now)
        break
    else:
        # tmp > d
        pass
    start -= 1

