def toTwoComp(n):
    s = bin(n & int("1"*16, 2))[2:]
    return ("{0:0>%s}" % (16)).format(s)
    
    
def fromTwoComp(n): 
    temp = n[:1]
    num = ""
    if int(temp):
        for x in n[1:]:
           
            if x == "1":
                num = num + "0"
            else:
                num = num + "1"
        return (-int(num,2))-1
    else:
        return int(n,2)
        
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
        num |= (1 << (16-1))

    return num