from bs4 import BeautifulSoup
from create_html import create_html
import json


def get_timetable(url, group_name):
    with open("index.html", "r", encoding="UTF-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    all_days = soup.find("div", class_="tab_content", id="all_weeks").find_all('h3', class_="rasp-weekday-title")
    group_timetable_dict = {}
    for day in all_days:
        day_dict = {}
        day_name = day.text
        day_info = day.find_next("table", class_="rasp")

        subjects_info_list = []
        time_hour = ""
        for subject in day_info.find_all('tr'):
            time_discipline = subject.find("td", class_="time-discipline")
            try:
                subject_subgroup = time_discipline.find("span", class_="event-subgroup").text
            except AttributeError:
                subject_subgroup = "None"
            week_type = subject.find("td", class_="time-discipline").find_previous('td').get('class')
            if week_type[1] == "weektype-0":
                week_type = "Ч/З"
            elif week_type[1] == "weektype-1":
                week_type = 'Ч'
            elif week_type[1] == "weektype-2":
                week_type = 'З'
            subject_type = time_discipline.find("span", class_="event-type").text
            subject_name = ""
            for name in time_discipline.find_all("span"):
                subject_name = name.next_sibling.strip()
                if subject_name:
                    break
            try:
                time_hour = subject.find("td", class_="time-hour").text.strip()
                subjects_info_list = []
            except AttributeError:
                pass
            subjects_info_list.append([week_type, subject_subgroup, subject_type, subject_name])
            day_dict.update({time_hour: subjects_info_list})
        group_timetable_dict.update({day_name: day_dict})
    timetable_dict = {}
    timetable_dict.update({group_name: group_timetable_dict})
    with open("timetable.json", "w", encoding="UTF-8") as file:
        json.dump(timetable_dict, file, indent=4, ensure_ascii=False)
    return


if __name__ == "__main__":
    link = "https://pnu.edu.ru/rasp/groups/65538/"
    group_name = "ИС(б) - 11"
    create_html(link)
    get_timetable(link, group_name)
