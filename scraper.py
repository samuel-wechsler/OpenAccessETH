"""

"""

import json
import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_html(url):
    """
    retrieves html content from a given website
    """
    # Define headers to mimic a legitimate browser requestpyth
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Referer": "https://example.com/",
    }

    # Define session to handle cookies and authentication
    session = requests.Session()

    # Make a GET request to the URL
    response = session.get(url, headers=headers)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    return soup


def get_department_links(url):
    """
    Retrieves all links to video lectures of ETH departments.
    """
    soup = get_html(url)

    links = soup.find_all("a")
    department_links = []

    for link in links:
        if 'href' in link.attrs and "lectures/" in link["href"]:
            department_links.append(urljoin(url, link["href"]))

    department_links = list(set(department_links))  # Remove duplicates
    return department_links


def get_years(department_url):
    """
    returns available years, semesters
    """
    department = (department_url.split("/")[4]).split(".")[0]
    found = []

    soup = get_html(department_url)
    links = soup.find_all("a")

    for link in links:
        link = link["href"]

        if f"/lectures/{department}/" in link and ".html" in link and len(link.split("/")) == 4:
            year_link = urljoin(department_url, link)
            found.append(year_link)

    return list(set(found))


def get_semester(year_link):
    soup = get_html(year_link)
    links = soup.find_all("a")
    found = []

    for link in links:
        link = link["href"]

        if len(found) >= 2:
            break

        elif "/spring.html" in link:
            found.append(urljoin(year_link+"/", "spring.html"))

        elif "/autumn.html" in link:
            link = urljoin(year_link, "autumn.html")
            found.append(urljoin(year_link+"/", "autumn.html"))

    return found


def get_lectures(url):
    """
    """
    soup = get_html(url)
    department = (url.split("/")[4]).split(".")[0]

    links = soup.find_all("a")

    found = []

    for link in links:
        link = link["href"]

        if len(link.split("/")) == 6 and department in link:
            link = urljoin(url+"/", link)
            found.append(link)

    return found


def retrieve_lecture_links_department(department_site):
    """
    Function which exhaustively searches all lecture links(i.e., from different years, courses, and so on)
    returns a list of links to lectures
    """
    links = []

    years = get_years(department_site)

    for year in years:
        semesters = get_semester(year)

        for semester in semesters:
            lectures = get_lectures(semester)

            links.extend(lectures)

    return list(set(links))


def retrieve_lecture_links():
    """
    retrieves all lecture links available on video.ethz.ch
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

    return list(set(links))


def get_json(lecture_url):
    json_url = lecture_url.replace(".html", "") + ".series-metadata.json"
    json_data = json.loads(get_html(json_url).text)
    return json_data


def check_access(json_data):
    """
    """
    # Find the protection token
    protection_token = json_data.get("protection")

    return protection_token == "NONE"


def retrieve_meta_data(lecture_url):
    meta = dict()

    json_data = get_json(lecture_url)
    url_data = lecture_url.split("/")

    meta = {
        "title": json_data.get('title'),
        "description": json_data.get("description"),
        "department": url_data[4],
        "year": url_data[5],
        "no_lectures": len(json_data.get("episodes")),
        "lecturer": json_data.get("createdBy"),
        "url": lecture_url,
        "access": check_access(json_data)
    }

    return meta
