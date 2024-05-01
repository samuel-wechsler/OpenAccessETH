# Evaluation of Accessibility of ETH Lecture Recordings

## Overview
This repository contains Python scripts designed to scrape, store, and analyze video lecture links and metadata from the ETH Zurich video portal ([https://video.ethz.ch/](https://video.ethz.ch/)). The goal of this project is to assess the accessibility of lecture recordings offered by ETH Zurich.

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

**Check: get_department_links**
  - Outcome: No duplicate department URLs were found.
  - Validation: The number of department links matched expectations.

**Check: get_years**
  - Outcome: No duplicate year links were found.
  - Validation: The number of year links was correct.

**Check: get_semester**
  - Outcome: No duplicate semester links were found.
  - Validation: The number of semesters matched expectations.

**Check: get_lectures**
  - Outcome: No duplicate lecture links were found.
  - Validation: The number of lectures was correct.

**Check: get_course_catalogue**
  - Outcome: No duplicate courses were found.
  - Validation: The number of courses matched expectations.

These checks confirm the reliability of the scraper module in accurately collecting and processing the required data from the ETH Zurich video portal.
