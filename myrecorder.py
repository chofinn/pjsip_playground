import sys
import pjsua as pj
import wave
from time import sleep

LOG_LEVEL=3
current_call = None
wait_call = 1
# Logging callback
def log_cb(level, str, len):
    print(str, end=' ')


# Callback to receive events from account
class MyAccountCallback(pj.AccountCallback):

    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)

    # Notification on incoming call
    def on_incoming_call(self, call):
        global current_call 
        if current_call:
            call.answer(486, "Busy")
            return
            
        print("Incoming call from ", call.info().remote_uri)
        print("Press 'a' to answer")

        current_call = call

        call_cb = MyCallCallback(current_call)
        current_call.set_callback(call_cb)

        current_call.answer(180)

        
# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):

    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    # Notification when call state has changed
    def on_state(self):
        global current_call
        print("Call with", self.call.info().remote_uri, end=' ')
        print("is", self.call.info().state_text, end=' ')
        print("last code =", self.call.info().last_code, end=' ') 
        print("(" + self.call.info().last_reason + ")")
        
        if self.call.info().state == pj.CallState.DISCONNECTED:
            current_call = None
            print('Current call is', current_call)
        elif self.call.info().state == pj.CallState.CONFIRMED:
            print('Answered')
            wait_call = 0
            # open wav file and get its playing time
            wfile = wave.open("intro.wav")
            print("opened file")
            # time = (1.0 * wfile.getnframes ()) / wfile.getframerate ()
            time = 10
            print ("play time: " + str(time) + "ms")
            wfile.close()

            # setup playing conf and play
            call_slot = self.call.info().conf_slot
            self.wav_player_id=pj.Lib.instance().create_player('hotel.wav',loop=False)
            self.wav_slot=pj.Lib.instance().player_get_slot(self.wav_player_id)
            pj.Lib.instance().conf_connect(self.wav_slot, call_slot)
            sleep(time)
            pj.Lib.instance().player_destroy(self.wav_player_id)
            print("end playing")
            print("start recording")
            # setup recording conf and record
            time = 10

            call_slot = self.call.info().conf_slot
            self.wav_recorder_id = pj.Lib.instance().create_recorder('voicemail.wav')
            self.wav_slot = pj.Lib.instance().recorder_get_slot(self.wav_recorder_id)
            pj.Lib.instance().conf_connect(call_slot, self.wav_slot)
            sleep(time)
            pj.Lib.instance().recorder_destroy(self.wav_recorder_id)

            print("end recording")
            self.call.hangup()


    # Notification when call's media state has changed.
    def on_media_state(self):
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            pj.Lib.instance().conf_connect(call_slot, 0)
            pj.Lib.instance().conf_connect(0, call_slot)
            print("Media is now active")
        else:
            print("Media is inactive")

        

# Create library instance
lib = pj.Lib()

try:
    # Init library with default config and some customized
    # logging config.
    lib.init(log_cfg = pj.LogConfig(level=LOG_LEVEL, callback=log_cb))

    # Create UDP transport which listens to any available port
    transport = lib.create_transport(pj.TransportType.UDP, 
                                     pj.TransportConfig(0))
    print("\nListening on", transport.info().host, end=' ') 
    print("port", transport.info().port, "\n")
    
    # Start the library
    lib.start()

    # Create local account
    acc = lib.create_account_for_transport(transport, cb=MyAccountCallback())

    my_sip_uri = "sip:" + transport.info().host + \
                 ":" + str(transport.info().port)
    
    while True:
       input = sys.stdin.readline().rstrip("\r\n")
       if input == "a":
            if not current_call:
                print("There is no call")
                continue
            current_call.answer(200)
            break

    while current_call:
        pass
    # Shutdown the library
    transport = None
    acc.delete()
    acc = None
    lib.destroy()
    lib = None

except pj.Error as e:
    print("Exception: " + str(e))
    lib.destroy()
    lib = None

