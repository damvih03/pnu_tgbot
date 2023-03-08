from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import datetime


async def get_page_data(session, page, group_name):
    headers = {}
    url = f"https://pnu.edu.ru/rasp/groups/{page}"
    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "lxml")
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
        with open("timetable.json", 'r', encoding="UTF-8") as file:
            timetable_dict = json.load(file)
        timetable_dict.update({group_name: group_timetable_dict})
        with open("timetable.json", "w", encoding="UTF-8") as file:
            json.dump(timetable_dict, file, indent=4, ensure_ascii=False)
        print(f"[INFO] Обработана страница группы '{group_name}'")


async def gather_data():
    with open("groups_info.json", 'r', encoding="UTF-8") as file:
        groups_info_dict = json.load(file)
    urls = []
    group_names_list = []
    for faculty in groups_info_dict.keys():
        for course in groups_info_dict[faculty].keys():
            for group in groups_info_dict[faculty][course].keys():
                urls.append(groups_info_dict[faculty][course].get(group))
                group_names_list.append(group)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for page, group_name in zip(urls, group_names_list):
            task = asyncio.create_task(get_page_data(session, page, group_name))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())


if __name__ == "__main__":
    time_start = datetime.datetime.now()
    main()
    time_end = datetime.datetime.now()
    print(f"Время работы скрипта: {time_end - time_start}")
