import os


class VirtualButton:
    """
    The virtual button can be pressed by creating an empty file VIRTUAL_BUTTON 
    at the same place as this script. The file will be deleted automatically 
    after it has been read.
    """
 
    FILE_NAME = 'VIRTUAL_BUTTON'

    def read(self):
        file_exists = os.path.exists(self.FILE_NAME)
        if file_exists:
            os.remove(self.FILE_NAME)
        return file_exists