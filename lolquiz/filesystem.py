import json
import os.path

class FileSystemService(object):
  """Class used to encapsulate file system calls."""
  DATA_FOLDER_PATH="./data"
  
  def saveJsonFile(self, jsonData, filename):
    with open(self.DATA_FOLDER_PATH + '/' + filename, 'w') as jsonFile:
      json.dump(jsonData, jsonFile)
    return

  def readJsonFile(self, filename):
    filePath = self.DATA_FOLDER_PATH + '/' + filename
    if(os.path.exists(filePath)):
      with open(filePath) as realmFile:
        data = json.load(realmFile)
      return data
    else:
      print("Error: " + filePath + " does not exist.")
      raise Exception
    return ""

  def readFile(self, filename):
    with open(self.DATA_FOLDER_PATH + '/' + filename) as file:
      fileString = file.read().strip()
    return fileString

  def appendFile(self, filename, data):      
    with open(self.DATA_FOLDER_PATH + '/' + filename, 'a') as file:
      file.write(data)
    return
