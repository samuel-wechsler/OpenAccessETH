from scraper import *
from tqdm import tqdm
from sqlalchemy import *
import pandas as pd

data = []
failed = []

dchab_url = "https://video.ethz.ch/lectures/d-chab.html"

for link in tqdm(retrieve_lecture_links()):
    try:
        data.append(retrieve_meta_data(link))
    except Exception as e:
        print("Failed: ", e)
        failed.append(link)


# Create a SQLite database
engine = create_engine('sqlite:///lecture_data.db')

# Convert the scraped data into a pandas DataFrame
df = pd.DataFrame(data)

# Store the DataFrame in the SQLite database
df.to_sql('lectures', engine, if_exists='replace')
