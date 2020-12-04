import os, datetime, PySimpleGUI as sg

''' --------------------------- delete old temp files ----------------- '''
os.chdir("C:/Temp/")
try:
    os.remove("file_1.tsv")
except:
    pass
try:
    os.remove("file_1_oneheader.tsv")
except:
    pass


''' ----------------- start with variables -------------------------- '''
s_date = 'test'
e_date = 'test'
layout1 = [[sg.Text('Test to get dates')],
            [sg.InputText('2020-05-20',key = '-start_date-')],
            [sg.CalendarButton('choose start date', target = '-start_date-', key='sdate')],
            [sg.InputText('2020-06-01', key='-end_date-')],
            [sg.CalendarButton('choose end date', target = '-end_date-', key='edate')],
            [sg.Button("store dates", key='Store_B'), sg.Button("compile", key='-compile-')]]

window1 = sg.Window('test to get dates', layout1)

while True:  # Event Loop
    event, values = window1.read()
    if event in (None, 'Exit'):
        break
    if event == 'Store_B':
        StartDate, EndDate = values['-start_date-'], values['-end_date-']
        s_tuple = (StartDate[:4], StartDate[5:7], StartDate[8:10] )
        e_tuple = (EndDate[:4], EndDate[5:7], EndDate[8:10])
        # tuples are in yyyy[0] mm[1] dd[1] format
        print ('Start of date range:', s_tuple[0], s_tuple[1], s_tuple[2])
        print ('End of date range:', e_tuple[0], e_tuple[1], e_tuple[2])
    if event == '-compile-':
        break

window1.close()

s_date = datetime.date(int(s_tuple[0]), int(s_tuple[1]), int(s_tuple[2]))
print(s_date)
og_s_date = s_date
e_date = datetime.date(int(e_tuple[0]), int(e_tuple[1]), int(e_tuple[2]))
print(e_date)
delt = e_date - s_date
delta = delt.days
cur_date = str(s_date)
end_date = str(e_date)

today = str(datetime.date.today())
t_tuple = today.split("-")

''' ----------- loading bar ------------ '''

sg.popup("                     ", 'file is compiling', 'window will close when file is compiled', text_color = 'black', background_color = '#ebf5a2', auto_close = True, non_blocking=True,)

''' -------------------set up files------------------------ '''
os.chdir("C:/Temp/")
f = open("file_1.tsv", "a") #create temp file in temp folder, not sure if this is needed
f.close()

''' --------------- compile the data --------- '''

directory = "this_is_the_file_directory"
dir_list = os.listdir(directory)

for x in dir_list:
    new_dir_2 = directory + x +"/"
    if x[0] == '3':              #make sure folder is a test station folder
        os.chdir(new_dir_2 + "extra_layer_in_directory/")
        while True:
            if  s_date > e_date:
                s_date = og_s_date
                break               #the issue is with this break is s_date is counted up and needs to be reset back to the orginal s_date to go through the loop again '''
            cur_date=str(s_date)
            with os.scandir() as listofentries:     #get all files from directory
                for entry in listofentries:
                    if entry.is_file():             #make sure entry is a file
                        file_loc = str(entry)       #convert file to string, not sure if this is needed
                        file = file_loc

                        file_ext = file[-6:]        #get file extension
                        file = file.strip(file_ext)     #remove file extension
                        file_front = file[:11]      #get file front
                        file = file.strip(file_front)   #file now in date format
                        file_length = len(file)
                        if file_length < 8 or  file_length > 10:    #skip any files that do not have the date format
                            pass
                        file_list = file.split("-")
                        file_year = file_list[0]
                        file_month_raw = file_list[1]
                        file_day_raw = file_list[2]
                        if len(file_month_raw) == 1:
                            file_month = "0" + file_month_raw
                        else:
                            file_month = file_month_raw
                            #print (file_month)
                        if len(file_day_raw) == 1:
                            file_day = "0" + file_day_raw
                        else:
                            file_day = file_day_raw

                        year = str(cur_date)[:4]
                        month = str(cur_date)[5:7]
                        day = str(cur_date)[8:]

                        if file_year == year and file_month == month and file_day == day: #filter based on matching year, month and day
                            file_loc = file_year + "-" + file_month_raw + "-" + file_day_raw + ".tsv"
                            print("file location is  " + file_loc)

                            with open(file_loc) as fp:
                                df=fp.read()                #store file contents as df so it can be written later

                            #print (file_loc)
                            os.chdir("C:/Temp/")
                            f=open("file_1.tsv","a")    #open temp file to append for each loop
                            f.write(df)                         #append previously stored file contents to the temp file
                            f.close()                           #close temp file
                            os.chdir(new_dir_2 + "extra_layer_in_directory/")   #change back to original directory, this may not be needed

            #print (s_date)
            s_date += datetime.timedelta(days=1)

            f.close()

''' ------------------------------------------------------------------------------------------
    this section is to remove all header lines from the temp file so it is set up for graphing '''

os.chdir("C:/Temp/")
f = open("file_1.tsv", "r") #create temp file in temp folder, not sure if this is needed
f2 = open("file_1_oneheader.tsv","a")

header_line = f.readline()
num_columns = len(header_line.split('\t'))
f2.write(header_line)
print = len(header_line)

for x in f:
    line = x
    #print(line)
    line_start = line[:6]       # only look at the first 6 characters of the line
    #print(line_start)
    if line_start == "Serial" :  #ignore lines that are a header row and any lines that do not have the same number of columns as the header
        pass
    else:

        f2.write(line)
        #print(line)
        #f2.close()


f.close()
f2.close()

sg.popup("                   ", 'file is done compiling', 'check temp folder for file')
