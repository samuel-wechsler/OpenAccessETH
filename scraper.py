"""
This module provides tools for scraping and extracting structured information from the 'video.ethz.ch' website.
It retrieves lecture video links along with related metadata such as title, description, and access status.
"""

import re
import json
import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define session to handle cookies and authentication
SESSION = requests.Session()


def get_html(url):
    """
    Retrieves HTML content from a specified URL using a session with custom headers.

    Args:
    url (str): URL of the website to retrieve HTML from.

    Returns:
    BeautifulSoup object: Parsed HTML content of the webpage.
    """

    # Define headers to mimic a legitimate browser requestpyth
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Referer": "https://example.com/",
    }

    try:
        response = SESSION.get(url, headers=headers)
        response.raise_for_status()  # Raises a HTTPError for bad responses
        return BeautifulSoup(response.content, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_department_links(url):
    """
    Extracts unique department-specific lecture links from a given URL.

    Args:
    url (str): URL of the main site to extract links from.

    Returns:
    list: Unique URLs of department-specific lecture sections.
    """
    soup = get_html(url)

    soup = get_html(url)
    if not soup:  # Check if the HTML was not fetched successfully
        return []

    links = []
    for link in soup.find_all("a", href=True):
        full_url = urljoin(url, link["href"])
        # Improve filtering: Ensure only valid department links are considered
        if "lectures/" in link["href"] and full_url.startswith("https://"):
            links.append(full_url)

    return list(set(links))  # set-list conversion to avoid duplicates


def get_years(department_url):
    """
    Extracts unique year-specific links from a department URL.

    Args:
    department_url (str): URL of the department page.

    Returns:
    list: Unique URLs for different academic years.
    """
    department = (department_url.split("/")[4]).split(".")[0]
    year_links = []

    soup = get_html(department_url)
    links = soup.find_all("a")

    for link in links:
        link = link["href"]

        # very hackish criterion but it works...
        if f"/lectures/{department}/" in link and ".html" in link and len(link.split("/")) == 4:
            year_link = urljoin(department_url, link)
            year_links.append(year_link)

    return list(set(year_links))


def get_semester(year_link):
    """
    Extracts semester-specific links from a year URL.

    Args:
    year_link (str): URL of the year-specific page.

    Returns:
    list: URLs for the 'spring' and 'autumn' semesters if available.
    """
    soup = get_html(year_link)
    if not soup:
        return []

    semester_links = []
    max_links = 2  # because there are only two semesters each year :)

    for link in soup.find_all("a", href=True):
        if "spring.html" in link["href"]:
            semester_links.append(
                urljoin(year_link.replace(".html", "") + "/", "spring.html"))
        elif "autumn.html" in link["href"]:
            semester_links.append(
                urljoin(year_link.replace(".html", "")+"/", "autumn.html"))
        if max_links and len(semester_links) >= max_links:
            break

    return list(set(semester_links))


def get_lectures(url):
    """
    Retrieves all lecture video links from a given semester page URL.

    Args:
    url (str): URL of the semester page.

    Returns:
    list: Links to individual lecture videos.
    """
    soup = get_html(url)
    if not soup:
        return []

    department = (url.split("/")[4]).split(".")[0]
    lecture_links = []
    for link in soup.find_all("a"):
        link = link["href"]
        if len(link.split("/")) == 6 and department in link:
            link = urljoin(url+"/", link)
            lecture_links.append(link)

    return list(set(lecture_links))


def retrieve_lecture_links_department(department_site):
    """
    Extracts all lecture links for a given department over all years and semesters.

    Args:
    department_site (str): URL of the department.

    Returns:
    list: All unique lecture links found.
    """
    print(f"Starting link retrieval for {department_site}")

    links = []
    years = get_years(department_site)

    for year in years:
        semesters = get_semester(year)
        for semester in semesters:
            lectures = get_lectures(semester)
            links.extend(lectures)

    unique_links = list(set(links))
    print(
        f"Completed link retrieval for {department_site}, found {len(unique_links)} links")
    return unique_links


def retrieve_lecture_links():
    """
    Retrieves all available lecture links from the main site 'https://video.ethz.ch'.

    Returns:
    list: All unique lecture links found on the site.
    """
    url = "https://video.ethz.ch/"
    links = []

    departments = get_department_links(url)
    for department in departments:
        print("Scraping lectures links from: ", department)
        years = get_years(department)
        for year in years:
            semesters = get_semester(year)

            for semester in semesters:
                lectures = get_lectures(semester)
                links.extend(lectures)
    unique_links = list(set(links))
    print(f"Total unique lecture links retrieved: {len(unique_links)}")
    return unique_links


def get_json(lecture_url):
    """
    Retrieves JSON metadata for a given lecture page.

    Args:
    lecture_url (str): URL of the lecture page.

    Returns:
    dict: JSON data extracted from the metadata link.
    """
    json_url = lecture_url.replace(".html", "") + ".series-metadata.json"
    json_data = json.loads(get_html(json_url).text)
    return json_data


def check_access(json_data):
    """
    Determines if a lecture is publicly accessible based on its metadata.

    Args:
    json_data (dict): Metadata JSON of a lecture.

    Returns:
    bool: True if lecture is accessible without restrictions, False otherwise.
    """
    # Find the protection token
    protection_token = json_data.get("protection")
    return protection_token == "NONE"


def retrieve_meta_data(lecture_url):
    """
    Retrieves and structures essential metadata from a lecture URL.

    Args:
    lecture_url (str): URL of the lecture.

    Returns:
    dict: A dictionary containing structured metadata of the lecture.
    """
    meta = dict()

    json_data = get_json(lecture_url)
    url_data = lecture_url.split("/")

    meta = {
        "title": json_data.get('title'),
        "description": json_data.get("description"),
        "department": url_data[4],
        "year": url_data[5],
        "no_lectures": len(json_data.get("episodes")),
        "lecturer": ", ".join(json_data.get("selectedEpisode")["createdBy"]),
        "url": lecture_url,
        "access": check_access(json_data)
    }

    return meta


def extract_catalogue_metadata(html, year):
    """
    """
    data = []

    department = {
        "Architecture": "d-arch",
        "Civil, Environmental and Geomatic Engineering": "d-baug",
        "Biosystems Science and Engineering": "d-bsse",
        "Computer Science": "d-infk",
        "Information Technology and Electrical Engineering": "d-itet",
        "Mechanical and Process Engineering": "d-mavt",
        "Materials": "d-matl",
        "Biology": "d-biol",
        "Chemistry and Applied Biosciences": "d-chab",
        "Mathematics": "d-math",
        "Physics": "d-phys",
        "Earth Sciences": "d-erdw",
        "Environmental Systems Science": "d-usys",
        "Health Sciences and Technology": "d-hest",
        "Management, Technology, and Economics": "d-mtec",
        "Humanities, Social and Political Sciences": "d-gess"
    }

    for row in html.find_all('tr')[1:]:  # Assuming the first row is header
        cols = row.find_all('td')
        data.append({
            'Name': cols[0].text.strip() + ", " + cols[1].text.strip(),
            'Field': cols[3].text.strip(),
            'Department': department[cols[4].text.strip()],
            'year': str(year)
        })

    return data


def get_course_catalogue(url=None):
    catalogue_data = []

    # just for testing
    if url is not None:
        html = get_html(url)
        data = extract_catalogue_metadata(html, "2024")
        catalogue_data.extend(data)
        return catalogue_data

    for year in range(2018, 2025):
        for semester in ["W", "S"]:
            # specify url
            semester = str(year) + semester
            base_url = f"https://www.vvz.ethz.ch/Vorlesungsverzeichnis/sucheDozierende.view?rufname=&stammDeptId=&famname=&deptId=&bereichAbschnittId=&orderByColId=0&semkez={semester}&studiengangAbschnittId=&unterbereichAbschnittId=&studiengangTyp=&seite=0&lang=en"

            # get html
            html = get_html(base_url)

            # extract metadata from html and add to list
            data = extract_catalogue_metadata(html, year)
            catalogue_data.extend(data)

    return catalogue_data
