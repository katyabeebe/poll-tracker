from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# Request to website and download HTML contents
url='https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html'
req=requests.get(url)
content=req.text

# Create empty list
data = []
  
# Get the header 
list_header = []
soup = BeautifulSoup(content,'html.parser')
header = soup.find_all("table")[0].find("thead")
 
for items in header:
    try:
        list_header.append(items.get_text())
    except:
        continue
 
# Get the data
HTML_data = soup.find_all("table")[0].find_all("tr")[1:]
 
for element in HTML_data:
    sub_data = []
    for sub_element in element:
        try:
            sub_data.append(sub_element.get_text())
        except:
            continue
    data.append(sub_data)
 
# Storing the data into Pandas DataFrame
dataFrame = pd.DataFrame(data = data, columns = list_header)

# Save file to CSV
cwd_dir = os.getcwd()
raw_data_path = 'data/raw_polls.csv'
dataFrame.to_csv(os.path.join(cwd_dir, raw_data_path), index=False)
print("Raw data saved in", os.path.join(cwd_dir, raw_data_path))
