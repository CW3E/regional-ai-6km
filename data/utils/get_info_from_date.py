def get_info_from_date(date):
    yyyy = str(date)[:4]
    mm = str(date)[5:7]
    dd = str(date)[8:10]
    if yyyy == "2020" and mm in ["09", "10", "11", "12"]:
        winter_season = "20-21"
    if yyyy == "2021" and mm in ["01", "02", "03", "04"]:
        winter_season = "20-21"
    if yyyy == "2021" and mm in ["09", "10", "11", "12"]:
        winter_season = "21-22"
    if yyyy == "2022" and mm in ["01", "02", "03", "04"]:
        winter_season = "21-22"
    if yyyy == "2022" and mm in ["09", "10", "11", "12"]:
        winter_season = "22-23"
    if yyyy == "2023" and mm in ["01", "02", "03", "04"]:
        winter_season = "22-23"
    return yyyy, mm, dd, winter_season

