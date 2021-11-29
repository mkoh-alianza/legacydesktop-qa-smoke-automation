from websocket import create_connection
from variables import *
from time import sleep
import xml.etree.ElementTree as ET
import ssl

class ApiBridge:
    
    def __init__(self, uri):
        self.uri = uri
        self.ws = None
        self.last_transaction_id = 0
        self.last_response = ''
        self.callId = ''

    '''======================================================================
                                HANDLING CONNECTIONS
    ========================================================================='''
    
    def open_connection(self):
        '''
        Establish a connection with API server by creating a Websocket object.
        Returns
        ----------
        'SUCCESS': string (byte array) value.
            If function does not raise an error.
        '''
        result = 0
        try:
            self.ws = create_connection(url=self.uri, sslopt={"cert_reqs": ssl.CERT_NONE})
        except Exception as e:
            raise AssertionError('Could not connect to server.\r\n' + str(e))
       
        return result
    

    def close_connection(self):
        '''
        Close Websocket object.
        Returns
        ----------
        'SUCCESS': string (byte array) value.
            If function does not raise an error.
        '''
        try:
            self.ws.close()
        except:
            raise AssertionError('Could not close connection.')
        
        return 'SUCCESS'


    def restart_connection(self):
        '''
        Closes and opens Websocket object.
        Returns
        ----------
        'SUCCESS': string (byte array) value.
            If function does not raise an error.
        '''
        try:
            self.close_connection()
            self.open_connection()
        except:
            raise AssertionError('Could not restart connection.')

        return 'SUCCESS'


    def response_contains(self, text=''):
        '''
        Checks if request response contains specific text.
        Parameters
        ----------
        text: str
            text to check in response.
        Returns
        ----------
        'SUCCESS': string (byte array) value.
            If function does not raise an error.
        '''
        try:
            response = self.last_response
            for word in text:
                if word not in response:
                    raise AssertionError("'{text}' not in response.\nActual response:\n{response}".format(text=word, response=response))
        except Exception as e:
            raise AssertionError('Could not get response.\r\nException: ' + str(e))

        return 'SUCCESS'


    def send_message(self, request_type=None, body=''):
        '''
        Checks if request response contains specific text.
        Parameters
        ----------
        text: str
            text to check in response.
        Returns
        ----------
        'SUCCESS': string (byte array) value.
            If function does not raise an error.
        '''
        try:
            msg = self._construct_api_message(request_type, body)
            # logger.console('\r\nSending...\r\n{msg}'.format(msg=msg))
            self.ws.send(msg)
            self._set_last_response()
            
        except:
            raise AssertionError('Could not send message or send response.')
        
        return 'SUCCESS'
        

    '''======================================================================
                            CONSTRUCTING REQUESTS MSGS
    ========================================================================='''

    def _construct_api_message(self, request_type, body):
        content_length = len(body)
        msg = '''\
GET /{request_type}
User-Agent: {user_agent_string}
Transaction-ID: {transaction_ID}
Content-Type: application/xml
Content-Length: {content_length}'''.format(request_type=api_request_types['properties'][request_type]['text'], 
                                            user_agent_string=user_agent_string, 
                                            transaction_ID=self._get_next_transaction_ID(),
                                            content_length=content_length)
        if (content_length > 0): msg += '\r\n\r\n' + body
        return msg
    

    def _get_next_transaction_ID(self):
        self.last_transaction_id += 1
        return self.last_transaction_id


    '''======================================================================
                                API CALLS
    ========================================================================='''

    def im(self, contact):
        content = xml_declaration_string + '''<im type="xmpp">
<address>{contact}</address>
</im>
        '''.format(contact=contact)
        try:
            self.send_message(api_request_types['IM'], content)
        except Exception as e:
            raise AssertionError('Could not start IM session\r\nException: ' + str(e))
    
    
    def check_voicemail(self):
        content = xml_declaration_string + '''<checkVoiceMail>
<accountId>0</accountId>
</checkVoiceMail>
        '''

        try:
            self.send_message(api_request_types['CHECKVOICEMAIL'], content)
        except Exception as e:
            raise AssertionError('Could not check voicemail.\r\nException: ' + str(e))
   
     
    def set_audio_properties(self, mute, speaker_mute, speaker, speaker_volume, microphone_volume):
        content = xml_declaration_string + '''<audioProperties>
<mute>{mute}</mute>
<speakerMute>{speaker_mute}</speakerMute>
<speaker>{speaker}</speaker>
<volume type="speaker">{speaker_volume}</volume>
<volume type="microphone">{microphone_volume}</volume>
</audioProperties>
        '''.format(mute=mute, speaker_mute=speaker_mute, speaker=speaker, speaker_volume=speaker_volume, microphone_volume=microphone_volume)
        try:
            self.send_message(api_request_types['AUDIOPROPERTIES'], content)
        except Exception as e:
            raise AssertionError('Could not set audio properties\r\nException: ' + str(e))

    
    def hold_call(self):
        try:
            self.send_message(api_request_types['HOLD'], xml_declaration_string + '<holdCall>\r\n <callId>{callId}</callId>\r\n</holdCall>'.format(callId=self.callId))
        except Exception as e:
            raise AssertionError('Could not hold call.\r\nException: ' + str(e))

        self.wait(2)
        return 'SUCCESS'
    

    def resume_call(self):
        try:
            self.send_message(api_request_types['RESUME'], xml_declaration_string + '<resumeCall>\r\n <callId>{callId}</callId>\r\n</resumeCall>'.format(callId=self.callId))
        except Exception as e:
            raise AssertionError('Could not resume call.\r\n')

        self.wait(2)
        return 'SUCCESS'


    def get_account_status(self, type):
        try:
            self.send_message(api_request_types['STATUS'], xml_declaration_string + '<status>\r\n <type>account</type>\r\n <accountType>{type}</accountType>\r\n</status>'.format(type=type))
        except:
            raise AssertionError("Could not get status for {type} account".format(type))
        
        return 'SUCCESS'


    def get_status(self, type=''):
        try:
            self.send_message(api_request_types['STATUS'], xml_declaration_string + '<status>\r\n <type>{type}</type>\r\n</status>'.format(type=type))
        except:
            raise AssertionError("Could not get status for type '{type}'".format(type))

        return 'SUCCESS'

    def get_status_with_parameters(self, status_type, parameters):
        content = xml_declaration_string + '''<status>
<type>{status_type}</type>
{parameters}
</status>
        '''.format(status_type=status_type, parameters=parameters)
        try:
            self.send_message(api_request_types['STATUS'], content)
        except Exception as e:
            raise AssertionError("Could not get status for type '{type}'\r\nException: ".format(type) + str(e))
        
    
    def place_call(self, remote_end=''):
        try:
            self.send_message(api_request_types['CALL'], xml_declaration_string + '<dial type="audio">\r\n <number>{remote_end}</number>\r\n<displayName>Test</displayName>\r\n<suppressMainWindow>false</suppressMainWindow>\r\n</dial>'.format(remote_end=remote_end))
            self.set_call_id()
        except:
            raise AssertionError('Could not place call.')
            
        self.wait(7)
        
        return 'SUCCESS'


    def end_call(self):
        try:
            self.send_message(api_request_types['ENDCALL'], xml_declaration_string + '<endCall>\r\n <callId>{call_id}</callId>\r\n</endCall>'.format(call_id=self.callId))
        except:
            raise AssertionError('Could not end call.')

        return 'SUCCESS'


    def start_call_recording(self, filename):
        try:
            self.send_message(api_request_types['STARTCALLRECORDING'],
                xml_declaration_string + '<startCallRecordiing>\r\n <callId>{callId}</callId>\r\n <filename>{filename}</filename>\r\n <suppressPopup>true</suppressPopup>\r\n</startCallRecording>'.format(callId=self.callId, filename=filename))
        except:
            raise AssertionError('Could not start call recording.')

        self.wait(5)
        return 'SUCCESS'


    def end_call_recording(self):
        try:
            self.send_message(api_request_types['STOPCALLRECORDING'],
                xml_declaration_string + '<stopCallRecordiing>\r\n <callId>{callId}</callId>\r\n</stopCallRecording>'.format(callId=self.callId))
        except:
            raise AssertionError('Could not stop call recording.')

        return 'SUCCESS'
    
    def set_device(self, deviceName, deviceID, deviceType, deviceRole):
        try:
            self.send_message(api_request_types['SELECTAUDIODEVICES'], xml_declaration_string + '<devices><device><name>{deviceName}</name><id>{deviceID}</id><type>{deviceType}</type><role>{deviceRole}</role></device></devices>'.format(deviceName=deviceName, deviceID=deviceID, deviceType=deviceType, deviceRole=deviceRole))
        except:
            raise AssertionError('Could not set audio device.')
        
        return 'SUCCESS'
    
    def get_device_info(self):
        deviceList = {}
        try:
            self.get_status('audioDevices')
            response = self.last_response
            response = self._get_xml_portion(response)
               
            root = ET.fromstring(response)
            for device in root.find('devices'):
                deviceList[device.find('name').text] = device.find('id').text
                
            #self.callId = root.find('call').find('id').text
        except AttributeError:
            raise AssertionError('Could not find call id.')
        
        return deviceList
    '''======================================================================
                                HELPER FUNCTIONS
    ========================================================================='''

    def _set_last_response(self):
        '''
        Set self.last_response to response that contains self.last_transaction_id.
        '''
        responses = self.ws.__iter__()
        
        for response in responses:
            tId = self._get_transaction_id(response)
            if tId > self.last_transaction_id:
                raise AssertionError('No response found.')

            if tId == self.last_transaction_id:
                self.last_response = response
                return

    def _get_all_responses(self):
        responses = self.ws.__iter__()
        count = 0;
        for response in responses:
            count = count + 1
            if(count > 7):
                return
    
    def _get_transaction_id(self, data):
        '''
        Get transaction id from xml in string format.
        Parameters
        ----------
        data: str
            xml data in string format.
        Returns
        ----------
        tId: integer value.
            -1 if no transaction ID if found, else return the transaction id found.
        '''
        tId = -1
        lines = data.replace('\r\n', '\n').split('\n')
        for line in lines:
            if line[0:15] == 'Transaction-ID:':
                tId = int(line[15:])
                return tId
        
        return tId # response doesn't contain a transaction id
    

    def _get_xml_portion(self, response):
        return '\n'.join(response.split('\n')[4:])


    def wait(self, length):
        sleep(int(length))
    
    def set_call_id(self):
        try:
            self.get_status('call')
            response = self.last_response
            response = self._get_xml_portion(response)
            root = ET.fromstring(response)
            self.callId = root.find('call').find('id').text
        except AttributeError:
            raise AssertionError('Could not find call id.')
        
        return 'SUCCESS'