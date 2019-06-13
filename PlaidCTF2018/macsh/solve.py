from pwn import *
conn = remote('macsh.chal.pwning.xxx',64791)
conn.recv()

def send_command(cmd):
    conn.sendline('mac <|> tag '+'a'*2048 + cmd.rjust(4,' '))
    t1 = int(conn.recvuntil('\n')[:-1],16)
    conn.recv()
    assert len(cmd)!= 5, 'sorry, this function can\'t do this.'
    if len(cmd) > 5 :
        echo = 'echo ' + 'a'*(len(cmd)-5)
    else :
        echo = 'echo'
    conn.sendline('mac <|> tag '+'a'*2048 + echo)
    t2 = int(conn.recvuntil('\n')[:-1],16)
    conn.recv()

    conn.sendline('mac <|> tag '+echo)
    t3 = int(conn.recvuntil('\n')[:-1],16)
    conn.recv()
    conn.sendline('{}<|>{}'.format(hex(t1^t2^t3)[2:],cmd.rjust(4,' ')))
    print(conn.recv())


send_command('pwd')
send_command('ls .')
send_command('cat flag.txt')


