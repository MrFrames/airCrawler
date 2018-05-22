import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
from Abs_date_range import*

from Main_functions import *

class inputs(QWidget):

    def __init__(self):
        super().__init__()

        self.city_list = []
        self.errors = []

        self.whole = False
        self.room = False
        self.shared = False

        self.depart_date = ''
        self.return_date = ''

        self.statusBar = QAction

        self.initUI()

    def initUI(self):

        self.ittr_room_type = []
        self.pages = 1
        self.in_list = []

        city = QLabel('City:')
        self.city_edit = QLineEdit()
        self.city_submit = QPushButton('Add to list')

        self.whole_in = QCheckBox('Whole place')
        self.room_in = QCheckBox('Room')
        self.shared_in = QCheckBox('shared')

        self.city_display = QTableWidget()
        self.city_display.horizontalHeader().hide()
        self.city_display.verticalHeader().hide()
        self.city_display.setColumnCount(1)
        self.city_display.setRowCount(0)

        self.subButton = QPushButton('Start crawling')

        self.depart_date = QLabel('Depart date:')
        self.return_date = QLabel('Return date:')
        self.pages_label = QLabel ('Pages per search:')

        self.date_out = QLineEdit()
        self.date_in = QLineEdit()
        self.pages_in = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(city, 1, 0)
        grid.addWidget(self.city_edit, 1, 1)
        grid.addWidget(self.city_submit,1,2)

        grid.addWidget(self.whole_in, 2, 0, 1, 2)
        grid.addWidget(self.room_in, 3, 0, 1, 2)
        grid.addWidget(self.shared_in, 4, 0, 1, 2)

        grid.addWidget(self.city_display, 2,2,5,1)

        grid.addWidget(self.depart_date, 5, 0)
        grid.addWidget(self.return_date, 6, 0)
        grid.addWidget(self.pages_label, 7, 0)

        grid.addWidget(self.date_out, 5, 1)
        grid.addWidget(self.date_in, 6, 1)
        grid.addWidget(self.pages_in, 7 ,1)

        grid.addWidget(self.subButton, 7,2)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)

        self.city_submit.clicked.connect(self.on_add_city)

        self.whole_in.stateChanged.connect(self.set_whole)
        self.room_in.stateChanged.connect(self.set_room)
        self.shared_in.stateChanged.connect(self.set_shared)

        self.subButton.clicked.connect(self.on_click)

        self.show()

    def on_add_city(self):
        city_name = (self.city_edit.text().lower())
        if not city_name in self.city_list:
            self.city_list.append(city_name)
            for i in range (0,len(self.city_list)):
                self.city_display.setRowCount(i+1)
                city_item = QTableWidgetItem(self.city_list[i])
                self.city_display.setItem(i,0,city_item)
        else:
            print ("That city is already in the list!")

    def set_whole(self,state):

        if state == 2:
            self.whole = True
        else:
            self.whole = False
        print(self.whole)

    def set_room(self,state):
        if state == 2:
            self.room = True
        else:
            self.room = False
        print(self.room)

    def set_shared(self,state):
        if state == 2:
            self.shared = True
        else:
            self.shared = False
        print(self.shared)

    def on_click (self):
        self.date_out_str = self.date_out.text()
        self.date_in_str = self.date_in.text()
        self.pages = int(self.pages_in.text())

    def test_inputs(self):
        if self.test_date_in(self.date_in_str) == False:
            return False
        if self.test_date_in(self.date_out_str) == False:
            return False
        return True

    def test_date_in(self, date1):
        '''

        :param date: str to be tested

        checks that year, month and day can be converted into an int, and that
        the value between them is a hyphen (required for splitting the string

        :return: True or False

        '''
        print (date1)
        try:
            if date1[4] != '-' or date1[7] != '-':
                print (False)
                return False
            test1 = int(date1[:4]) + int(date1[5:7]) + int(date1[8:])
        except:
            return False
        return True

    def add_if (self, list_name, value, bool):
        if bool == True:
            list_name.append(value)

    def make_ittr_room_type(self):
        self.add_if(self.ittr_room_type, 'shared', self.shared)
        self.add_if(self.ittr_room_type, 'room', self.room)
        self.add_if(self.ittr_room_type, 'whole_place', self.whole)
        print ("Ittr room: " + str(self.ittr_room_type))

    def make_in_list(self):
        in_list = []
        for item in [self.shared,self.room,self.whole]:
            temp = ''
            if item == True:
                temp = 'y'
            else:
                temp = 'n'
            in_list.append(temp)
        in_list.append(self.city_list)
        in_list.append(self.date_out_str)
        in_list.append(self.date_in_str)
        in_list = in_list + [1,1]
        in_list.append(self.pages)
        self.in_list = in_list

class data_Show(QTableWidget):

    def __init__(self,r = 100,c = 7):
        super().__init__(r, c)
        self.data = []
        self.filtered_data = []

        self.initUI()
        self.searchNo = 0
        self.in_list = []
        self.days = 0

        self.whole = False
        self.room = False
        self.shared = False
        self.cap = False

        self.cap_amount = 0

        self.bool_list = ['whole', 'room', 'shared', 'cap']
        self.bool_list = [self.whole, self.room, self.shared,self.cap]
        self.filter_func_map = {}

    def initUI(self):
        self.col_headers = ['City', 'type', 'Total price', 'Stay price',
                            'Per night', 'Flight price', 'Temperature']
        self.setHorizontalHeaderLabels(self.col_headers)

        self.show()

    def get_data(self):
        print ("getting data")
        index = get_index()
        self.in_list = index[self.searchNo][1]
        self.get_sorted_data()
        self.get_days()
        self.get_full_stay_prices()
        for i in range (0,10):
            print (self.filtered_data[i])

    def filter_cap(self):
        if self.cap == True:
            capped = []
            for item in self.filtered_data:
                if item[-1] <= self.cap_amount:
                    capped.append(item)
            self.filtered_data = capped

    def filter_type(self):
        bool_list = [self.whole, self.shared, self.room]
        ref_list  = ['whole_place','shared','room']
        emp_list = []
        for i in range (0,3):
            if bool_list[i] == True:
                emp_list.append(ref_list[i])
        if emp_list == []:
            emp_list = ref_list
        type_list = []
        for item in self.filtered_data:
            if item[-2] in emp_list:
                type_list.append(item)
        self.filtered_data = list(type_list)

    def get_full_stay_prices(self):
        temp_data = []
        for item in self.data:
            temp_item = list(item)
            price = int(item[-4])
            temp_item.append(price * self.days)
            temp_data.append(temp_item)
        self.filtered_data = temp_data

    def populate_table(self):

        print ("index: " + str(index))
        index_map = {'City': -3 ,
                     'type': -2,
                     'Total price': 'N/A',
                     'Stay price': -1,
                     'Per night' : -5,
                     'Flight price': 'N/A',
                     'Temperature': 'N/A'}

        #test cell entry:
        #self.add_entry(1,1,'hello')

        for row in range (0,100):
            entry = self.filtered_data[row]
            print (entry[-1])
            print ("entry: " + str(entry))
            for col in range (0,7):
                try:
                    entry_index = int(index_map.get(self.col_headers[col]))
                    data_in = str(entry[entry_index])
                except:
                    data_in = index_map.get(self.col_headers[col])
                self.add_entry(row, col, data_in)
            self.setCurrentCell(1,1)

    def get_days(self):
        date1 = abs2k_date(self.in_list[4])
        date2 = abs2k_date(self.in_list[5])
        self.days = date2 - date1

    def add_entry(self,row,col,string):
        cell_entry = QTableWidgetItem(string)
        self.setCurrentCell(row,col)
        self.setItem(row,col,cell_entry)


    def get_sorted_data(self):
        raw_data = ret_data(self.in_list)
        self.data = get_sorted(raw_data)

class index(QTableWidget):

    def __init__(self,r = get_index_entries(),c = 10):
        super().__init__(r, c)

        self.initUI()

    def initUI(self):
        self.col_headers = ['Date out', 'Date in', 'Whole_place', 'Room',
                         'Shared', 'city1', 'city2', 'city3', 'city4', 'city5']
        self.setHorizontalHeaderLabels(self.col_headers)

        self.show()

    def populate_table(self):
        index = get_index()
        print ("index: " + str(index))
        index_map = {'Date out': 4,
                    'Date in': 5,
                    'Whole_place': 0,
                    'Room': 1,
                    'Shared': 2,
                    'city1': 1,
                    'city2': 2,
                    'city3': 3,
                    'city4': 4,
                    'city5': 5}

        #test cell entry:
        #self.add_entry(1,1,'hello')


        for row in range (0,len(index)):
            entry = index[row][1]
            print ("entry: " + str(entry))
            city_list = entry[3]
            for col in range (0,5):
                entry_index = index_map.get(self.col_headers[col])
                data_in = entry[entry_index]
                self.add_entry(row,col,data_in)
            for col in range (5,10):
                try:
                    city = city_list[col-5]
                    self.add_entry(row,col,city)
                except:
                    nocity = 1

    def add_entry(self,row,col,string):
        cell_entry = QTableWidgetItem(string)
        self.setCurrentCell(row,col)
        self.setItem(row,col,cell_entry)

class crawling(QWidget):
    def __init__(self):
        super().__init__()
        self.progress = 0

        self.initUI()

    def initUI(self):
        self.only = QPushButton('Crawling')

        self.pbar = QProgressBar(self)
        self.progress_label = QLabel('Starting crawl')
        self.current_url = QLabel ('URL.')
        self.url_text = 'Click here to open current search URL.'
        self.current_url.setOpenExternalLinks(True)

        grid = QGridLayout()
        grid.setSpacing(10)
        self.setGeometry(300, 300, 300, 300)

        grid.addWidget(self.pbar, 0, 0)
        grid.addWidget(self.progress_label, 1, 0)
        grid.addWidget(self.current_url, 2, 0)

        self.setLayout(grid)

        self.show()

    def start_search(self):
        print("start_search")

class data_view(QWidget):
    def __init__(self):
        super().__init__()
        self.data_index = 0
        self.initUI()

    def initUI(self):

        # Init data_show class, which creates a table
        self.data = data_Show()

        print("init data_show ok")

        # init check boxes to fiter data
        self.whole_in = QCheckBox('Whole place')
        self.room_in = QCheckBox('Room')
        self.shared_in = QCheckBox('shared')

        # init check boxes which can't be used yet
        self.flights = QCheckBox ('Flight prices')
        self.temp = QCheckBox ('Temperature')

        self.cap = QLabel ('Price cap (£):')
        self.cap_in = QLineEdit()
        self.filter_go = QPushButton('Filter')

        #sets layout to grid format
        grid = QGridLayout()
        grid.setSpacing(10)

        #adds widgerts to grid layout
        grid.addWidget(self.whole_in, 1, 0)
        grid.addWidget(self.room_in, 2, 0)
        grid.addWidget(self.shared_in, 3, 0)

        grid.addWidget(self.flights, 1, 1)
        grid.addWidget(self.temp, 2,1)
        grid.addWidget(self.cap, 1,2)
        grid.addWidget(self.cap_in, 1, 3)

        grid.addWidget(self.filter_go, 2,2,2,3)

        grid.addWidget(self.data, 4,0,5,4)

        self.setLayout(grid)

        self.show()

    def get_data(self):
        print (self.data_index)

class main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.progress = 0
        self.max_progress = 0
        self.current_page = 0

        self.setUI()

    def setUI(self):

        # init toolbar
        self.toolbar = self.addToolBar('exit')

        # init Qobjects to go into toolbar:
        new_search = QAction('New search', self)
        search_index = QAction('Search index', self)
        last_search = QAction('Last search', self)

        # add Qactions to toolbar
        self.toolbar.addAction(new_search)
        self.toolbar.addAction(search_index)
        self.toolbar.addAction(last_search)

        # Connect toolbar actions to functions:
        new_search.triggered.connect(self.new_search1)
        search_index.triggered.connect(self.search_index)
        last_search.triggered.connect(self.prev_search)

        self.layout = QStackedWidget()

        # Creates an instance of each widget:
        self.inputs_box = inputs()
        self.crawling_box = crawling()
        self.index_box = index()
        self.data_box = data_view()

        # Adds all widgets to layout & saves their indexes to variables:

        self.in_dex = self.layout.addWidget(self.inputs_box)
        self.crawl_dex = self.layout.addWidget(self.crawling_box)
        self.index_dex = self.layout.addWidget(self.index_box)
        self.data_dex = self.layout.addWidget(self.data_box)

        # self.layout.setCurrentIndex(self.in_dex)
        self.setCentralWidget(self.layout)

        # Connect the output of the search widget to a function in this class:
        self.inputs_box.subButton.clicked.connect(self.on_crawl)

        # Runs 'on_index_click" when user double clicks on an enty in the
        # index box, which switches layout to the data_view_box
        self.index_box.cellDoubleClicked.connect(self.on_index_click)

        self.show()

    def on_crawl(self):
        time.sleep(0.5)
        inputs_ok = self.inputs_box.test_inputs()
        print("inputs ok? " + str(inputs_ok))
        if inputs_ok == True:
            self.layout.setCurrentIndex(self.crawl_dex)
            self.inputs_box.make_in_list()
            self.inputs_box.make_ittr_room_type()
            ittr_room_type = self.inputs_box.ittr_room_type
            in_list = self.inputs_box.in_list
            dates = [self.inputs_box.date_out_str,self.inputs_box.date_out_str]
            self.init_progress(in_list,ittr_room_type)
            print ("max progress: ".format(self.max_progress))
            self.main_search(in_list,ittr_room_type,dates)
        self.prev_search()

    def main_search(self,in_list,ittr_room_type,dates):
        print("Innitialising...")
        filename = get_file_name(in_list)
        save_to_index(filename, in_list)
        innit_progress = check_progress(filename)
        for a in range(int(innit_progress[0]), len(ittr_room_type)):
            type = ittr_room_type[a]
            for b in range(int(innit_progress[1]), len(in_list[3])):
                time.sleep(0.1)
                city = in_list[3][b]
                progress = [a, b, 0]
                url = get_url(type, city, dates, 0)
                data = get_data(url)

                data_list = []
                data_filename = get_data_file_name(filename,
                                                   progress, city)
                self.current_page = 0
                self.update_progress(progress, in_list, ittr_room_type, url)
                for item in data:
                    data_list.append(item + [1] + [city] + [type])

                for page in range(2, in_list[8] + 1):
                    QApplication.processEvents()
                    self.current_page = page-1
                    url = get_url(type, city, dates, page)
                    self.update_progress(progress, in_list, ittr_room_type,
                                         url)
                    data = get_data(url)
                    for item in data:
                        data_list.append(
                            item + [page] + [city] + [type])

                save_data(data_list, data_filename)
                save_progress(filename, progress)



        #for i in range (0,100):
        #    time.sleep(0.1)
        #    self.progress += 1
        #    self.pbar.setValue(self.progress)

    def new_search1(self):
        if self.layout.currentIndex() != self.in_dex:
            self.layout.setCurrentIndex(self.in_dex)
            # Resets the city list, in_list and clears the city table:
            self.inputs_box.city_list = []
            self.inputs_box.city_display.setRowCount(0)
            self.inputs_box.in_list = []
            self.inputs_box.ittr_room_type = []

    def search_index(self):
        if self.layout.currentIndex() != self.index_dex:
            self.layout.setCurrentIndex(self.index_dex)
        self.index_box.setRowCount(get_index_entries())
        self.index_box.populate_table()

    def prev_search(self):
        self.data_box.data.searchNo = -1
        self.data_box.data.get_data()
        self.layout.setCurrentIndex(self.data_dex)
        self.data_box.data.populate_table()

    def init_progress (self, in_list,ittr_room_types):
        print ("init progress")
        self.max_progress = get_abs_progress([1,1,1],
                         ittr_room_types,
                         in_list[3],
                         [1],
                         self.inputs_box.pages,
                         self.current_page,
                         True)
        print ("Max progress: " + str(self.max_progress))

    def update_progress(self,progress,in_list,ittr_room_types,url):
        self.abs_progress = get_abs_progress(progress,
                                             ittr_room_types,
                                             in_list[3],
                                             [1],
                                             self.inputs_box.pages,
                                             self.current_page)
        print("Abs progress: " + str(self.abs_progress))
        string = "Opening page " + str(self.abs_progress) + " of " + str(
            self.max_progress) + "."
        self.crawling_box.progress_label.setText(string)
        #link_str = r"<a href=\"" + url + r">'" + self.crawling_box.url_text
        #  + r"</a>"
        #self.crawling_box.current_url.setText()

        percent = int((float(self.abs_progress*100))/float(self.max_progress))
        self.crawling_box.pbar.setValue(percent)
        print ("percent: " + str(percent))

    def on_index_click(self,state1,state2):
        self.data_box.data.searchNo = state1
        self.data_box.data.get_data()
        self.layout.setCurrentIndex(self.data_dex)
        self.data_box.data.populate_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    new_instance = main()
    sys.exit(app.exec_())
