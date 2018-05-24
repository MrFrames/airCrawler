
def YYYY_MM_DD (date):
    date_list = []
    for value in date.split('-'):
        date_list.append(int(value))
    return (date_list)

def recon_date(date):
    days = str(date[2])
    months = str(date[1])
    years = str(date[0])

    year = '0' * (4 - len(years)) + years
    months = '0' * (2 - len(months)) + months
    days = '0' * (2 - len(days)) + days

    date_str = years + '-' + months + '-' + days
    return date_str

def get_days_from_month (month, leap_year):
    feb = 28
    if leap_year == True:
        feb = 29
    month_days_list = [31, feb, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_to_month = 0
    for i in range (0,month-1):
        days_to_month += month_days_list[i]
    return days_to_month

def test_get_days_to_month():
    print ('Feb given, should return 31, returns: {}'.format(get_days_to_month(2,False)))
    print('March given, leap year False, should return 59, returns: {}'.format(get_days_to_month(3, False)))
    print('March given, leap year True, should return 60, returns: {}'.format(get_days_to_month(3, True)))

def is_leap_year (year):
    if not year%4 == 0:
        return False
    elif not year%100 == 0:
        return True
    elif not year%400 == 0:
        return False
    else:
        return True

def days_from_years(years):
    days = 0
    for i in range(2000,years):
        if is_leap_year(i)== True:
            days += 366
        else:
            days += 365
    return days

def abs2k_date (date):
    print ("date: " + str(date))
    dl = YYYY_MM_DD(date)
    leap = is_leap_year(dl[0])
    from_years = days_from_years(dl[0])
    from_month = get_days_from_month(dl[1],leap)
    days = dl[2]-1
    return (from_years+from_month+days)

def get_days_in_month (month, leap_year):
    feb = 28
    if leap_year == True:
        feb = 29
    month_comp = month-1
    month_days_list = [31, feb, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return month_days_list[month_comp]

def count_up_days (current_date, add_days):
    broken = YYYY_MM_DD(current_date)

    day = broken[2]
    month = broken[1]
    year = broken[0]

    days = int(day) + int(add_days)
    leap_year = is_leap_year(year)
    days_in_month = get_days_in_month(month, leap_year)
    while days > days_in_month:
        days = days - days_in_month
        month = month + 1
        if month == 13:
            month = 1
            year = year+1
    return (recon_date([year,month,days]))



def test_count_days ():
    date1 = "2018-01-12"
    days = 22
    print ("Testing count_days with '2018-01-12' plus 22 days, should return '2018-02-03: ")
    new_date = count_up_days(date1,days)
    print (new_date)