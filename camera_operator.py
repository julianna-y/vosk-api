from picamera2 import Picamera2, Preview
from libcamera import controls
import time
import os

picam2 = Picamera2()
    
class Camera_Operator:

    def __init__(self):
        # initialize camera
        
        self.is_recording = False
        self.time_rec = time.time()

    def do_command(self, cmd):
        """
        Execute camera action based on detected voice command
        """
        cmd_variations = {
            "start video" : ["start video", "start the video", "started video", "stirred video", "started the video", "start a video"],
            "stop video" : ["stop video", "stop the video", "stop a video"],
            "take photo": ["take photo", "take a photo", "tate photo", "take the photo", "teach photo"]
        }
        
        if any(sub in cmd for sub in cmd_variations["start video"]):
            # start camera's video
            print("Starting video")
            self.start_video()

        elif any(sub in cmd for sub in cmd_variations["stop video"]):
            # stop camera's video
            print("Stopping video")
            self.stop_video()
            
        elif any(sub in cmd for sub in cmd_variations["take photo"]):
            # take photo
            print("Taking photo")
            self.take_photo()

        else:
            print("Command not recognized")
     
    def take_photo(self):
        
        if self.is_recording == True:
            print("Cannot take a photo while recording video")
            return
        
        #self.focus_cam()
        picam2.start_and_capture_file(self.get_valid_filename("photo"))
     
    def start_video(self):
        
        if self.is_recording == True:
            print("Already recording; cannot start a new video")
            return
        
        #self.focus_cam()
        picam2.start_and_record_video(self.get_valid_filename("video"))
        self.is_recording = True
        self.time_rec = time.time()
     
    def stop_video(self):
        
        if self.is_recording == False:
            print("Was not recording a video; no video to stop")
            return
        
        picam2.stop_recording()
        self.is_recording = False
        self.time_rec = 0
        print("Stopped the video")
            
    def get_valid_filename(self, recording_type):
        folder = ""
        recording_num = 1
        ext = ""
        match recording_type:
            case "photo":
                folder = "/cam_photos/IMG_"
                ext = ".jpg"
            case "video":
                folder = "/cam_videos/VID_"
                ext = ".mp4"
            case _:
                print("Error in choosing filename - media is not a photo nor video")
                return ""
            
        valid_filename = False
        filename = ""
        
        while not valid_filename:
            filename = '/home/team_125/my_envt/vosk-api' + folder + str(recording_num) + ext
            if os.path.exists(filename):
                recording_num += 1
            else:
                valid_filename = True
                
        return filename
    
    def focus_cam(self):
        autofocus_done = False
        while not autofocus_done:
            autofocus_done = picam2.autofocus_cycle()
        return
