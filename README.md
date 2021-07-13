# Sound Quality Testing
## Tests
Currently there are two audio tests set up, the sine wave test and the voice recognition test.

###Sine Wave Test
This test can be used to test the amount of sound data that is lost over the connection. Using a sine wave audio file, we can mitigate factors like audio compression and recording quality and highlight the loss that is the result of the client or internet connections.

For this test, you will need to play the sine wave through one end of a call or collab call, and record it on the other end. (Using VB Cable https://vb-audio.com/Cable/ or other software)
The provided file 1000hz.wav is a perfect sine wave at 1000hz.
Make sure that the sound is not played too loud: the audio may clip and cause issues. In the recording, there can be silence before and after the sound is played.

Once it is recorded, you can run the test by running 'python frequency_analyzer.py'
It will prompt you for the file, and return the number of data points, the number of missing data points, and the percent of the sine wave that is missing 
It takes into account the silence before and after the wave.

##Voice Recognition Test
This test determines audio quality by using voice recognition to analyze and audio file. Based on how many of the words the audio recognizer gets correct, we can infer the quality of the recording.

For this test, you will need to record speech that is being played on one end of a call or collab call and record it on the other end. (Using VB Cable https://vb-audio.com/Cable/ or other software. You can also talk into the microphone and use that) 
weekday1.wav, is a provided example.
Optionally, you can put the correct words in the audio file in order, on a single line and seperated by spaces into a .txt file. (see words_list.txt for an example)
 
Once you have the recording, you can run 'python audio_recognizer.py'. It will prompt you for the name of the recording, and the name of the file containing the correct words (you can type either 'none' or nothing to just get the output.

If you provided a file, it will list the analyzed words, as well as the expected output, and the number of issues.
If you did not provide a file, it will output the recognized text.

If the audio file is unrecognizable as speech, it will return an error.
