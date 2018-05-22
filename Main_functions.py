import pickle
import mechanicalsoup
import re
import os.path
import time
from PyQt5.Qt import QDateTime

def airBnB(in_list):
    print ("Innitialising...")
    filename = get_file_name(in_list)
    save_to_index (filename,in_list)
    innit_progress = check_progress(filename)
    for a in range(int(innit_progress[0]), len(ittr_room_type)):
        type = ittr_room_type[a]
        for b in range (int(innit_progress[1]), len(in_list[3])):
            city = in_list[3][b]
            for c in range (int(innit_progress[2]), len(date_list)):
                dates = date_list[c]
                progress = [a, b, c]
                print (progress)
                data_list = []
                data_filename = get_data_file_name(filename,progress,city)
                data = get_data(get_url(type,city,dates,0))
                for item in data:
                    data_list.append(item + [1] + [city] + [type])
                for page in range (2,in_list[8]+1):
                    data = get_data(get_url(type,city,dates,page))
                    for item in data:
                        data_list.append(item + [page] + [city] + [type])

                save_data(data_list,data_filename)
                save_progress (filename,progress)


# Below are functions relating to storage of data

direct = "data/"



def get_file_name(in_list):
    name = str(in_list[0]) + ',' + str(in_list[1]) + ',' + str(in_list[2]) + ','
    name = name + str(in_list[4]) + ',' + str(in_list[5]) + ','
    name = name + str(in_list[7]) + ',' + str(in_list[8])
    return name

def save_to_index (filename, in_list):
    name = os.path.join(direct, 'index' + '.pickle')
    value = [filename,in_list]
    try:
        pickle_in = open(name, 'rb')
        index = pickle.load(pickle_in)
        print("Retrieving index: {}".format(index))
        is_in = False
        for item in index:
            if item == value:
                is_in = True
        if is_in == False:
            print ("creating index entry...")
            index.append(value)
        else:
            print("Search already in index.")
    except:
        index = [value]
        print ("Index doesn't exist yet, creating...")
    pickle_out = open(name, 'wb')
    pickle.dump(index,pickle_out)

def save_data (data,data_filename):
    name = os.path.join(direct, data_filename + '.pickle')
    print (data)
    pickle_out = open(name,'wb')
    pickle.dump(data,pickle_out)
    pickle_out.close()

def load_data(data_filename):
    name = os.path.join(direct, data_filename + '.pickle')
    pickle_in = open(name, 'rb')
    data = pickle.load(pickle_in)
    pickle_in.close()
    return data

def load_specific_data(data_filename):
    pickle_in = open(data_filename, 'rb')
    data = pickle.load(pickle_in)
    pickle_in.close()
    return data

def get_data_file_name (filename, progress,city):
    file_name = filename + ',' + str(progress[0]) + ',' + str(
        progress[1]) + ',' + str(progress[2]) + ',' + city
    return file_name

def save_progress(filename, progress):
    name = os.path.join(direct, filename + ',prog.pickle')
    pickle_out = open(name, 'wb')
    pickle.dump(progress, pickle_out)
    pickle_out.close()

def check_progress (filename):
    try:
        name = os.path.join(direct, filename + ',prog.pickle')
        pickle_in = open(name,'rb')
        progress = pickle.load(pickle_in)
        return progress
    except:
        return [0,0,0]

def get_abs_progress(prog,lista,listb,listc, pages, current_pages,
                     max = False):

    base_c = 1
    base_b = len(listc)
    base_a = base_b * len(listb)
    if max == True:
        return (base_a * len(lista))*pages
    else:
        return (base_c * prog[2] + base_b * prog[1] + base_a * prog[0])*pages + current_pages

def test_abs_progress():
    testOK = True
    list1 = [1,2,3,4,5,6,7]
    list2 = [1,2,3,4,5,6,7,8,9,10]
    list3 = [1,2,3]

    prog = [6,9,2]

    maximum = get_abs_progress(prog,list1,list2,list3, 10,max = True)
    current = get_abs_progress(prog,list1,list2,list3, 10)

    print (maximum)
    print (current)

    if maximum != current:
        testOK = False

    if testOK:
        print ("Ok so far")

    for a in range (0,len(list1)):
        for b in range(0, len(list2)):
            for c in range(0, len(list3)):
                prog1 = [a,b,c]
                current = get_abs_progress(prog1,list1,list2,list3, 10)
                print (current)

#test_abs_progress()

# Below are functions related to constructing the right url & retriving data:

def get_url (type,city,dates,page):
    url_start = 'https://www.airbnb.co.uk/s/'
    url = url_start + city
    url = url + '/homes?refinement_paths%5B%5D=%2Fhomes&allow_override%5B%5D=&'
    type_dict = {'shared' : ['room_types%5B%5D','Shared%20room'],
                 'room' : ['room_types%5B%5D','Private%20room'],
                 'whole_place' : ['room_types%5B%5D','Entire%20home%2Fapt']}
    print (type)
    if type in type_dict.keys():
        url = url + type_dict.get(type)[0] + '=' + type_dict.get(type)[1] + '&'
    url = url + 'checkin=' + dates[0] + '&'
    url = url + 'checkout=' + dates[1] + '&'
    url = url + 's_tag=L6WSGaxj'
    if page == 0:
        return url
    else:
        url = url + '&section_offset=' + str(page)
    return (url)

def test_get_url (date1,date2):
    for type in ['shared','room','whole_place']:
        for city in ['amsterdam', 'calais', 'london']:
            get_url(type,city,[date1,date2], 2)

def get_price (html_seg):
    result = re.findall('£.*?<', str(html_seg))
    cln_result = result[0][1:-1]
    if len(cln_result) <= 3:
        return cln_result

def get_meta (html_seg):
    result = re.findall('meta content=".*?"', str(html_seg))
    output = []
    if len(result) > 2:
        if len(result[0]) > 15 and len(result[2]) > 15:
            name = result[0][14:-1]
            output.append(name)
            link = result[2][14:-1]
            output.append(link)
            return (output)
    else:
        print ("Troublesome result: {}".format(result))
        return None

def get_data (url):
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (" \
            "KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    browser = mechanicalsoup.Browser(user_agent=agent,
                                         soup_config={'features': 'html.parser'})
    data = []
    page = browser.get(url)
    html_text = page.soup
    listings_list = html_text.find_all('div', attrs={'class' : '_1mpo9ida'})
    for listing in listings_list:
        meta = get_meta(listing)
        if meta != None:
            meta.append(get_price(listing))
            data.append(meta)
    return data

def test_get_data (date1,date2):
    for type in ['shared']:
        for city in ['amsterdam','london']:
            url = get_url(type,city,[date1,date2])
            print (get_data(url))

def get_index_entries():
    try:
        name = os.path.join(direct, 'index' + '.pickle')
        pickle_in = open(name, 'rb')
        index = pickle.load(pickle_in)
        return len(index)
    except:
        return 0

def inspect_dir():
    name = os.path.join(direct, 'index' + '.pickle')
    pickle_in = open(name, 'rb')
    index = pickle.load(pickle_in)
    print ("Current searches and progress:")
    for i in range (0,len(index)):
        print ("{}: {}".format(i,index[i]))
    index_entry = int(input ("please enter an index entry: "))
    return index[index_entry]

def get_index():
    name = os.path.join(direct, 'index' + '.pickle')
    pickle_in = open(name, 'rb')
    index = pickle.load(pickle_in)
    return index

# Below are functions for retrieving & processing data:

def make_ittr_room_type (in_list):
    ittr_list = []
    types = ['shared', 'room', 'whole_place']
    ynbool = in_list[:3]
    print ("ynbool: " + str(ynbool))
    for i in range (0,3):
        if ynbool[i] == 'y':
            ittr_list.append(types[i])
    return ittr_list



def ret_data (in_list):

    print ("in list" + str(in_list))
    ittr_room_type = make_ittr_room_type(in_list)
    date_list = [in_list[4],in_list[5]]
    filename = get_file_name(in_list)
    complete_data = []
    print ("Cities: " + str(in_list[3]))
    for a in range(0, len(ittr_room_type)):
        type = ittr_room_type[a]
        for b in range (0, len(in_list[3])):
            city = in_list[3][b]
            for c in range (0, len(date_list)):
                dates = date_list[c]
                prog = [a,b,c]
                try:
                    data_filename = get_data_file_name(filename, prog, city)
                    data = load_data(data_filename)
                    for listing in data:
                        complete_data.append(listing)
                except:
                    print ("{}:{}:{}".format(type,city,dates))
                    print ("No such file.")
    return complete_data

def get_raw_data():
    index = inspect_dir()
    entry = int(input("Select an input entry: "))
    data = ret_data(index,entry)
    print (len(data))
    clean_data = []
    for listing in data:
        if not type(listing[2]) == type(None):
            clean_data.append(listing)
    sorted_list = sorted(clean_data, key = lambda x: int(x[2]))
    print("Listings in sorted list: " + str(len(sorted_list)))
    return clean_data

def get_prices():
    raw_data = get_raw_data()
    nights = 3
    for i in range (0,len(raw_data)):
        stay_cost = int(raw_data[i][2])*nights
        flight_cost = price_dict.get(raw_data[i][4])
        #print (raw_data[i][4] + ":" + str(flight_cost))
        total_cost = flight_cost + stay_cost
        raw_data[i].append(total_cost)
    return raw_data

def get_sorted(raw_data):
    clean_data = []
    for item in raw_data:
        if type(item[-4]) != type(None):
            clean_data.append(item)
    sorted_new = sorted(clean_data,key=lambda  x:int(x[-4]))
    print ("sorted_new: " + str(sorted_new))
    return sorted_new

def test_get_sorted():
    data = ret_data(-1)
    sorted = get_sorted(data)
    print (sorted)

def get_capped(sorted_list,cap):
    capped = []
    for item in sorted_list:
        if item[-1] <= cap:
            capped.append(item)


def get_cats(list_in):
    room = []
    shared = []
    whole_place = []
    other = []
    for item in list_in:
        if item[-2] == 'shared':
            shared.append(item)
        elif item[-2] == 'room':
            room.append(item)
        elif item[-2] == 'whole_place':
            whole_place.append(item)
        else:
            other.append(item)
    return [shared,room,whole_place,other]

def print_all(lists_in):
    print("Whole place listings:")
    for listing in lists_in[2]:
        print (listing)

    print ("----------------------------------------------------------------------")

    print("Room listings:")
    for listing in lists_in[1]:
        print (listing)

    print ("----------------------------------------------------------------------")

    print("Shared listings:")
    for listing in lists_in[0]:
        print (listing)

    print(
        "----------------------------------------------------------------------")

    print("Unrecognised listings:")
    for listing in lists_in[0]:
        print(listing)

try:
    var = 10/0
except:
    print ()