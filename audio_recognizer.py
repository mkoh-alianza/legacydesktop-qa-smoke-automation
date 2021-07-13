import speech_recognition as sr

from os import path
from text_compare import TextComparer

class AudioRecognizer:
	def work(filename):
		AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), filename)

		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
			audio = r.record(source) 
	
		try:
			# for testing purposes, we're just using the default API key
			# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
			# instead of `r.recognize_google(audio)`
			output = r.recognize_google(audio)
			print("Google Speech Recognition thinks you said: " + output)
			return output
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			return ""
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))	
			return ""
			
if __name__ == '__main__':
	print("Enter the name of the audio file to analyze: ")
	filename = input()
	
	print("Enter the file containing expected output (type 'none' for no file): ")
	expected = input()
	
	output = AudioRecognizer.work(filename)
	if(expected != "none" and expected != ""):
		try:
			TextComparer.compareOutputToFile(expected, output)
		except:
			print("Unable to compare with file")
