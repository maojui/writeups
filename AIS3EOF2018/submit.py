#!/usr/bin/env python3

import requests

flags = [
    'EOF{task1}',
    'EOF{task2}',
    'EOF{task3}',
]

for flag in flags:
    re = requests.get("http://10.140.0.8/submit?token=zFErzItq&flag={}".format(flag))
    print(re.text)