class Camera:

    def __init__(self):
        # initialize camera
        pass

    def do_command(self, cmd):
        """
        Execute camera action based on detected voice command
        """
        
        match cmd:

            case "start video":
                # start camera's video
                print("Starting video")

            case "stop video":
                # stop camera's video
                print("Stopping video")

            case "take photo":
                # take photo
                print("Take photo")

            case _:
                print("Command not recognized")


