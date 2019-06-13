#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


#define NPTS 5
#define flagSZ 5

/* Ciphertexts */
/* Each round has 5 ciphertext, and remaining is encrypted flag */
uint32_t cts[NPTS * 5 + flagSZ][2][2] = {
{ {0xd51cd761, 0x38f5dde5}, {0xf9e58398, 0xf9ecf6d2} },
{ {0x0745c161, 0x2ef38ca0}, {0x274da856, 0x1bd1ed77} },
{ {0x9124a4a5, 0x5ed2c9aa}, {0xf13c7cfd, 0xdbe96f09} },
{ {0xd24e818a, 0x6e9ee115}, {0xb25629a1, 0x6f295f04} },
{ {0xb72009c5, 0xe0ebd655}, {0xd738d12e, 0xfc179f7a} },
{ {0x49446b7d, 0x7a8f9193}, {0x29e40977, 0xcc961d79} },
{ {0x91169352, 0x7a55448d}, {0xbab97d69, 0x383d4fcc} },
{ {0x96ddf463, 0x0b1f7059}, {0x97ba72f9, 0x39bacfab} },
{ {0x39fc490f, 0x7069b595}, {0xa25eb233, 0x1db81c0c} },
{ {0xf4792d36, 0x52ab38ca}, {0xd2259e89, 0xf337ab87} },
{ {0xab8eb9d6, 0xfafe1061}, {0xedf217f0, 0x350b2056} },
{ {0x9ee4e086, 0x6d8ac80f}, {0x9833e9b7, 0x5686cbff} },
{ {0x62c46852, 0x5a7a5bdd}, {0xade9e0bf, 0xfe66d06c} },
{ {0xece6ce88, 0x0f26f1f2}, {0x83ee135d, 0x33b17692} },
{ {0x626b79f7, 0xa75a8ca5}, {0xfc663609, 0x7cfe0ad5} },
{ {0xaf117df6, 0x71d3d779}, {0x887abb59, 0xd024846c} },
{ {0x173fbb04, 0xe8da3542}, {0xf4d2d829, 0xecd50de2} },
{ {0x21f9dfa1, 0xdbb1fd5b}, {0x66e276b0, 0xc6ff1462} },
{ {0x7e21830a, 0xca8d459e}, {0x4d07f93a, 0x27b16ee6} },
{ {0x4f6fc0e5, 0xa04d1764}, {0x0e4bd35d, 0x2954ce09} },
{ {0x81e403a6, 0xa5ae97f1}, {0x8741b4c8, 0x8ab19d20} },
{ {0xf5a57382, 0xcde0016d}, {0xfaf1f7e2, 0xd7d51984} },
{ {0x5d2f2df9, 0x0084befc}, {0xdbeac6e3, 0x0f8dd9a4} },
{ {0xa754be5e, 0x662eb507}, {0x12fb3cc8, 0x2909fee8} },
{ {0xc46be9e0, 0x238ad296}, {0xee1d2da5, 0xfbecbf42} },
{ {0x833f8a11, 0x1f7c6138}, {0x833f8a11, 0x1f7c6138} },
{ {0x504d1cc8, 0x4165e486}, {0x504d1cc8, 0x4165e486} },
{ {0x1f0dd8b1, 0xa948aa6c}, {0x1f0dd8b1, 0xa948aa6c} },
{ {0xa3b1396a, 0x8b4343c1}, {0xa3b1396a, 0x8b4343c1} },
{ {0xe83bec46, 0xaea7f281}, {0xe83bec46, 0xaea7f281} },
};


/* Plaintext */
uint32_t pts[NPTS * 5][2][2] = {
{ {0xedcef72a, 0x657e53d9}, {0xedcef72a, 0x657ed359} },
{ {0x7a23d9be, 0xb5cbd626}, {0x7a23d9be, 0xb5cb56a6} },
{ {0xb985bcd9, 0xabd9f8e1}, {0xb985bcd9, 0xabd97861} },
{ {0xf2e781ca, 0xce155909}, {0xf2e781ca, 0xce15d989} },
{ {0xf2115b33, 0x2bc6c1d2}, {0xf2115b33, 0x2bc64152} },
{ {0x17c9e836, 0x62787b84}, {0x17c968b6, 0x6278fb04} },
{ {0xcec7c576, 0x41035b8a}, {0xcec745f6, 0x4103db0a} },
{ {0x2245fdf4, 0x7d53a40a}, {0x22457d74, 0x7d53248a} },
{ {0xb80e1745, 0x9cd3e26c}, {0xb80e97c5, 0x9cd362ec} },
{ {0x2c2f1276, 0x6cc00483}, {0x2c2f92f6, 0x6cc08403} },
{ {0x66fafe55, 0xbae6660e}, {0x64fafe55, 0xb8e6660e} },
{ {0xf493f761, 0x6706298f}, {0xf693f761, 0x6506298f} },
{ {0xb38a2a41, 0xb7947d5d}, {0xb18a2a41, 0xb5947d5d} },
{ {0xab0910cf, 0x8f198c3c}, {0xa90910cf, 0x8d198c3c} },
{ {0xca91b17b, 0x5766ebb8}, {0xc891b17b, 0x5566ebb8} },
{ {0x917212d8, 0xa43b09e1}, {0x8288ec9a, 0xb5c1f7a3} },
{ {0x6a27e7be, 0x1720eb47}, {0xed074c96, 0x9200406f} },
{ {0x2e2add36, 0xc7053563}, {0x78d12981, 0x93fec1d4} },
{ {0x50b3e02e, 0x67d16922}, {0x66ae07c8, 0x53cc8ec4} },
{ {0x4a894251, 0x577a3363}, {0xa125504d, 0xbed6217f} },
{ {0xff40eb87, 0x446e0f88}, {0x656537e4, 0x7b0acd29} },
{ {0x21d5e9a4, 0x62823045}, {0xe1369771, 0x8cebeab9} },
{ {0x2f99b639, 0x1b4a07ce}, {0xac7ab269, 0xaa93db7e} },
{ {0x5535d05d, 0x0918897e}, {0xd76a1406, 0x5c5c48bc} },
{ {0x6c268c5e, 0x63fdd964}, {0x9526c36a, 0x868d6ca5} },
};


/* DEBUG key oracle */
uint32_t ks[6] = {
0x02e774ec,
0xe0d3afe5,
0x77623d9a,
0x529c8c48,
0x709b3792,
0xbf416731,
};


/* Non-linear Function */
inline uint8_t gbox (uint8_t a, uint8_t b, uint8_t mode) {
    uint8_t x = a + b + mode;
    return (x << 2) | (x >> 6);
}


/* Feistel Function */
uint32_t fbox (uint32_t plain) {
    uint8_t p0 = plain;
    uint8_t p1 = plain >> 8;
    uint8_t p2 = plain >> 16;
    uint8_t p3 = plain >> 24;
    uint8_t t0 = p2 ^ p3;
    uint8_t y1 = gbox(p0 ^ p1, t0, 1);
    uint8_t y0 = gbox(p0, y1, 0);
    uint8_t y2 = gbox(t0, y1, 0);
    uint8_t y3 = gbox(p3, y2, 1);
    return ((uint32_t) y0 << 24) | ((uint32_t) y1 << 16) | ((uint32_t) y2 << 8) | y3;
}


void printcts() {
    for (int i=0; i<NPTS * 5 + flagSZ; i++) {
        uint32_t l0 = cts[i][0][0];
        uint32_t r0 = cts[i][0][1];
        uint32_t l1 = cts[i][1][0];
        uint32_t r1 = cts[i][1][1];
        printf("(%08x, %08x), (%08x, %08x)\n", l0, r0, l1, r1);
    }
}


int main() {
    /* Undo last xor */
    for (int i=0; i<NPTS * 5 + flagSZ; i++) {
        for (int j=0; j<2; j++) {
            uint32_t tmp = cts[i][j][0] ^ cts[i][j][1];
            cts[i][j][1] = cts[i][j][0];
            cts[i][j][0] = tmp;
        }
    }

    printcts();

    for (int round=0; round<4; round++) {
        uint32_t roundkey = 0;

        /* Search subkey */
        #pragma omp parallel for
        for (uint32_t k=0; k<0xffffffff; k++) {
        // for (uint32_t k=ks[3]; k<ks[3] + 1; k++) {
        // for (uint32_t k=ks[3] - 1000; k<ks[3] + 1000; k++) {
            int pass = 1;
            for (int i=0; i<NPTS; i++) {
                uint32_t l0 = cts[i + round * NPTS][0][0];
                uint32_t r0 = cts[i + round * NPTS][0][1];
                uint32_t l1 = cts[i + round * NPTS][1][0];
                uint32_t r1 = cts[i + round * NPTS][1][1];
                uint32_t z0 = l0 ^ fbox(r0 ^ k);
                uint32_t z1 = l1 ^ fbox(r1 ^ k);
                if ((z0 ^ z1) != 0x02000000) {
                    pass = 0;
                    break;
                }
            }
            if (pass) {
                if (k != ks[3 - round]) {
                    printf("QAQQQ: %08x != %08x\n", k, ks[3 - round]);
                } else {
                    printf("Found: %08x\n", k);
                }
                roundkey = k;
            }
        }
        puts("");
        
        /* Decrypt this round */
        for (int i=0; i<NPTS * 5 + flagSZ; i++) {
            for (int j=0; j<2; j++) {
                uint32_t tmp = cts[i][j][0] ^ fbox(cts[i][j][1] ^ roundkey);
                // uint32_t tmp = cts[i][j][0] ^ fbox(cts[i][j][1] ^ ks[3 - round]);
                cts[i][j][0] = cts[i][j][1];
                cts[i][j][1] = tmp;
            }
        }

        printcts();
    }

    /* Undo first xor */
    for (int i=0; i<NPTS * 5 + flagSZ; i++) {
        for (int j=0; j<2; j++) {
            uint32_t tmp = cts[i][j][0] ^ cts[i][j][1];
            cts[i][j][1] = tmp;
        }
    }

    /* Input subkey pair */
    uint32_t k4 = pts[0][0][0] ^ cts[0][0][0];
    uint32_t k5 = pts[0][0][1] ^ cts[0][0][1];
    for (int i=0; i<NPTS * 5 + flagSZ; i++) {
        for (int j=0; j<2; j++) {
            cts[i][j][0] = cts[i][j][0] ^ k4;
            cts[i][j][1] = cts[i][j][1] ^ k5;
        }
    }

    /* Check input subkey pair */
    for (int i=0; i<NPTS * 5; i++) {
        for (int j=0; j<2; j++) {
            if (cts[i][j][0] != pts[i][j][0]) {
                puts("QAQQQQQQQQ");
                exit(255);
            }
            if (cts[i][j][1] != pts[i][j][1]) {
                puts("QAQQQQQQQQ2");
                exit(255);
            }
        }
    }

    /* Print flag !!!!!!!! */
    for (int i=0; i<flagSZ; i++) {
        char buf[5] = {0};
        *((uint32_t*) buf) = cts[i+NPTS*5][0][0];
        printf("%s", buf);
        *((uint32_t*) buf) = cts[i+NPTS*5][0][1];
        printf("%s", buf);
    }
}
