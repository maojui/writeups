## 04Hastad’s Broadcast Attack_1 :

```
from cryptools.rsa import *
n2s(nroot(hastad_broadcast([j1['c'],j2['c'],j3['c'],j4['c'],j5['c'],j6['c'],j7['c']],[j1['n'],j2['n'],j3['n'],j4['n'],j5['n'],j6['n'],j7['n']]),7))
```
`Flag : CTF{Hastad's Broadcast Attack & Chinese Remainder Theorem}`

## 04Hastad’s Broadcast Attack_2 :

```
n2s(nroot(hastad_broadcast([C,C2,C3],[N,N2,N3]),3))
```
`Flag : key=bff149a0b87f5b0e00d9dd364e9ddaa0`

## 04Hastad’s Broadcast Attack_3 :

```
n2s(nroot(hastad_broadcast([c1,c2,c3],[n1,n2,n3]),3))
```
`Flag : broadcast_with_small_e_is_killer_40332300191`

## 04Hastad’s Broadcast Attack_4 :

```
n2s(nroot(hastad_broadcast([c1,c2,c3],[n1,n2,n3]),3))
```
`Flag : theoretical_computer_scientist_johan_torkel_hastad`

