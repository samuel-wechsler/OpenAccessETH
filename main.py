from scraper import *
from tqdm import tqdm
from sqlalchemy import *
import pandas as pd


# Create a sqlalchemy engine
engine = create_engine('sqlite:///lecture_data.db')

# Uncomment if you want to retrieve links from scratch
# links = retrieve_lecture_links()

# Retrieve all lecture links from the database
links = engine.connect().execute(text("SELECT url FROM lectures")).fetchall()

data = []
failed = []

for link in tqdm(links, unit="link"):
    try:
        data.append(retrieve_meta_data(link[0]))
    except Exception as e:
        print("Failed: ", e)
        failed.append(link[0])

print("Failures")
if len(failed) == 0:
    print("None")
for fail in failed:
    print(fail)


# Convert the scraped data into a pandas DataFrame
df = pd.DataFrame(data)

# Store the DataFrame in the SQLite database
df.to_sql('lectures', engine, if_exists='replace')
