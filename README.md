# Test_data_compiler

Background:
There is a need for manufacturing to monitor product testing data for varying date ranges. Product testing is completed over several duplicate test systems. Each test system outputs a daily .tsv file which is stored through in different directories associated with the unique number of the test system. Daily .tsv files naming is not a standard YYYY-MM-DD format. For example 2020-01-01 would be titled as 2020-1-1.tsv.

Problem:
It is very time consuming to navigate through the various directories and complie the files into a single file for analysis. Additionally there is room for human error in pulling the correct data files. Files that are accidentally omitted can skew the overall data. 

Solution:
Create a program with a user interface to allow user to choose a date range and then compile that data into a single file. 
