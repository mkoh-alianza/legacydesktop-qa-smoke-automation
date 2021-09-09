import math

class SoundModifier:
    def __init__(self, data1, data2, acc):
        self.data1 = data1
        self.data2 = data2
        self.acc = acc
        self.maxes1 = self.getMaxes(data1, acc)
        self.maxes2 = self.getMaxes(data2, acc)
        self.outliers = self.defineOutliers()
        self.scale = 0
        self.offset = 0
        self.analyze()
        
    def defineOutliers(self):
        outliers = []
        for i in [x for x in range(self.acc) if x != 0]:
            dif1 = self.maxes1[i][1] - self.maxes1[i - 1][1]
            dif2 = self.maxes2[i][1] - self.maxes2[i - 1][1]
        if(abs(dif1-dif2) > 500):
            outliers.append(i)
        return outliers
        
    def getMaxes(self, data, num):
        maxes = [[0]] * num
        for i in range(len(data)):
            for j in range(len(maxes)):
                if data[i] > maxes[j][0]:
                    maxes.insert(j, [data[i], i])
                    maxes.pop()
                    break
        return maxes
        
    def analyze(self):
        
        count = 0
        scale = 0
        offset = 0
        print(self.maxes1)
        print(self.maxes2)
        for i in [x for x in range(self.acc) if x not in self.outliers]:
            scale += self.maxes1[i][0]/self.maxes2[i][0]
            offset += self.maxes2[i][1] - self.maxes1[i][1]
            count = count + 1
  
        self.scale = scale/count
        self.offset = int(offset/count)
        
    def pinPoint(self):   
        for i in range(len(self.data2)):
            self.data2[i] = self.data2[i] * self.scale
        
        step = self.offset - 10
        print(self.offset)
        print(self.scale)
        
        match = False
        allowence = 400
        count = 0
        loss = 0
        while(match != True):
            while(len(self.data1) + step <= len(self.data2)):
                for i in range(self.acc * 1000):
                    match = True
                
                if(self.outOfRange(self.data1[i], self.data2[step + i], self.acc * 20)):
                        loss = loss + 1
                        if(loss > allowence):
                            loss = 0
                            match = False
                            break 
                if(match):
                    break

                step = step + 1
            print("No Match, increasing allowence:")
            allowence += 200
            
        newData2 = [0] * len(self.data1)
        print(len(self.data2))
        print(len(newData2))
        print(step)
        for i in range(len(self.data1)):
            newData2[i] = self.data2[i + step]
        
        self.data2 = newData2
        
        return newData2
        
        
    def outOfRange(self, a, b, rng):
        if(abs(a - b) < rng):
            return False
        else:
            return True
            
            
    def cosineSimilarity(self):
        product = 0
        powerA = 0
        powerB = 0
        
        for i in range(len(self.data1)):
            product += self.data1[i] * self.data2[i]
            powerA += self.data1[i]**2
            powerB += self.data2[i]**2
            
        return product/(math.sqrt(powerA)*math.sqrt(powerB))
        
    def setSampleRate(r1, data2, r2):
        scale = r1/r2
        
        step = 0
        newData = []
        for i in range(len(data2)):
            if(step > 1):
                step = step - 1
                newData.append(data2[i])
            
            step += scale
            
        return newData