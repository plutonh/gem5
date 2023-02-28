import sys

sys.stdout = open("/home/jonghyeon/gem5/Convert/convert_out.txt", "w")

def hexaToBinary(data):
    if   data == "0": return "0000"
    elif data == "1": return "0001"
    elif data == "2": return "0010"
    elif data == "3": return "0011"
    elif data == "4": return "0100"
    elif data == "5": return "0101"
    elif data == "6": return "0110"
    elif data == "7": return "0111"
    elif data == "8": return "1000"
    elif data == "9": return "1001"
    elif data == "a": return "1010"
    elif data == "b": return "1011"
    elif data == "c": return "1100"
    elif data == "d": return "1101"
    elif data == "e": return "1110"
    else:             return "1111"

def converting(_file):
    lines = file_in.readlines()
    for i, line in enumerate(lines):
    #for line in lines: # total 16 pairs of hexadecimal data
        if i > 10 and i < 682951: # qsort_small
        # if i > 10 and i < 10885475: # qsort_large
            j = 0
            plus = 28
            for j in range(16):
                index = j + plus
                first = line[index]
                second = line[index + 1]
                # print(first + second, j)
                print(hexaToBinary(first) + hexaToBinary(second))
                if index == 49:
                    plus = plus + 3
                else:
                    plus = plus + 2

file_in = open("/home/jonghyeon/gem5/m5out/simout", "r")
converting(file_in)

file_in.close()
sys.stdout.close()