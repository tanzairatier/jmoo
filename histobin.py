from utility import *
class histobin:
        def __init__(self, numBins, decision, decIndex):
            self.decIndex = decIndex
            self.numBins = numBins
            self.bins = []
            spread  =  decision.up - decision.low
            step = spread/float(numBins)
            self.bins = [singleBin(i, decision.low + step*i, decision.low + step*(i+1)) for i in range(numBins)]
        def getTotal(self):
            total = 0
            for bin in self.bins:
                total += bin.count
            return total
        def __repr__(self):
            s = "["
            total = self.getTotal()
            if total == 0: return  str([0 for bin in self.bins])
            for bin in self.bins:
                if bin.count == 0: 
                    s += '{0: >3}'.format("-") + " "
                else:
                    s += str("%3.0f" % (100.0*bin.count/float(total))) + " "
            s += "]"
            return s
        def var(self):
            total = float(self.getTotal())
            counts = [100*bin.count/total for bin in self.bins]
            return var(counts)
        def stdev(self):
            return self.var()**0.5
        def externalVar(self, histobins):
            allCounts = []
            for hb in histobins:
                total = float(hb.getTotal())
                for bin in hb.bins:
                    allCounts.append(100*bin.count/total)
            return var(allCounts)
        def importance(self):
            max_case = [0 for bin in self.bins]
            max_case[0] = 100
            max_var = var(max_case)
            return self.var()/max_var
        def populate(self, data):
            
            for item in data:
                for b,bin in enumerate(self.bins):
                    if b == 0:
                        if item >= bin.low and item < bin.up:
                            self.bins[b].add(item)
                            break
                    elif b == (len(self.bins)-1):
                        if item > bin.low and item <= bin.up:
                            self.bins[b].add(item)
                            break
                    else:
                        if item > bin.low and item <= bin.up:
                            self.bins[b].add(item)
                            break
        def sort(self, bywhat=None):
            if bywhat == "count": bywhat = lambda bin: bin.count
            else: bywhat = lambda bin: bin.index
            
            self.bins = sorted(self.bins, key=bywhat)
        def freq(self, bin):
            total = float(self.getTotal())
            return 100 * bin.count / total 
        def newImportance(self, histobins):
            self.NI =(self.var()) / sum([hb.var() for hb in histobins]) 
            return self.NI
        def rex(self):
            self.sort("count")
            importance = self.importance()*100
            removed_sum = 0
            self.rex_bins = []
            for bin in self.bins:
                binfreq = self.freq(bin)
                if removed_sum+binfreq < importance:
                    removed_sum += binfreq
                    #self.rex_bins.append(bin)
                    #self.rex_bins[-1].count = 0
                    bin.count = 0
                #else:
                    #self.rex_bins.append(bin)
            
            #self.bins = self.rex_bins
            """
            self.rex_bins = sorted(self.rex_bins, key=lambda bin: bin.index)
            s = "["
            total = self.getTotal()
            if total == 0: return  str([0 for bin in self.rex_bins])
            for bin in self.rex_bins:
                if bin.count == 0:
                    s += '{0: >3}'.format("X") + " "
                else:
                    s += str("%3.0f" % (100.0*bin.count/float(total))) + " "
            s += "]"
            print s
            """ 
                
class singleBin:
        def __init__(self, ind, low, up):
            self.index = ind
            self.low = low
            self.up = up
            self.count = 0
            self.items = []
        def add(self, item):
            self.count += 1
            self.items.append(item)
