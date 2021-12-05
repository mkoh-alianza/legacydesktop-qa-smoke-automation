

'''============================================================================
                                CHANGE THESE
==============================================================================='''
REMOTEEND = '5555551006'  # SIP number that will be called during testing. Make the remote is setup to auto-answer.
FILENAME = 'UserscpqaDesktopmy_recording'  # File path that call recordings will be saved
CONTACT = 'qatest1@counterpath.com'  # XMPP address of an existing contact.
'''==============================================================================='''























'''============================================================================
                            RESPONSE CONTAINS VARS
==============================================================================='''
JUST200OK = ['200 OK']
JUST400 = ['400']
FALSECONTACT = 'K23JH(3H3KJ'


'''============================================================================
                                MESSAGE CONSTANTS
==============================================================================='''

xml_declaration_string = '<?xml version="1.0" encoding="utf-8" ?>'

user_agent_string = 'Robot Framework'

api_request_types = {
    'BRINGTOFRONT':			    0,
    'SHOWHISTORY':			    1,
    'STATUS':					2,
    'SELECTAUDIODEVICES':		3,
    'CALL':					    4,
    'ANSWER':					5,
    'HOLD':					    6,
    'RESUME':					7,
    'DTMF':					    8,
    'TRANSFERCALL':			9,
    'AUDIOPROPERTIES':		10,
    'CALLOPTIONS':			11,
    'ENDCALL':				12,
    'STARTCALLRECORDING':		13,
    'STOPCALLRECORDING':		14,
    'CHECKVOICEMAIL':			15,
    'SETPRESENCE':			16,
    'IM':						17,
    'STARTSCREENSHARE':		18,
    'STARTCOLLAB':			19,
    'JOINCOLLAB':				20,
    'SIGNIN':					21,
    'SIGNOUT':				22,
    'EXIT':					23,
	'STARTATTENDEDTRANSFER': 24,
	'MERGE': 25,

    'properties': {
        0: {'text': "bringToFront"},
        1: {'text': "showHistory"},
        2: {'text': "status"},
        3: {'text': "selectAudioDevices"},
        4: {'text': "call"},
        5: {'text': "answer"},
        6: {'text': "hold"},
        7: {'text': "resume"},
        8: {'text': "dtmf"},
        9: {'text': "transferCall"},
        10: {'text': "audioProperties"},
        11: {'text': "callOptions"},
        12: {'text': "endCall"},
        13: {'text': "startCallRecording"},
        14: {'text': "stopCallRecording"},
        15: {'text': "checkVoiceMail"},
        16: {'text': "setPresence"},
        17: {'text': "im"},
        18: {'text': "startScreenShare"},
        19: {'text': "startCollab"},
        20: {'text': "joinCollab"},
        21: {'text': "signIn"},
        22: {'text': "signOut"},
        23: {'text': "exit"},
		24: {'text': "startAttendedTransferCall"},
		25: {'text': "merge"},
    }
}

api_message_types = {
    'UNKNOWN':				0,
    'RESPONSE':				1,
    'EVENT':					2,
    'ERROR':					3
}

api_event_types = {
    'UNKNOWN':				0,
    'STATUSCHANGE':			1
}

api_status_event_types = {
    'UNKNOWN':				0,
    'PHONE':					1,
    'CALL':					2,
    'CALLHISTORY':			3,
    'MISSEDCALL':				4,
    'VOICEMAIL':				5,
    'AUDIODEVICES':			6,
    'AUDIOPROPERTIES':		7,
    'CALLOPTIONS':			8,
    'PRESENCE':				9,
    'SCREENSHARE':			10,
    'AUTHENTICATION':			11,
    'SYSTEMSETTINGS':			12,
    'ACCOUNT':				13,

    'properties': {
        1: {'text': "phone"},
        2: {'text': "call"},
        3: {'text': "callHistory"},
        4: {'text': "missedCall"},
        5: {'text': "voicemail"},
        6: {'text': "audioDevices"},
        7: {'text': "audioProperties"},
        8: {'text': "callOptions"},
        9: {'text': "presence"},
        10: {'text': "screenShare"},
        11: {'text': "authentication"},
        12: {'text': "systemSettings"},
        13: {'text': "account"}
    }
}

api_call_states = {
    'UNKNOWN':				0,
    'RINGING':				1,
    'CONNECTING':				2,
    'CONNECTED':				3,
    'FAILED':					4,
    'ENDED':					5,

    'properties': {
        1: {'text': "ringing"},
        2: {'text': "connecting"},
        3: {'text': "connected"},
        4: {'text': "failed"},
        5: {'text': "ended"}
    }
}

api_history_event_states = {
    'ALL':				0,
    'MISSED':				1,

    'properties': {
        0: {'text': "all"},
        1: {'text': "missed"}
    }
}