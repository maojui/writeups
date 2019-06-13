

def submit(flag):
    import os
    token = '294d34acf11783a50f0fe3a51db8aef4'
    os.system("curl 'http://10.10.10.1/team/submit_key?token={}&key={}'".format(token,flag))
