from datetime import date, timedelta
from pprint import pprint

def get_dates():
    today = date.today()
    one_day = timedelta(days=1)
    month_name = [
        "January", "February", "March", 
        "April", "May", "June", 
        "July", "August", "September",
        "October", "November", "December"
    ]
    def __date_to_string(date):
        return "{0:04d}".format(date.year) + "-" + "{0:02d}".format(date.month) + "-" + "{0:02d}".format(date.day)

    dates = {}

    temp = today
    while temp.year == today.year:
        month_no = temp.month
        month = month_name[month_no - 1]
        dates[month] = []
        while temp.month == month_no:
            dates[month].append(__date_to_string(temp))
            temp -= one_day
    return dates