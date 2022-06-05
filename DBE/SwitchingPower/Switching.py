import sys

sys.stdout = open('/home/youri/project/gem5/DBE/SwitchingExperimentResults.txt', 'w')

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

# to store the initial value
def copyInit(_originFlag):
    iniFlags = []
    for i in _originFlag:
        iniFlags.append(i)
    # print('iniFlags = ', iniFlags)

    return iniFlags

# to calculate the switching power of NRZ data
def switchingNRZ(_prev_NRZ, _cur_NRZ):
    charging = 0
    for i in range(8):
        if _prev_NRZ[i] == 0 and _cur_NRZ[i] == 1:
            charging = charging + 1

    return charging

def bin2int(_data_PAM4_1, _data_PAM4_2):
    if _data_PAM4_1 == 0 and _data_PAM4_2 == 0:     # <= 00
        _int = 0
    elif _data_PAM4_1 == 0 and _data_PAM4_2 == 1:    # <= 01
        _int = 1
    elif _data_PAM4_1 == 1 and _data_PAM4_2 == 0:    # <= 10
        _int = 2
    else:                                            # <= 11
        _int = 3
    
    return _int

# to calculate the switching power of PAM4 data
def switchingPAM4(_prev_PAM4, _cur_PAM4):
    charging = 0
    for i in range(8):
        _int_prev = bin2int(_prev_PAM4[0][i], _prev_PAM4[1][i])
        _int_cur = bin2int(_cur_PAM4[0][i], _cur_PAM4[1][i])
        # calculate the amount of charging
        diff = _int_cur - _int_prev
        if diff == 1:
            newCharging = 1/6
        elif diff == 2:
            newCharging = 1/3
        elif diff == 3:
            newCharging = 1/2
        else:
            newCharging = 0
        charging = charging + newCharging

    return charging

 # PAM4-DBI
def enc_PAM4_DBI(_PAM4_data):
    _encoded = _PAM4_data  # 2*8
    for i in range(8):
        if _PAM4_data[0][i] == 0 and _PAM4_data[1][i] == 0:       # <= 00
            _encoded[0][i] == 1 and _encoded[1][i] == 1
        elif _PAM4_data[0][i] == 0 and _PAM4_data[1][i] == 1:     # <= 01
            _encoded[0][i] == 1 and _encoded[1][i] == 0
        elif _PAM4_data[0][i] == 1 and _PAM4_data[1][i] == 0:     # <= 10
            _encoded[0][i] == 0 and _encoded[1][i] == 1
        else:                                                     # <= 11
            _encoded[0][i] == 0 and _encoded[1][i] == 0

    return _encoded

 # PAM4-MF
def enc_PAM4_MF(_PAM4_data, _max_Index):
    _encoded = _PAM4_data
    # what is the most frequent?
    if _max_Index == 0:
        _fir = 0
        _sec = 0
    elif _max_Index == 1:
        _fir = 0
        _sec = 1
    elif _max_Index == 2:
        _fir = 1
        _sec = 0

    for i in range(8):
        if _PAM4_data[0][i] == _fir and _PAM4_data[1][i] == _sec:   # frequent case => 11
            _encoded[0][i] = 1
            _encoded[1][i] = 1
        elif _PAM4_data[0][i] == 1 and _PAM4_data [1][i] == 1:       # 11 => frequenct case
            _encoded[0][i] = _fir
            _encoded[1][i] = _sec

    return _encoded

def sortCompare(_origin, _sorted):
    _cList = [] # to store the index if it is changed : [before, after]
    # print('origin = ', _origin)
    # print('sorted = ', _sorted)
    for _index in range(4):
        _sortedIndex = _sorted.index(_origin[_index]) # where it is in the sorted list
        if _origin[_index] != _sorted[_index]: # if it is not same
            _cList.append([_index, _sortedIndex])
    
    return _cList

def int2bin(_cList_ele):  # element list in _cList
    # before
    if _cList_ele[0] == 0:     # before = 00
        _bFir = 0
        _bSec = 0
    elif _cList_ele[0] == 1:    # before = 01
        _bFir = 0
        _bSec = 1
    elif _cList_ele[0] == 2:    # before = 10
        _bFir = 1
        _bSec = 0
    elif _cList_ele[0] == 3:    # before = 11
        _bFir = 1
        _bSec = 1
    
    # after
    if _cList_ele[1] == 0:     # after = 00
        _aFir = 0
        _aSec = 0
    elif _cList_ele[1] == 1:    # after = 01
        _aFir = 0
        _aSec = 1
    elif _cList_ele[1] == 2:    # after = 10
        _aFir = 1
        _aSec = 0
    elif _cList_ele[1] == 3:    # after = 11
        _aFir = 1
        _aSec = 1
    
    return _bFir, _bSec, _aFir, _aSec

# PAM4-Sort
def enc_PAM4_sort(_data_PAM4, _cList):
    _encoded = _data_PAM4
    for i in range(len(_cList)):
        bFir, bSec, aFir, aSec = int2bin(_cList[i])
        for j in range(8):
            if _data_PAM4[0][j] == bFir and _data_PAM4[1][j] == bSec:
                _encoded[0][j] = aFir
                _encoded[1][j] = aSec

    return _encoded



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

    print('start experiment',_num)
    _count = 0

    # charging
    charging_1 = 0
    charging_2 = 0
    charging_3 = 0
    charging_4 = 0
    
    # lines
    lines = _file.readlines()

    # cosnt
    const_NRZ = 15 * 3.3 * 10e-3 / ((len(lines) - 1) * 8) # 15pF * 3.3GHz * (1V)^2
    const_PAM4 = 15 * 3.3 * 10e-3 / (((len(lines)/2) - 1) * 8) # 15pF * 3.3GHz * (1V)^2

    print('experiment ', _num, 'has ', len(lines), 'NRZ words and ', len(lines)/2, 'PAM4 words')

    example_1 = 0
    example_2 = 0

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
            inversion(data_NRZ)
            if example_1 < 3:
                print('#1 NRZ-DBI')
                print(lines[i], ' encoded to ', data_NRZ)
        elif example_1 < 3:
            print('#1 NRZ-DBI')
            print(lines[i], " nothing has been changed")
        ### 1 swithcing
        if i == 0: # first data
            prev_NRZ = data_NRZ
            print('first data: ', prev_NRZ)
        else:
            current_NRZ = data_NRZ
            newCharging_1 = switchingNRZ(prev_NRZ, current_NRZ)
            charging_1 = charging_1 + newCharging_1
            if example_1 < 3:
                print('prev_NRZ =', prev_NRZ)
                print('current_NRZ = ', current_NRZ)
                print('newCharging = ', newCharging_1)
            prev_NRZ = current_NRZ

        current_powerdc_1 = 1/100 * (8-sum(data_NRZ))
        total_powerdc_1 = total_powerdc_1 + current_powerdc_1

        example_1 += 1

        # data for PAM4
        if _count % 2 == 1:
            _count = 0
            continue
        data_PAM4 = [list(map(int,list(lines[i])[:8])),list(map(int,list(lines[i+1])[:8]))] # 2*8

        ### Main Code ###
        DBI_Flag = Flag(data_PAM4)
        DBI_Flag.countFlag()

        # to count the total number of flag for each (00,01,10,11)
        for k in range(4):
            num_flag[k] = num_flag[k] + DBI_Flag.Flags[k]
        
        # non - encoded
        ### 2, 3, 4
        current_powerdc_no_PAM4 = DBI_Flag.calPower(0,1,2,3)
        total_powerdc_no_PAM4 = total_powerdc_no_PAM4 + current_powerdc_no_PAM4

        # encoded
        DBI_Flag_Origin = copyInit(DBI_Flag.Flags) # to store the initial state
        if example_2 < 3:
            print('PAM4 data =')
            print(data_PAM4[0])
            print(data_PAM4[1])
            print('Origin Flags: ', DBI_Flag_Origin)

        ### 2
        if 3 * DBI_Flag.Flags[0] + DBI_Flag.Flags[1] - DBI_Flag.Flags[2] - 3 * DBI_Flag.Flags[3] > 0:   # before power > after power => inversion
            total_powerdc_2 = total_powerdc_2 + DBI_Flag.calPower(3,2,1,0)
            encoded_2 = enc_PAM4_DBI(data_PAM4)
            if example_2 < 3:
                print("#2 PAM4-DBI")
                print('encoded to ', encoded_2)
        else:
            total_powerdc_2 = total_powerdc_2 + DBI_Flag.calPower(0,1,2,3)
            encoded_2 = data_PAM4
            if example_2 < 3:
                print('#2 PAM4-DBI')
                print("nothing has been changed")
        ### 2 switching
        if i == 0:
            prev_PAM4_2 = encoded_2
            print("first cycle")
        else:
            current_PAM4_2 = encoded_2
            newCharging_2 = switchingPAM4(prev_PAM4_2, current_PAM4_2)
            if example_2 < 3:
                print("newCharging_2 = ", newCharging_2)
            charging_2 = charging_2 + newCharging_2

        ### 3
        changed_DBI_Flag, maxIndex = DBI_Flag.change_11()
        total_powerdc_3 = total_powerdc_3 + changed_DBI_Flag.calPower(0,1,2,3)
        if maxIndex != 3:
            encoded_3 = enc_PAM4_MF(data_PAM4, maxIndex)
            if example_2 < 3:
                print('#3 PAM4-MF')
                print('encoded to ', encoded_3)
        else:
            encoded_3 = data_PAM4
            if example_2 < 3:
                print('#3 PAM4-MF')
                print("nothing has been changed")
        # 3 switching
        if i == 0:
            prev_PAM4_3 = encoded_3
        else:
            current_PAM4_3 = encoded_3
            newCharging_3 = switchingPAM4(prev_PAM4_3, current_PAM4_3)
            if example_2 < 3:
                print("newCharging_3 = ", newCharging_3)
            charging_3 = charging_3 + newCharging_3

        ### 4
        sorted_DBI_Flag = DBI_Flag.sortFlags()
        total_powerdc_4 = total_powerdc_4 + sorted_DBI_Flag.calPower(0,1,2,3)
        cList = sortCompare(DBI_Flag_Origin, sorted_DBI_Flag.Flags)
        encoded_4 = enc_PAM4_sort(data_PAM4, cList)
        # 4 switching
        if i == 0:
            prev_PAM4_4 = encoded_4
            print("#4 PAM4-Sort")
            print("first, encoded to ", encoded_4)
        else:
            current_PAM4_4 = encoded_4
            newCharging_4 = switchingPAM4(prev_PAM4_4, current_PAM4_4)
            if example_2 < 3:
                print("newCharging_4 = ", newCharging_4)
            charging_4 = charging_4 + newCharging_4
        
        _count = 1
        # print('\n\n\n\n\n')
        if example_2 < 3:
            example_2 = example_2 + 1

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
    print("NRZ-DBI Power = ", charging_1, ' * ', const_NRZ, ' = ', charging_1 * const_NRZ, "W")
    print("PAM4-DBI Power = ", charging_2, ' * ', const_PAM4, ' = ', charging_2 * const_PAM4, "W")
    print("PAM4-MF Power = ", charging_3, ' * ', const_PAM4, ' = ', charging_3 * const_PAM4, "W")
    print("PAM4-Sort Power = ", charging_4, ' * ', const_PAM4, ' = ', charging_4 * const_PAM4, "W\n\n\n\n\n")


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
