# Evaluation of Accessibility of ETH Lecture Recordings

## Overview
This repository contains Python scripts for scraping, storing, and analyzing video lecture links and metadata from the ETH Zurich video portal ([https://video.ethz.ch/](https://video.ethz.ch/)). The objective is to evaluate the accessibility of lecture recordings provided by ETH Zurich.

## Data Availability
The datasets obtained and compiled in this project are available in both SQL and CSV formats. For every lecture series listed on the ETH Zurich video portal, the following metadata is captured:
- **title** (str): The title of the lecture series.
- **description** (str): A brief description of the lecture series.
- **department** (str): The academic department responsible for the lecture.
- **year** (str): The academic year when the lectures were recorded.
- **no_lectures** (int): The number of video recordings available for the lecture series.
- **lecturer** (str): The name(s) of the instructor(s) delivering the lectures.
- **url** (str): The direct link to the lecture series.
- **access** (bool): Indicates the accessibility status (1 for public, 0 for restricted).

## Project Structure
The codebase is organized into three primary components:

### `scraper.py`
Responsible for:
- Fetching HTML content from the specified URLs.
- Parsing the HTML to extract links to lecture videos and associated metadata.
- Structuring the extracted metadata for further processing.

### `main.py`
Serves as the entry point of the application, where:
- Lecture links are retrieved and processed.
- Metadata for each lecture is fetched and stored in a SQLite database.
- Errors during the scraping process are managed and logged.

### `visuals.py`
Used for generating visual insights from the collected data:
- Connects to the SQLite database to retrieve data.
- Utilizes matplotlib to create bar charts and other visualizations to display metrics such as lecture accessibility.

## Usage
To use these scripts, follow the setup instructions in the README file. Ensure that all dependencies are installed, and execute `main.py` to begin data collection.

To recreate the plots, execute `visuals.py`.
