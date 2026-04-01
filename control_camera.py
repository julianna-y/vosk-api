#Managing queue of data
import queue
import sys
import json
#library for listening to the microphone
import sounddevice as sd
#Import the offline model and the offline recognizer from VOSK library
from vosk import Model, KaldiRecognizer

from camera import Camera
##
# create new camera object
my_camera = Camera()

'''This script processes audio input from the microphone and displays the transcribed text.'''

# get the samplerate - this is needed by the Kaldi recognizer
device_info = sd.query_devices(sd.default.device[0], 'input')
samplerate = int(device_info['default_samplerate'])

# display the default input device
print("===> Initial Default Device Number:{} Description: {}".format(sd.default.device[0], device_info))

# setup queue and callback function
q = queue.Queue()

def recordCallback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block.
    Saves the audio block to a queue."""

    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
    
# build the model and recognizer objects.
print("===> Build the model and recognizer objects. This will take a few minutes.")

# create Vosk model object, with English setting
model = Model(lang="en-us")

# create speech recognizer, with custom instruction/command words to recognize
recognizer = KaldiRecognizer(model, samplerate)

recognizer.SetWords(False)

print("===> Begin recording. Press Ctrl+C to stop the recording ")
try:
    # start the recording thread, and listens to the microphone
    with sd.RawInputStream(dtype='int16', channels=1,callback=recordCallback):
        
        while True:
            # get the next audio block from the queue
            data = q.get()

            # recognize the speech in the audio block
            # condition is true if model detects a pause after a speech fragment
            if recognizer.AcceptWaveform(data):

                # returns a list of possible transcripts - specifically, full commands
                recognizerResult = recognizer.Result()

                # convert the recognizerResult string into a dictionary  
                resultDict = json.loads(recognizerResult)

                # if a command was detected
                if not resultDict.get("text", "") == "":

                    print(recognizerResult) # print command

                    # send detected command to the camera object, to execute the command
                    my_camera.do_command(resultDict.get("text", ""))

                # otherwise, inform user that no input sound was detected
                else:
                    print("no input sound")
            
# if Ctrl+C is pressed, stop the recording thread and finish
except KeyboardInterrupt:
    print('===> Finished Recording')

except Exception as e:
    print(str(e)) # print error message
