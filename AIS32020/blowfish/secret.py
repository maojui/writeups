import pickle

FLAG = 'AIS3{ATk_BloWf1sH-CTR_by_b1t_Flipping_^_^}'

if __name__ == "__main__":
    user = [
        {'name': 'maojui', 'password': 'SECRET', 'admin':False},
        {'name': 'djosix', 'password': 'S3crE7', 'admin':False},
        {'name': 'kaibro', 'password': 'GGInIn', 'admin':False},
        {'name': 'others', 'password': '_FLAG_', 'admin':False},
    ]
    p = open('user.pickle', 'wb')
    pickle.dump(user, p)
    p.close()