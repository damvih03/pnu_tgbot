from bs4 import BeautifulSoup
from create_html import create_html
import json


def get_faculties():
    with open("index.html", "r", encoding="UTF-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    all_faculties_dict = {}
    for faculty in soup.find_all('p', class_="btn-slide inst_name"):
        faculty_short_name = faculty.find('b').text
        faculty_full_name = faculty.find("a").text.replace(f"({faculty_short_name})", "")
        all_faculties_dict.update({faculty_short_name: faculty_full_name})
    with open("faculties.json", "w", encoding="UTF-8") as file:
        json.dump(all_faculties_dict, file, indent=4, ensure_ascii=False)
    return list(all_faculties_dict.keys())


def get_groups():
    with open("index.html", "r", encoding="UTF-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    faculties_names_list = get_faculties()
    faculties_groups_dict = {}  # Faculties groups
    all_faculties_html = soup.find_all("div", class_="panel_gallery")
    for faculty in all_faculties_html:
        all_courses = faculty.find('tr').find_all('th')
        all_faculty_groups = faculty.find('tr').find_next('tr').find_all('td')

        faculty_groups_dict = {}
        for course, groups in zip(all_courses, all_faculty_groups):
            course = course.text
            groups_links_dict = {}
            for group in groups.find_all('a'):
                group_name = group.text
                group_link = group.get('href')
                groups_links_dict.update({group_name: group_link})
            faculty_groups_dict.update({course: groups_links_dict})
        faculties_groups_dict.update({faculties_names_list[all_faculties_html.index(faculty)]: faculty_groups_dict})
        with open("groups_info.json", "w", encoding="UTF-8") as file:
            json.dump(faculties_groups_dict, file, indent=4, ensure_ascii=False)

    return True


def main():
    url = "https://pnu.edu.ru/rasp/groups/"
    create_html(url)
    get_groups()
    return True


if __name__ == "__main__":
    main()
