




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
        

    