import numpy as np

LENGTH = 1024

# FLAG = 'AIS3{EveryONe_kn0w_Quan7um_k3Y_Distr1but1on--BB84}'
FLAG = 0b0100000101001001010100110011001101111011010001010111011001100101011100100111100101001111010011100110010101011111011010110110111000110000011101110101111101010001011101010110000101101110001101110111010101101101010111110110101100110011010110010101111101000100011010010111001101110100011100100011000101100010011101010111010000110001011011110110111000101101001011010100001001000010001110000011010001111101

def measure(qubits, basis):
    bit_stream = ""
    for q, b in zip(qubits, basis):
        if b == 'x':
            q *= complex(0.707, -0.707)
        bit_stream += str(np.random.choice([0,1], p=[round(pow(q.real, 2),1), round(pow(q.imag, 2),1)]))
    return bit_stream


def key_exchange(qubits, basisA, basisB) :
    measured_bits = measure(qubits, basisA)
    bs = ''
    for i in range(LENGTH) :
        if basisA[i] == basisB[i] :
            bs += measured_bits[i]
    return bs