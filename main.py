from scraper import *
from tqdm import tqdm
from sqlalchemy import create_engine, text
import pandas as pd

# # Part 1: Retrieve all metadata from video.ethz.ch

# Create a SQLAlchemy engine
engine = create_engine('sqlite:///lecture_data.db')

# # Retrieve all lecture links from the database
# with engine.connect() as connection:
#     links = connection.execute(text("SELECT url FROM lectures")).fetchall()

# # Uncomment if you want to retrieve links from scratch
# # links = retrieve_lecture_links()

# data = []
# failed = []

# # Process each link and retrieve metadata
# for link in tqdm(links, desc="Retrieving metadata", unit="link"):
#     try:
#         metadata = retrieve_meta_data(link[0])  # Assuming link is a tuple
#         data.append(metadata)
#     except Exception as e:
#         print(f"Failed to retrieve {link[0]}: {e}")
#         failed.append(link[0])

# # Report failures
# print("Failures:")
# if failed:
#     for fail in failed:
#         print(fail)
# else:
#     print("None")

# # Convert the scraped data into a pandas DataFrame
# df = pd.DataFrame(data)
# # Store the DataFrame in the SQLite database
# df.to_sql('lectures', engine, if_exists='replace', index=False)

# Part 2: Retrieve all entries from ETH's course catalogue

# Retrieve course catalogue data
course_data = get_course_catalogue_data()


# Convert the course data into a DataFrame
df_courses = pd.DataFrame(course_data)
# Append the data to the 'catalogue' table in the database
df_courses.to_sql('catalogue', engine, if_exists='append', index=False)
