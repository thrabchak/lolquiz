import json
import os.path

class FileSystemService(object):
  """Class used to encapsulate file system calls."""
  DATA_FOLDER_PATH = os.path.join(os.path.dirname(__file__), '..', "data")
  
  def saveJsonFile(self, jsonData, filename):
    filePath = os.path.join(self.DATA_FOLDER_PATH, filename)
    with open(filePath, 'w') as jsonFile:
      json.dump(jsonData, jsonFile)
    return

  def readJsonFile(self, filename):
    filePath = os.path.join(self.DATA_FOLDER_PATH, filename)
    if(os.path.exists(filePath)):
      with open(filePath) as realmFile:
        data = json.load(realmFile)
      return data
    else:
      print("Error: " + filePath + " does not exist.")
      raise Exception
    return ""

  def readFile(self, filename):
    filePath =os.path.join(self.DATA_FOLDER_PATH, filename)
    with open(filePath) as file:
      fileString = file.read().strip()
    return fileString

  def appendFile(self, filename, data):
    filePath = os.path.join(self.DATA_FOLDER_PATH, filename)
    with open(filePath, 'a') as file:
      file.write(data)
    return

  def exists(self, filename):
    filePath = os.path.join(self.DATA_FOLDER_PATH, filename)
    return os.path.exists(filePath)
