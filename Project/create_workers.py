__author__ = 'omrim'
my_list = [1]*3 + [0]
for e in range(10):
    print('w' + str(e) + '=[' , end=''),
    for d in range(1,8):
        print('[', end=''),
        for s in range(1,3):
            x = random.choice(my_list)
            print(str(x) + ',', end='')
        x = random.choice(my_list)
        print(str(x) + ']', end='')
        if d<7:
            print(',', end='')
    print(']')