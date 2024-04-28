# ETH Lecture Video Scraper

This project provides tools for scraping, storing, and analyzing lecture video links and metadata from the ETH Zurich video portal. The goal is to automate the collection of lecture information and facilitate easy access to lecture series across various departments and years.

## Project Structure

This codebase is organized into three main components:

- **scraper.py**: Handles the scraping of lecture links and metadata from the website.
- **main.py**: Integrates the scraping functions and manages data storage into a SQLite database.
- **visuals.py**: Offers visualization tools to analyze the scraped data visually.

### scraper.py

Responsible for:
- Fetching HTML content from the specified URLs.
- Parsing the HTML to extract links to lecture videos and metadata.
- Providing structured metadata from each lecture page.

### main.py

Serves as the entry point of the application, where:
- All available lecture links are retrieved and processed.
- Metadata for each lecture is fetched and stored in a database.
- Errors during the scraping process are handled and logged.

### visuals.py

Used for generating visual insights into the data collected:
- Connects to the SQLite database to query data.
- Uses matplotlib to generate bar charts and other graphs to display lecture accessibility and other metrics.

## Installation

Before running the project, ensure you have Python 3.8+ installed and then install the required dependencies:

```bash
pip install requests beautifulsoup4 pandas sqlalchemy matplotlib
