import sys
import CPU.IS as IS
import MotherBoard.util as util
def FromInt(num):
   # print num
    first = (num>>8)&255
    #print first
    second = (num&255)
    #print second
    return (chr(first),chr(second))

def format(b):
    return ("{0:0>%s}" % (4)).format(bin(b)[2:])
def format2(t):
    return ("{0:0>%s}" % (16)).format(bin(t)[2:])
def ReadASM(file):

    Out = []
    f = open(file)
    lines = f.readlines()
    f.close()
    lineNum = 0
    
    for x in lines:

        parts = x.upper().split(" ")
        if parts[0] not in IS.op2int.keys():
            Out.append(int(util.mybin(int(parts[0].replace("\n",""))),2))
        else:
            op = IS.op2int[parts[0]]
            out = format(op)
            for x in xrange(1,4):
                try:
                    out = out + format(int(parts[x]))
                except:
                    out = out + format(0)
            print out
            Out.append(int(out,2))



        
    return Out

def WriteBin(file,data):
    #print data
    data.reverse()
    f = open(file,"wb+")
    try:
        while True:
            t = data.pop()
            parts = FromInt(t)
            #print parts
            f.write(parts[0])
            f.write(parts[1])
    except Exception as e:
        #pass
        print e
        
    f.flush()
    f.close()
    
data = ReadASM(sys.argv[1])
WriteBin(sys.argv[1].split(".")[0]+".bin",data)
   
    