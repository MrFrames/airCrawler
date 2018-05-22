from Full import inputs

print ("yes")


def test_date_in(date1):
    '''

    :param date: str to be tested

    checks that year, month and day can be converted into an int, and that
    the value between them is a hyphen (required for splitting the string

    :return: True or False

    '''
    print(date1)
    try:
        if date1[4] != '-' or date1[7] != '-':
            print(False)
            return False
        test1 = int(date1[:4]) + int(date1[5:7]) + int(date1[8:])
    except:
        print("Date must have the form YYYY-MM-DD")
        return False
    return True

bool1 = test_date_in("12-05-2018")

print ("outcome: " + str(bool1))