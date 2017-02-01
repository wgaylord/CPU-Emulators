
def mybin(num):
    s = bin(abs(num))[2:]
    s = ("{0:0>%s}" % (15)).format(s)
    if num < 0:
        return "1"+s
    else:
        return "0"+s


def myint(bnum):
    #print ("-"*int(bnum[0]))+bnum[0:]
    #print int(bnum[1:],2)
    return int(("-"*int(bnum[0]))+bnum[1:],2)

def format2(t):
    return ("{0:0>%s}" % (16)).format(bin(t)[2:])

def format(t):
    return ("{0:0>%s}" % (15)).format(bin(t)[2:])

def rollover(num):
    if num >= 2**15:
        return 0-(num-(2**15))
    if num <= -2**15:
        return 0+(num+(2**15))
    return num

def rotl(num):
    bit = num & (1 << (16-1))
    num <<= 1
    if(bit):
        num |= 1
    num &= (2**16-1)
    return num

def rotr(num):
    num &= (2**16-1)
    bit = num & 1
    num >>= 1
    if(bit):
        num |= (1 << (16 - 1))
    return num