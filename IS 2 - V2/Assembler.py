import BinLib
import sys
import IS

def FromInt(num):
   # print num
    first = (num>>8)&255
    #print first
    second = (num&255)
    #print second
    return (chr(first),chr(second))
def format(b):
    return ("{0:0>%s}" % (4)).format(bin(b)[2:])
def ReadASM(file):

    Out = []
    f = open(file)
    lines = f.readlines()
    f.close()
    lineNum = 0
    nextRaw = False
    for x in lines:
        try:
            print x
            if nextRaw == True:
                Out.append( int(BinLib.toTwoComp(int(x.replace("\n",""))),2))
                nextRaw = False
                lineNum +=1
            else:
                splitline = x.split(" ")
                extras = len(splitline) - 1 
                OP = IS.str2OP[splitline[0].upper()]
                next = None
                if OP in IS.Requires2Lines:
                    nextRaw = True
                if OP == 6:
                    Out.append(int(format(OP)+"00000000"+format(int(splitline[3])),2))

                if OP == 7:
                    Out.append(int(format(OP)+format(int(splitline[1]))+"0000"+format(int(splitline[3])),2))
                if OP == 8 or OP == 9:
                    Out.append(int(format(OP)+format(int(splitline[1]))+format(int(splitline[2]))+format(int(splitline[3])),2))
                    if int(splitline[2]) == 0:
                        nextRaw = True
                    else:
                        nextRaw = False
                if OP == 12:
                    Out.append(int(format(OP)+format(int(splitline[1]))+format(int(splitline[2]))+format(int(splitline[3])),2))
                
                if OP == 13:
                    Out.append(int(format(OP)+format(int(splitline[1]))+format(int(splitline[2]))+"0000",2))
                    
                if OP == 15:
                    Out.append(int(format(OP)+format(int(splitline[1]))+"00000000",2))
                if OP < 6 or OP == 10 or OP ==11 or OP == 14:
                    try:
                        Out.append(int(format(OP)+format(int(splitline[1]))+format(int(splitline[2]))+format(int(splitline[3])),2))
                    except:
                        print "ERROR! on line number: " + str(lineNum) +" Operation: "+splitline[0]+" requires 3 numbers!"
            
        except Exception as e:
            print "ERROR! on line number: " + str(lineNum) +" Operation: "+splitline[0]
            #print e
        
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
   
    