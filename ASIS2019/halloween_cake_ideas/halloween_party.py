#!/usr/bin/env python

from fastecdsa.curve import Curve
from fastecdsa.point import Point
from Crypto.Util.number import *
from secret import EC_params, flag, Q



p, a, b, q, Px, Py = EC_params
C = Curve('halloween', p, a, b, q, Px, Py)
P = Point(Px, Py, curve = C)
P1 = Point(p + 1, 467996041489418065436268622304855825266338280723, curve = C)
P2 = Point(p - 1, 373126988100715326072483107245781156204485119489, curve = C)
P3 = Point(p + 3, 245091091146774561796627894715885724307214901148, curve = C)


assert ((9<<8>>4<<9<<12<<6>>9>>2<<5>>3>>4>>8<<12>>1>>5>>7<<13>>12>>12) * P).x == Q.x
assert bytes_to_long(flag) == P.x
assert ((-1) * Q).y == 621803439821606291947646422656643138592770518069