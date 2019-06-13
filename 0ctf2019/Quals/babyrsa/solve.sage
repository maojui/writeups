from pubkey import P, n, e

R.<a> = GF(2^2049)

# Factoring
f = factor(n)
(p, _), (q, _) = f
np = pow(2,p.degree())
nq = pow(2,q.degree())
phi = (np-1)*(nq-1)
d = inverse_mod(31337, phi)

# Load data
with open('flag.enc', 'rb') as f:
    enc = f.read()

c_int = Integer(enc.encode('hex'), Integer(16))
c_poly = P(R.fetch_int(c_int))

# Decrypt
m_poly = pow(c_poly, d, n)
m_int = R(m_poly).integer_representation()
print(hex(m)[2:-1].decode('hex'))

# flag{P1ea5e_k33p_N_as_A_inTegeR~~~~~~}