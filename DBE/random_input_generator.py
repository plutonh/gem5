import random

data_random = open('/home/jonghyeon/gem5/DBE/random_data_10000.txt','w')

for i in range(10000):
    data =  "".join([str(random.randint(0, 1)) for j in range(8)]) # 1*8
    data_random.write(data+'\n')

data_random.close()