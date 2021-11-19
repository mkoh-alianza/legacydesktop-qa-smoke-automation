#$Current Project Overview
##Main
Currently just initilizes an 'Agent', as well as the device IO.

##Agents
A test agent is a contoller that will perform actions to complete a test. These actions include any API commands, as well as playing or listening and recognizing audio through VB cable. Currently requires the API's URI to initilize.

##API_bridge
A component of the agent. Handels all API commands using the 'websocket-client' libary, as is seen in api_bridge.py. Requires the API URI to initialize, does not open the connection once started, must be opened through the open_connection method.

##Device-io
Another agent component. Handels all IO using 'SoundDevice' and 'SoundFile' libarys. It plays and records files, usually read from 'test-data' and written to 'outputs'. Devices must be set for playing and recording beforehand.

##Audio-Recognizer
Another agent component 'SpeechRecognition' libary to recognize and list out text in a sound file. Also can compare between expected and actual results using the Text Comparer.

