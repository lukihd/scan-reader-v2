from bs4 import BeautifulSoup
from pathlib import Path
import shutil
import urllib3

'''
function checkDir         - Check if a directory with the name of the manga is created
param dirPath             - Path to directory we check / create
param dirName             - Name of directory
''' 
def checkDir(dirPath, dirName):
    try:
        # Create target Directory
        Path(f"{dirPath}").mkdir()
        print("Directory ", dirName, " Created ")
    except FileExistsError:
        print("Directory ", dirName, " already exists")
    return dirName

'''
function getUrl          - Used to retrieve html code and return links of scan's images
param {str} url          - Url of chapter
'''
def getUrl(url):
  output = []

  # Make get request to retrieve code of the chapter page
  http = urllib3.PoolManager()
  res = http.request('GET', url)

  # Check if we get a valid request code and parse HTML for retrieving only img tag
  if res.status == 200:
    soup = BeautifulSoup(res.data, 'html.parser')
    imgs = soup.find(id="all").find_all('img')
    index = 1
    for img in imgs:
      if index < 10:
        output.append({
          "page": f"0{index}",
          "link": str(img['data-src']).strip()
        })
      else:
        output.append({
          "page": index,
          "link": str(img['data-src']).strip()
        })
      index += 1
    print('Chapter\'s urls retrieved')
    return output
  # return invalid request code
  else:
    print(f"Error : HTTP code {res.status}")
    return False

'''
function dowload         - Download scan from url and save it to a local specific path
param {str} url          - url of scan's page
param {str} localPath    - path where image are stored on the user machine
param {str} filename     - filename of this image
'''
def download(url, path, filename):
  # Retrieve image and store it in the path bellow
  http = urllib3.PoolManager()
  with http.request('GET', url, preload_content=False) as res, open(filename, 'wb') as f:
    shutil.copyfileobj(res, f)
  del res
  shutil.move(filename, f"{path}/{filename}")


'''
MUST CHANGE IN THE FUTURE FOR USER INTERFACE ADAPTATION

function manager          - This is the main function, we use each bellow function and manage them to downlad all the scans we want.
param {str} name          - Name of the manga to retrieve. Need to be same as website url
param {int} startChapter  - Chapter where we start downloading
param {int} endChapter    - Chapter where we stop downloading 
param {str} dirPath       - Path to directory we save images
param {bool} isHome       - Is it save in the default user folder
'''
def manager(name, startChapter, endChapter, dirPath, isHome):
  # Set file path
  path = ""
  if isHome == True:
    path = f"{Path.home()}/{dirPath}/{name}"
  else:
    path = f"{dirPath}/{name}"

  # Create directory if not exist
  checkDir(f"{path}", name)
  print(path)
  # Start parse chapter and download each page of each chapter
  currentChapter = startChapter
  while currentChapter < endChapter: 
    scans = getUrl(f"https://www.scan-vf.net/{name}/chapitre-{currentChapter}")
    for scan in scans:
      if currentChapter < 10: 
        filename = f"0{currentChapter}-{scan['page']}.png"
      else:
        filename = f"{currentChapter}-{scan['page']}.png"
      download(scan['link'], path, filename)
      print('Page downloaded')
    currentChapter += 1
    print('Chapter downloaded')
  print('Operation complete')

# TEST WORKING
manager('one_piece', 1, 10, '.scan-r2', True)

