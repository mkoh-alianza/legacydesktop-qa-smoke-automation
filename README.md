See documentation for complete steps: https://alianza.atlassian.net/wiki/spaces/DEV/pages/2708931010/Automation+for+Desktop+Client

<h1> Steps to setup: </h1> 

To set up the cable and windows:

1. Download and install theVC Cables (You will notice there is a cable A and cable B, we will need both of them). The cables will need to be installed on both ends.
You will also need to install Python and pip, but you may already have those.

2. Install the product you wish to test

3. Open remote desktop. Before you connect to the remote end, click on ‘Show Options’ in the remote desktop window. Then go to Local Resources->Remote Audio and set it to ‘Play on remote computer’. (You should only need to do this the first time)
Then, connect to the remote end.

4. Open up Bria on both ends. Go to Softphone->Preferences->Devices and uncheck the ‘Enable echo cancellation’ box on both ends.

5. On the main end, set Speaker to ‘Cable-B Input’ and Microphone to ‘Cable-A Output’.
On the remote end, set Speaker to ‘Cable-A input’ and Microphone to ‘Cable-A Output’.

6. Position the Bria window in the top left and put Bria, then the remote desktop at the front of your taskbar. Different screen resolutions have different sizes for these, so you may have to move stuff to different positions if the clicks aren’t clicking in the right places. 

All of the external setup is complete, now we need to setup the code itself.


To setup the code

1. Download the GitHub repository onto the main end. (https://github.com/AlianzaQA/Smoke-Client-Automation)

2. Open an command prompt in the folder where the code has been downloaded.

3. You can create a virtual environment using the command: ‘python -m venv env’ and switch into it using ‘env\scripts\activate.bat’.

4. Use pip install -r requirements.txt to install all of the required packages.

All of the code has now been setup, here is how to run.


To run the code

1. Open a command prompt where the repo is downloaded.

2. Enter a virtual environment using ‘python -m venv env’.

3. Use the command ‘python main.py’ to run the testing code in ‘main.py’.

It should begin with the tests.



<h3>Note</h3>
Remember to go to Prefrences->Application->Security and set API access to "Allow Access Always"
When connecting remote desktop, before connecting go to More Options->Local Resources->Remote Audio

<h2>Current Project Overview</h2>
<h3>Main</h3>
Currently just initilizes an 'Agent', which has access to devices (Device-io), API (API_Bridge) and auto-clicker actions (Action Clicker). This 'agent' is what runs the programmed tests.

<h3>Agents</h3>
A test agent is a contoller that will perform actions to complete a test. These actions include any API commands, as well as playing or listening and recognizing audio through VB cable. Currently requires the API's URI to initilize.

<h3>API_bridge</h3>
A component of the agent. Handels all API commands using the 'websocket-client' libary, as is seen in api_bridge.py. Requires the API URI to initialize, does not open the connection once started, must be opened through the open_connection method.

<h3>Action Clicker</h3>
Another agent component. Uses pre-recorded actions to operate the client using the mouse. You can record new actions using 'record.py'. It assumes for all actions that the client window is in the top left corner (allowing these saved actions to work across different computers). Actions can be as breif or as long as required. For remote connections,they must first be connected, then the task bar must be organized. 

<h3>Device-io</h3>
Another agent component. Handels all IO using 'SoundDevice' and 'SoundFile' libarys. It plays and records files, usually read from 'test-data' and written to 'outputs'. Devices must be set for playing and recording beforehand.

<h3>Audio-Recognizer</h3>
Another agent component 'SpeechRecognition' libary to recognize and list out text in a sound file. Also can compare between expected and actual results using the Text Comparer.

<h3>Text Comparison</h3>
Used by the audio recognizer to compare two sections of text (expected vs actual) and print a status report containing the differences.

<h2>Unused Sound Analysis</h2>

<h3>Frequency Analyzer</h3>
Used to determine the frequency of a waveform. Used to test sound quality. Currently unused.

<h3>Sound Modifier</h3>
Used to compare two audio files using cosine-similarity. Also used to change sample rate. Currently unused.
