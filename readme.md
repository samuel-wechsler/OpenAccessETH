# Evaluation of Accessibility of ETH Lecture Recordings

## Overview
This repository contains a collection of Python scripts to evaluate the lecture accessibility of lecture recordings by ETH Zurich. Two main data sources are integrated into a SQL database:
1. Metadata from ETH Zurich video portal ([https://video.ethz.ch/](https://video.ethz.ch/)) 
2. ETHZ course catalogue ([https://www.vvz.ethz.ch/Vorlesungsverzeichnis/sucheLehrangebotPre.view?lang=de](https://www.vvz.ethz.ch/Vorlesungsverzeichnis/sucheLehrangebotPre.view?lang=de))

## Data Availability
The datasets compiled in this project are accessible in both SQL and CSV formats. For each lecture series featured on the ETH Zurich video portal, the following metadata is captured:
- **Title** (str): The official title of the lecture series.
- **Description** (str): A concise description of the lecture series.
- **Department** (str): The academic department that oversees the lecture.
- **Year** (str): The academic year in which the lectures were recorded.
- **No_Lectures** (int): The total number of video recordings available for the lecture series.
- **Lecturer** (str): The instructor(s) responsible for delivering the lectures.
- **URL** (str): The direct link to the lecture series.
- **Access** (bool): The accessibility status of the lectures (1 for public, 0 for restricted).

## Project Structure
The codebase is divided into three primary modules:

### `scraper.py`
This module is tasked with:
- Downloading HTML content from specified URLs.
- Parsing the HTML to extract links to lecture videos and relevant metadata.
- Organizing the extracted metadata for subsequent analysis.

### `main.py`
This module acts as the application's entry point, where:
- Lecture links are collected and processed.
- Metadata for each lecture is retrieved and stored in a SQLite database.
- Any errors encountered during the scraping process are logged and handled.

### `visuals.py`
This module is responsible for generating visual data insights:
- It connects to the SQLite database to fetch data.
- It uses matplotlib to produce bar charts and other visualizations that showcase metrics such as the accessibility of the lectures.

## Usage
Follow the setup instructions detailed in the README file to utilize these scripts. Ensure all dependencies are installed and run `main.py` to start the data collection process.

To regenerate the visualizations, run `visuals.py`.

## Proof of Concept
The efficacy of the scraper module (`scraper.py`) was validated through detailed testing of each function using a manageable subset of URLs. The results of these tests are documented in `test.py` and are summarized below:

Check: get_department_links
  - No duplicate department urls found.
  - Correct number of departments.

Check: get_years
  - No duplicate year links found.
  - Correct number of years.

Check: get_semester
  - No duplicate semester links found.
  - Correct number of semesters.

Check: get_lectures
  - No duplicate lecture links found.
  - Correct number of lectures.

Check: get_course_catalogue
  - No duplicate courses found.
  - Correct number of courses. 

These tests establish some reliability of the scraper module in collecting and processing data from the indicated sources.
