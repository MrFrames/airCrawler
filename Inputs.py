from Abs_date_range import count_up_days, abs2k_date
import os
import pickle

def load_file_obj (filename):
    dir = r'D:\Users\Ben\PycharmProjects\AirBnB_Crawler\Resources'
    name = os.path.join(dir, filename)
    pickle_in = open(name,'rb')
    obj = pickle.load(pickle_in)
    return obj

city_names = load_file_obj('City_names.pickle')
valid_cities = load_file_obj('Valid_cities.pickle')

'''
This file contains:

1) List of hardcoded inputs, process modifiers to control how the crawler will
run.

2) Functions to ensure the inputs are entered correctly.

3) Input modifiers to convert user friendly inputs into forms which can be
directly processed by the program.

4) Test functions to ensure that the input process is functioning as it
should.

'''

sky_scanner_cities = ["bydgoszcz", "gdansk", "pozan",
                      "toulouse", "kerry", "knock",
                      "dublin", "baden-baden", "frankfurt",
                      "reykjavik", "oslo", "stockholme",
                      "venice"]
price_dict = {}

ave_temps_dict = {}

shared = 'y'
room = 'y'
whole_place = 'y'

cities = sky_scanner_cities

outbound_date = '2018-01-28'
return_date = '2018-01-31'
per = 7
reps = 1
pages_returned = 10

budget = 150

'''
Accommodation type - enter y/n, default searches for all.
cities - Enter a list of cities, minimum 1.
dates - enter dates as YYYY-MM-DD. 
per - indicates the repeat period, for example 7 - means the function will 
      search the same period repeating every 7 days. will be 'week'  or 
      'month' later on.
      Note: Periods longer than 28 days can cause errors.
reps - how many times the search period repeats, for instance with a per of 7,
       a rep of 6 will search the same days every week for 6 weeks.
pages_returned - How many pages of results the program should gather data 
                 from, max 17, or 300 listings.
'''

in_list = [shared, room, whole_place, cities, outbound_date, return_date, reps,
           per, pages_returned]

def test_acc_in (room_types):
    '''

    :param acc_list: list containing the tree accomodation inputs

     Checks if the inputs are in the 'y' or 'n' format

    :return: Bool
    '''

    for type in room_types:
        if type != type(True):
            print ("Inputs must be 'y' or 'n'. Input given: {}".format(type))
            return False
    return True

def test_cities_in (cities):
    '''

    :param cities: List of input cities
    :param valid_Cities: List of valid cities

    Checks if the length of the given list is greater than zero and if each
    item in the list is in a pre-approved list of cities. Prints out any
    cities which are spelled wrong, or not valid entries.

    :return: bool - If each item in the list is valid
    '''

    if len(cities) == 0:
        return False
    '''
    for city in cities:
        if city not in city_names:
            print("There is an invalid city in your list: {}".format(city))
            return False
    '''
    return True

def test_date_in (date):
    '''

    :param date: str to be tested

    checks that year, month and day can be converted into an int, and that
    the value between them is a hyphen (required for splitting the string

    :return: True or False

    '''
    if date[4] != '-' or date[7] != '-':
        return False
    try:
        test1 = int(date[:4])+ int(date[5:7]) + int(date[8:])
    except:
        return False
    return True

def test_int_in (int):
    if type (int) != type(4):
        return False
    return True

def test_inputs(in_list):
    ok = True
    a = 0
    test_list = [[test_acc_in,in_list[:3]],
                 [test_cities_in, in_list[3]],
                 [test_date_in, in_list[4], in_list[5]],
                 [test_int_in, in_list[6], in_list[7]]]

    for item in test_list:
        for i in range(1,len(item)):
            a = item[i]
            if not item[0](a):
                return False
    return True

def get_dates_list(outbound_date, return_date, per, reps):
    '''

    :param outbound_date: str - 'YYYY-MM-DD'
    :param return_date: str - 'YYYY-MM-DD'
    :param per: int - period of repetition in days
    :param reps: int - no of repetitions

    Takes inbound date and outbound date, and returns a list of dates
    bounding the same period repeating every 'per' days for 'reps repetitions

    :return: list - containing a of lists in ascending date order:
                sub lits: each containing the outbound date at [0] and the
                return date at [1]
    [[out1,in1],[out2,in2],...[out*reps],[in*reps*]]

    '''
    dates_list = []
    outboundD = outbound_date
    returnD = return_date
    dates_list.append([outboundD, returnD])
    for i in range(0,reps-1):
        outboundD = count_up_days(outboundD, per)
        returnD = count_up_days(returnD, per)
        dates_list.append([outboundD,returnD])
    return dates_list

def test_get_dates_list():
    print ("Testing get_dates_list: ...")
    list = get_dates_list('2018-01-14', '2018-01-17', 7, 150)
    if (abs2k_date(list[110][1])) == 7368:
        print ("Ok for 150 iterations of week periods, including leap years")

def get_itterable():
    type_key_list = ['shared', 'room', 'whole_place']
    none=0
    ittr_list = []
    for i in range (0,3):
        if in_list[i] == 'y':
            ittr_list.append(type_key_list[i])
            none = 1
    if none == 0:
        ittr_list.append('default')
    return ittr_list
