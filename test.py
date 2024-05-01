from scraper import *

# Checking get_department_links
print("\nCheck: get_department_links")
url = "https://video.ethz.ch/"
department_links = sorted(get_department_links(url))

# Check for duplicates
if len(department_links) != len(set(department_links)):
    print("  -> Duplicates found!")
else:
    print("  -> No duplicate department urls found.")
# Check the length
if len(department_links) != 16:
    print("  -> Length is not 16!")
else:
    print("  -> Correct number of departments.")

# Checking get_years function: (recordings available from 2011-2024)
sample_url = "https://video.ethz.ch/lectures/d-phys.html"
year_links = get_years(sample_url)

print("\nCheck: get_years")
# Check for duplicates in year links
if len(year_links) != len(set(year_links)):
    print("  -> Duplicates found in year links!")
else:
    print("  -> No duplicate year links found.")
# Check the length of year links
if len(year_links) != 14:
    print("  -> Length of year links is not 14!")
else:
    print("  -> Correct number of years.")

# Check: get_semester (expected: spring semester only)
sample_url = "https://video.ethz.ch/lectures/d-phys/2024.html"
semester_links = get_semester(sample_url)

print("\nCheck: get_semester")
# Check for duplicates in semester links
if len(semester_links) != len(set(semester_links)):
    print("  -> Duplicates found in semester links!")
else:
    print("  -> No duplicate semester links found.")
# Check the length of semester links
if len(semester_links) != 1:
    print("  -> Length of semester links is not 1!")
else:
    print("  -> Correct number of semesters.")

# Check: get_lectures (expected: 10 lecture links, no duplicates)
sample_url = "https://video.ethz.ch/lectures/d-phys/2018/autumn.html"
lecture_links = get_lectures(sample_url)

print("\nCheck: get_lectures")
# Check for duplicates in lecture links
if len(lecture_links) != len(set(lecture_links)):
    print("  -> Duplicates found in lecture links!")
else:
    print("  -> No duplicate lecture links found.")
# Check the length of lecture links
if len(lecture_links) != 10:
    print("  -> Length of lecture links is not 10!")
else:
    print("  -> Correct number of lectures.")


# Checking: get_course_catalogue (expected: 30 lectures, no duplicates)
url = "https://www.vvz.ethz.ch/Vorlesungsverzeichnis/sucheDozierende.view?lang=en&search=on&semkez=2024S&stammDeptId=&famname=&rufname=&studiengangTyp=&deptId=&studiengangAbschnittId=&search=Search"
catalogue = get_course_catalogue(url)

# Convert the list of dictionaries into a list of tuples
catalogue_tuples = [tuple(course.items()) for course in catalogue]

print("\nCheck: get_course_catalogue")
# Check for duplicates in course catalogue
if len(catalogue_tuples) != len(set(catalogue_tuples)):
    print("  -> Duplicates found in course catalogue!")
else:
    print("  -> No duplicate courses found.")
# Check the length of course catalogue
if len(catalogue_tuples) != 30:
    print("  -> Length of course catalogue is not 30!")
else:
    print("  -> Correct number of courses.")
