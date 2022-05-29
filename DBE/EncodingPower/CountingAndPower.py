import sys

sys.stdout = open('/home/youri/project/gem5/DBE/ExperimentResults.txt', 'w')

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

def calCharging(_after, _before):
    charging = 0
    diff = _after - _before
    # print('diff = ', diff)
    if diff == 1:
        charging = 1/6
    elif diff == 2:
        charging = 1/3
    elif diff == 3:
        charging = 1/2

    return charging

def sortCompare(_origin, _sorted):
    _cList = [] # to store the index if it is changed : [index, diff]
    # print('origin = ', _origin)
    # print('sorted = ', _sorted)
    for _index in range(4):
        _sortedIndex = _sorted.index(_origin[_index])
        if (_origin[_index] != _sorted[_index]) and (_sortedIndex > _index):
            _diff = _sortedIndex - _index
            _cList.append([_sortedIndex, _diff])
    # print('cList = ', _cList)

    return _cList

def copyInit(_originFlag):
    iniFlags = []
    for i in _originFlag:
        iniFlags.append(i)
    # print('iniFlags = ', iniFlags)

    return iniFlags

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
            else:                                                    # <= 11
                self.Flags[3] = self.Flags[3] + 1

  
    def calPower(self,x,y,z,w):
        self.power = self.Flags[x]/100 + self.Flags[y]/112.5 + self.Flags[z]/180 + self.Flags[w]*0
    
        return self.power

    def change_11(self):
        maxIndex = self.Flags.index(max(self.Flags))
        flag_11 = self.Flags[3]
        self.Flags[3] = self.Flags[maxIndex]
        self.Flags[maxIndex] = flag_11
        
        return self, maxIndex
        

    def sortFlags(self):
        self.Flags.sort()
        
        return self

        


# read files
data_1_bin = open("/home/youri/project/gem5/DBE/DATA_input/1_bin.txt","r")
data_2_bin = open("/home/youri/project/gem5/DBE/DATA_input/2_bin.txt","r")
data_3_bin = open("/home/youri/project/gem5/DBE/DATA_input/3_bin.txt","r")
data_4_bin = open("/home/youri/project/gem5/DBE/DATA_input/4_bin.txt","r")
data_5_bin = open("/home/youri/project/gem5/DBE/DATA_input/5_bin.txt","r")
data_6_bin = open("/home/youri/project/gem5/DBE/DATA_input/6_bin.txt","r")
data_7_bin = open("/home/youri/project/gem5/DBE/DATA_input/7_bin.txt","r")
data_8_bin = open("/home/youri/project/gem5/DBE/DATA_input/8_bin.txt","r")
data_9_bin = open("/home/youri/project/gem5/DBE/DATA_input/9_bin.txt","r")
data_10_bin = open("/home/youri/project/gem5/DBE/DATA_input/10_bin.txt","r")
data_11_bin = open("/home/youri/project/gem5/DBE/DATA_input/11_bin.txt","r")
data_12_bin = open("/home/youri/project/gem5/DBE/DATA_input/12_bin.txt","r")
data_13_bin = open("/home/youri/project/gem5/DBE/DATA_input/13_bin.txt","r")
data_14_bin = open("/home/youri/project/gem5/DBE/DATA_input/14_bin.txt","r")
data_random = open("/home/youri/project/gem5/DBE/DATA_input/random_data_10000.txt","r")

def doExperiment(_file,_num):
    print('********************* start experiment ', _num, ' *********************')
    # Initialization
    total_powerdc_no_NRZ = 0
    total_powerdc_no_PAM4 = 0

    total_powerdc_1 = 0
    total_powerdc_2 = 0
    total_powerdc_3 = 0
    total_powerdc_4 = 0

    num_flag = [0 for k in range(4)]

    const = 15 * 3.3 * 10e-6 # 15pF * 3.3GHz * (1V)^2

    print('start experiment',_num)
    _count = 0
    charging_1 = 0
    charging_2 = 0
    charging_3 = 0
    charging_4 = 0
    lines = _file.readlines()

    # p = 0

    for i in range(len(lines)):
        # data for NRZ
        data_NRZ = list(map(int,list(lines[i])[:8])) # 1*8

        # non - encoded
        ### 1
        current_powerdc_no_NRZ = 1/100 * (8-sum(data_NRZ))
        total_powerdc_no_NRZ = total_powerdc_no_NRZ + current_powerdc_no_NRZ

        # encoded
        ### 1
        if sum(data_NRZ) <= 4:
            charging_1 = charging_1 + (8 - sum(data_NRZ))
            inversion(data_NRZ)
        current_powerdc_1 = 1/100 * (8-sum(data_NRZ))
        total_powerdc_1 = total_powerdc_1 + current_powerdc_1

        # data for PAM4
        if _count % 2 == 1:
            _count = 0
            continue
        data_PAM4 = [list(map(int,list(lines[i])[:8])),list(map(int,list(lines[i+1])[:8]))] # 2*8
        # if p <=4:
        #     print(data_PAM4)
        #     print(i)
        #     p += 1



        ### Main Code ###
        DBI_Flag = Flag(data_PAM4)
        DBI_Flag.countFlag()

        # to count the total number of flag for each (00,01,10,11)
        for i in range(4):
            num_flag[i] = num_flag[i] + DBI_Flag.Flags[i]
        
        # non - encoded
        ### 2, 3, 4
        current_powerdc_no_PAM4 = DBI_Flag.calPower(0,1,2,3)
        total_powerdc_no_PAM4 = total_powerdc_no_PAM4 + current_powerdc_no_PAM4

        # encoded
        DBI_Flag_Origin = copyInit(DBI_Flag.Flags) # to store the initial state
        # print('DBI_Flag_Origin = ', DBI_Flag_Origin)

        ### 2
        if 3 * DBI_Flag.Flags[0] + DBI_Flag.Flags[1] - DBI_Flag.Flags[2] - 3 * DBI_Flag.Flags[3] > 0:   # before power > after power => inversion
            total_powerdc_2 = total_powerdc_2 + DBI_Flag.calPower(3,2,1,0)
            charging_2 = charging_2 + calCharging(3,0) * DBI_Flag.Flags[0] + calCharging(2,1) * DBI_Flag.Flags[1] ## 00 -> 11 and 01 -> 10
            # print('charging_2 = ', charging_2)
            # print('DBI_Flag.Flags[0] = ',DBI_Flag.Flags[0])
            # print('calCharging(3,0) = ',calCharging(3,0))
        else:
            total_powerdc_2 = total_powerdc_2 + DBI_Flag.calPower(0,1,2,3)
        # print('after 2 = ', DBI_Flag.Flags)
        ### 3
        changed_DBI_Flag, maxIndex = DBI_Flag.change_11()
        # print('change_11 =', DBI_Flag.Flags)
        total_powerdc_3 = total_powerdc_3 + changed_DBI_Flag.calPower(0,1,2,3)
        # print(DBI_Flag.Flags)
        charging_3 = charging_3 + calCharging(3,maxIndex) * DBI_Flag.Flags[3]
        # print(calCharging(3,maxIndex))
        ### 4
        sorted_DBI_Flag = DBI_Flag.sortFlags()
        # print('sorted4 = ',DBI_Flag.Flags)
        total_powerdc_4 = total_powerdc_4 + sorted_DBI_Flag.calPower(0,1,2,3)
        # print('DBI_Flag_Origin', DBI_Flag_Origin)
        cList = sortCompare(DBI_Flag_Origin, sorted_DBI_Flag.Flags)
        for i in range(len(cList)):
            charging_4 = charging_4 + calCharging(cList[i][1], 0) * DBI_Flag.Flags[cList[i][0]]
        _count = 1
        # print('\n\n\n\n\n')

    # Ratio
    print('######################### Result ', _num, '#########################') 
    ### 1
    power_ratio_1 = calRatio(total_powerdc_1, total_powerdc_no_NRZ)
    print('power_ratio_1 =', power_ratio_1, '%')
    ### 2
    power_ratio_2 = calRatio(total_powerdc_2, total_powerdc_no_PAM4)
    print('power_ratio_2 =', power_ratio_2, '%')
    ### 3
    power_ratio_3 = calRatio(total_powerdc_3, total_powerdc_no_PAM4)
    print('power_ratio_3 =', power_ratio_3, '%')
    ### 4
    power_ratio_4 = calRatio(total_powerdc_4, total_powerdc_no_PAM4)
    print('power_ratio_4 =', power_ratio_4, '%')
    
    print("total number [00]: ", num_flag[0], "  /  [01]: ",  num_flag[1], "  /  [10]: ",  num_flag[2], "  /  [11]: ",  num_flag[3], "\n")
    print("if we calculate as a percentage,")
    total_flag = sum(num_flag)
    print("total number [00]: ", num_flag[0] / total_flag * 100, "%  /  [01]: ",  num_flag[1] / total_flag * 100, "%  /  [10]: ",  num_flag[2] / total_flag * 100, "%  /  [11]: ",  num_flag[3] / total_flag * 100, "%\n\n\n")
    
    # Power
    print("******************  SWITCHING POWER  ******************\n\n\n")
    print("NRZ-DBI Power = ", charging_1 * const, "W")
    print("PAM4-DBI Power = ", charging_2 * const, "W")
    print("PAM4-MF Power = ", charging_3 * const, "W")
    print("PAM4-Sort Power = ", charging_4 * const, "W\n\n\n\n\n")


doExperiment(data_1_bin,1)
doExperiment(data_2_bin,2)
doExperiment(data_3_bin,3)
doExperiment(data_4_bin,4)
doExperiment(data_5_bin,5)
doExperiment(data_6_bin,6)
doExperiment(data_7_bin,7)
doExperiment(data_8_bin,8)
doExperiment(data_9_bin,9)
doExperiment(data_10_bin,10)
doExperiment(data_11_bin,11)
doExperiment(data_12_bin,12)
doExperiment(data_13_bin,13)
doExperiment(data_14_bin,14)
doExperiment(data_random,15)




data_1_bin.close()
data_2_bin.close()
data_3_bin.close()
data_4_bin.close()
data_5_bin.close()
data_6_bin.close()
data_7_bin.close()
data_8_bin.close()
data_9_bin.close()
data_10_bin.close()
data_11_bin.close()
data_12_bin.close()
data_13_bin.close()
data_14_bin.close()
data_random.close()

print('clear')

sys.stdout.close()