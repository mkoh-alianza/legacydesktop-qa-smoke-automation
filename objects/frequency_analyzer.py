import sys

sys.path.append('s./env/Lib/site-packages')
import librosa

class FrequencyAnalyzer:
	def findStart(data):
		i = 0
		while(True):
			i = i + 1
			if(data[i] > 0.1 and data[i+1] > data[i]):
				while(True):
					if(data[i] < data[i+1]):
						i = i + 1
					else:
						return i
	
	
	def findWrong(start, data):
		fail = 0
		size = 0
		step = start
		allowence = 5
		load = 0
		while(step + 1 < len(data)):
            
			if(abs(data[step] - data[step+1]) < 0.01):
				if(allowence < 1):
					load = load + 1
					size = size + 1
				else:
					allowence = allowence - 1
					#if(allowence == 0):
						#print('found spot at ' + str(step/16000))
			else:
				if(allowence  == 0):
					#print(size)
					size = 0
				fail = fail + load
				load = 0
				allowence = 5
			step = step + 1	
		return fail, load

	def getFrequencyOff(start, sr, fq, data):
	
		offsum = 0
		while(step+1 < len(data)):
			if(data[step] < 0 and data[step + 1] > 0):
				if(lastPeak > start):
					dif = lastPeak - step
					if(dif < 100):
						
						offsum = offsum + abs(sr/dif - fq)/fq
				
				lastPeak = step
		return offsum / (len(data) - start)
		
		
				
if __name__ == '__main__':
	print("Enter the name of the sine wave audio file to analyze")
	filename = input()
	
	data, Fs = librosa.load(filename, sr=16000)


	start = FrequencyAnalyzer.findStart(data)
	print('Sound starts at index ' + str(start))

	wrong, end = FrequencyAnalyzer.findWrong(start, data)
	print('total data length: ' + str(len(data) - start - end))
	print('lost data points found: ' + str(wrong))
	#percent = (100 - (100 * wrong/(len(data) - start - end)))
	percent = 100 * wrong/(len(data) - start - end)
	print("Roughly" + f'{percent:.5g}' + '%' + "of the sine wave is missing")

