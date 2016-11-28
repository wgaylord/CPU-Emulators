
class RamUsage:

    
    q = 0
    def tick(self,ram,prom):
        x = ram.exportRAM()
        used = 0
        for z in x:
            if not z == 0:
                used +=1
        if self.q == 1000:
            print used/(len(x)*1.0)*100
            self.q = 0
        else:
            self.q += 1