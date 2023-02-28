from sympy import re


def inversion(_data):
    for d in range(len(_data)):

        if _data[d] == 0:
            _data[d] = 1
        else:
            _data[d] = 0

    return _data

def calRatio(_after, _before):
    _ratio = _after / _before * 100

    return _ratio

def setDataset(_file):
    lines = _file.readlines()
    
    data_NRZ_set = []
    data_PAM4_set = []
    p = 0  #to confirm the input data
    _count = 0

    for i in range(len(lines)):
        # data for NRZ
        data_NRZ_ele = list(map(int,list(lines[i])[:8])) # 1*8
        data_NRZ_set.append(data_NRZ_ele)

        # data for PAM4
        if _count % 2 == 1: # i = 1, 3, 5, 7, ... -> skip
            _count = 0
            continue

        # i = 0, 2, 4, 6, ...
        data_PAM4_ele = [list(map(int,list(lines[i])[:8])),list(map(int,list(lines[i+1])[:8]))] # 2*8
        data_PAM4_set.append(data_PAM4_ele)
        _count += 1

        # # to confirm the data
        # if p <=4:
        #     print('line [', i, '] and [', i+1, ']th data is ',data_PAM4_ele)
        #     p += 1


    return data_NRZ_set, data_PAM4_set

def NRZ_experiment(_data_NRZ_set):
    # Initialization
    total_powerdc_no_NRZ = 0

    total_powerdc_1 = 0
    
    # do the experiment 1
    for data_NRZ in _data_NRZ_set:
        # non-encoded
        current_powerdc_no_NRZ = 1/100 * (8-sum(data_NRZ))
        total_powerdc_no_NRZ = total_powerdc_no_NRZ + current_powerdc_no_NRZ

        # encoded
        ### 1
        if sum(data_NRZ) <= 4:
            data_NRZ = inversion(data_NRZ)
        current_powerdc_1 = 1/100 * (8-sum(data_NRZ))
        total_powerdc_1 = total_powerdc_1 + current_powerdc_1
    
    power_ratio_1 = calRatio(total_powerdc_1, total_powerdc_no_NRZ)
    
    return power_ratio_1

def PAM4_experiment(_data_PAM4_set):
    # Initialization
    total_powerdc_no_PAM4 = 0

    total_powerdc_2 = 0
    total_powerdc_3 = 0
    total_powerdc_4 = 0

    num_flag = [0 for k in range(4)]

    ### Main Code ###
    for data_PAM4 in _data_PAM4_set:
        DBI_Flag = Flag(data_PAM4)
        DBI_Flag.countFlag()
        # print('Flags = ', DBI_Flag.Flags)

        # to count the total number of flag for each (00,01,10,11)
        for i in range(4):
            num_flag[i] = num_flag[i] + DBI_Flag.Flags[i]
        
        # non - encoded
        ### 2, 3, 4
        current_powerdc_no_PAM4 = DBI_Flag.calPower(0,1,2,3)
        total_powerdc_no_PAM4 = total_powerdc_no_PAM4 + current_powerdc_no_PAM4

        # encoded
        ### 2
        if 3 * DBI_Flag.Flags[0] + DBI_Flag.Flags[1] - DBI_Flag.Flags[2] - 3 * DBI_Flag.Flags[3] > 0:   # before power > after power => inversion
            total_powerdc_2 = total_powerdc_2 + DBI_Flag.calPower(3,2,1,0)
        else:
            total_powerdc_2 = total_powerdc_2 + DBI_Flag.calPower(0,1,2,3)
        

        ### 3
        changed_DBI_Flag = DBI_Flag.change_11()
        total_powerdc_3 = total_powerdc_3 + changed_DBI_Flag.calPower(0,1,2,3)
        
        ### 4
        sorted_DBI_Flag = DBI_Flag.sortFlags()
        total_powerdc_4 = total_powerdc_4 + sorted_DBI_Flag.calPower(0,1,2,3)

    power_ratio_2 = calRatio(total_powerdc_2, total_powerdc_no_PAM4)
    power_ratio_3 = calRatio(total_powerdc_3, total_powerdc_no_PAM4)
    power_ratio_4 = calRatio(total_powerdc_4, total_powerdc_no_PAM4)

    return power_ratio_2, power_ratio_3, power_ratio_4, num_flag

def printResult(_ratio, _num_flag, _num):
    print('######################### Result ', _num, '#########################') 
    for i in range(4):
        print('power_ratio_', i+1,' = ', _ratio[i] , '%')

    print("total number [00]: ", _num_flag[0], "  /  [01]: ",  _num_flag[1], "  /  [10]: ",  _num_flag[2], "  /  [11]: ",  _num_flag[3], "\n\n\n")
    
    return

# Flag : Calculate the number of 00/01/10/11  Data each for comparison
class Flag:
    def __init__(self,_data):
        self.Flags = [0 for j in range(4)]
        self.data = _data
        self.power = 0
        self.col = len(_data[0])
        self.row = len(_data)

    def countFlag(self):
        for i in range(self.col):
            if self.data[0][i] == 0 and self.data[1][i] == 0:        # <= 00
                self.Flags[0] = self.Flags[0] + 1
            elif self.data[0][i] == 0 and self.data[1][i] == 1:      # <= 01
                self.Flags[1] = self.Flags[1] + 1
            elif self.data[0][i] == 1 and self.data[1][i] == 0:      # <= 10
                self.Flags[2] = self.Flags[2] + 1
            else:                                          # <= 11
                self.Flags[3] = self.Flags[3] + 1

  
    def calPower(self,x,y,z,w):
        self.power = self.Flags[x]/100 + self.Flags[y]/112.5 + self.Flags[z]/180 + self.Flags[w]*0
    
        return self.power

    def change_11(self):
        maxIndex = self.Flags.index(max(self.Flags))
        flag_11 = self.Flags[3]
        self.Flags[3] = self.Flags[maxIndex]
        self.Flags[maxIndex] = flag_11
        
        return self
        

    def sortFlags(self):
        self.Flags.sort()
        
        return self


# read files
data_1_bin = open("/home/youri/project/gem5/DBI/DATA_input/basicmath_large_bin.txt","r")
data_2_bin = open("/home/youri/project/gem5/DBI/DATA_input/basicmath_small_bin.txt","r")
data_3_bin = open("/home/youri/project/gem5/DBI/DATA_input/bitcount_bitcnts_bin.txt","r")
data_4_bin = open("/home/youri/project/gem5/DBI/DATA_input/qsort_large_bin.txt","r")
data_5_bin = open("/home/youri/project/gem5/DBI/DATA_input/qsort_small_bin.txt","r")
data_6_bin = open("/home/youri/project/gem5/DBI/DATA_input/susan_large_smoothing_bin.txt","r")
data_7_bin = open("/home/youri/project/gem5/DBI/DATA_input/susan_small_smoothing_bin.txt","r")
data_8_bin = open("/home/youri/project/gem5/DBI/DATA_input/FFT_bin.txt","r")
data_random = open("/home/youri/project/gem5/DBI/DATA_input/random_data_10000.txt","r")
data_000 = open("/home/youri/project/gem5/DBI/DATA_input/test000.txt")


def doExperiment(_file,_num):
    data_NRZ_set, data_PAM4_set = setDataset(_file)
    print('\n\ndata for experiment', _num, 'is ready!\n')

    print('********************* start experiment ', _num, ' *********************')
    power_ratio_1 = NRZ_experiment(data_NRZ_set)
    power_ratio_2, power_ratio_3, power_ratio_4, num_flag = PAM4_experiment(data_PAM4_set)
    ratio = [power_ratio_1, power_ratio_2, power_ratio_3, power_ratio_4]

    printResult(ratio, num_flag,_num)


doExperiment(data_1_bin,1)
# doExperiment(data_2_bin,2)
# doExperiment(data_3_bin,3)
# doExperiment(data_4_bin,4)
# doExperiment(data_5_bin,5)
# doExperiment(data_6_bin,6)
# doExperiment(data_7_bin,7)
# doExperiment(data_8_bin,8)
# doExperiment(data_random,9)
# doExperiment(data_000,10)




data_1_bin.close()
data_2_bin.close()
data_3_bin.close()
data_4_bin.close()
data_5_bin.close()
data_6_bin.close()
data_7_bin.close()
data_8_bin.close()
data_random.close()
data_000.close()

print('\n\n\nclear!!!')