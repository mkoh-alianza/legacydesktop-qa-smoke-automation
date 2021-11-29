#$Current Project Overview
##Main
Currently just initilizes an 'Agent', which has access to devices (Device-io), API (API_Bridge) and auto-clicker actions (Action Clicker). This 'agent' is what runs the programmed tests.

##Agents
A test agent is a contoller that will perform actions to complete a test. These actions include any API commands, as well as playing or listening and recognizing audio through VB cable. Currently requires the API's URI to initilize.

##API_bridge
A component of the agent. Handels all API commands using the 'websocket-client' libary, as is seen in api_bridge.py. Requires the API URI to initialize, does not open the connection once started, must be opened through the open_connection method.

##Action Clicker
Another agent component. Uses pre-recorded actions to operate the client using the mouse. You can record new actions using 'record.py'. It assumes for all actions that the client window is in the top left corner (allowing these saved actions to work across different computers). Actions can be as breif or as long as required. For remote connections,they must first be connected, then the task bar must be organized. 

##Device-io
Another agent component. Handels all IO using 'SoundDevice' and 'SoundFile' libarys. It plays and records files, usually read from 'test-data' and written to 'outputs'. Devices must be set for playing and recording beforehand.

##Audio-Recognizer
Another agent component 'SpeechRecognition' libary to recognize and list out text in a sound file. Also can compare between expected and actual results using the Text Comparer.

##Text Comparison
Used by the audio recognizer to compare two sections of text (expected vs actual) and print a status report containing the differences.

#$Unused Sound Analysis

##Frequency Analyzer
Used to determine the frequency of a waveform. Used to test sound quality. Currently unused.

##Sound Modifier
Used to compare two audio files using cosine-similarity. Also used to change sample rate. Currently unused.