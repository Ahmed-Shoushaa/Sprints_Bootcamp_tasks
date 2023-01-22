import csv
from datetime import date
import os #used it to check for file existence in system

today = date.today()                              #getting today date in the format year-month-day
filename = "ContactBook_" + str(today) + ".csv"   #create file name in the desired format
header = ["UserName", "Email", "Phone Numbers", "Address", "Insertion Date"]  #csv file header

#Make sure the user input is in the right format
def input_in_valid_format():
    while True:
        x = input()
        added_line = x.split(",")
        # check if the user inputed four elements and a valid email and a valid phone number
        if len(added_line) == 4 and added_line[1].__contains__("@") and added_line[2].isdigit() == True:
            break
        else:
            print("Your Input is in the wrong format please re enter 4 elemnts seperated with a comme ',' with no spaces "
                  "\n1-UserName(can contain any character)"
                  "\n2-Email(must contain @ symbol)"
                  "\n3-Phone Number(must contain numbers only)"
                  "\n4-Address(can contain any character)\n.........\nTry Again\n.....")
    #adding the Insertion date automatically to the user input
    added_line.append(str(today))
    return added_line

#checkk if there is a contact book created with today's date
def todays_file_exist():
    #Return true or false depends on file existance
    isExist = os.path.exists(filename)
    if isExist == True:
        print(filename)
        print("==========================")
        pass
    else:
        print("There is no Contact Book with today's date")
        #Create the file if it wasn't created
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        print(filename,"is Created")

#show a list of users in the csv file (first column)
def list_of_users_in_csvFile(file):  #Function to list all the users in file
    names = []  #create empty list to add the users names in it
    with open(file, 'r') as ff:
        read = csv.reader(ff)
        next(read)  #skip the header row
        for row in read:
            names.append(row[0])   #add the first element in each row(User Names) to the names list
    return names

#Welcome function to let the user decide what command he wants to do with the app
def welcome():
    print("WELCOME BACK TO YOUR CONTACT BOOK\n=================================")
    print("What do you need to do?\n.......................")
    print("1-Create New Contact\n2-Update Old Contact\n3-Delete a Contact\n4-Backup Contact Book\n5-Show Contact Book")
    cmd = input("Enter Command Number:")  #user command number input
    print("=====================")
    return cmd

#Depending on user command from welcome function the program flow
def cases(cmd_num):
    if cmd_num == "1":
        print("CONTACTS CREATION\n~~~~~~~~~~~~~~~~~")
        create()
    elif cmd_num == "2":
        print("CONTACTS UPDATE\n~~~~~~~~~~~~~~~")
        update()
    elif cmd_num == "3":
        print("DELETING A CONTACT\n~~~~~~~~~~~~~~~~~~")
        delete()
    elif cmd_num == "4":
        print("BACKUP CONTACT BOOK\n~~~~~~~~~~~~~~~~~~~")
        backup(filename,"ahmedadelelsayed")  #had a problem running exe file when importing boto3 at the begining of the main file
    elif cmd_num == "5":
        show()
    else:
        print("You Enterd Wrong Command Number")

#creatin contacts either manually or importing it from a file
def create():
    print("How do you want to add data?\n...........................\n1-Add manually\n2-Add from file")
    #let the user choose manual data entry or importing
    a = input("ENTER COMMAND NUMBER:")
    #Condition 1 for manual data entry
    if a == "1":
        print(".................\nMANUAL DATA ENTRY\n.................")
        print("ENTER YOUR CONTACT IN CSV FORMAT \nUserName,Email,Number,Address(the insertion date will be added automatically)")
        #Take User Input and make sure it's in the right format
        added_line = input_in_valid_format()
        # open file in append mode to add the new line
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(added_line)
        print('CONTACT:', added_line, 'ADDED SUCCESSFULLY')
    #Condition 2 for data entry from a file
    elif a == "2":
        print(".....................\nIMPORT DATA FROM FILE\n.....................")
        file = input("Enter File Name with it's extension:")
        #check whether the user enterd an existing file or not
        try:
            # open the imported file in read mode and the original file in write mode then loop over imported file rows and add to the original one
            data =[]
            with open(file, mode="r",newline='') as old_file:
                reader = csv.reader(old_file)
                for row in reader:
                    data.append(row)
            with open(filename, mode="a", newline='') as new_file:
                writer = csv.writer(new_file)
                for row in data:
                    writer.writerow(row)
                    # If condition to pass input file lines in format and remove others
                    # for data in reader:
                    #     if len(data) == 4 and data[1].__contains__("@") and data[2].isdigit() == True:
                    #         writer.writerow(data)
                    # else:
                    #     pass
            print(file,"IMPORTED SUCCESSFULLY")
        except:
            print(file,"DOESN'T EXISTS")
    else:
        print("You entered wrong command number")
    return filename

def update():
    updatedlist =[]  #empty list to add the updated line to
    index_counter = 0  # used it to detect which row the user we want to update in
    #This function prints user names in the csv file
    users_list = list_of_users_in_csvFile(filename)
    print("CONTACTS:",users_list)
    #This block to make sure the user entered a valid input
    while True:
        username = input("Enter the user you want to update his data from Contacts above:")
        if username in users_list:
            break
        else:
            print(username,"DOESN'T EXISTS ENTER A valid ONE")
    print("Enter your updated data in CSV format\nUserName,Email,Number,Address,(the insertion date will be added automatically)")
    #x = input() + ',' + str(today)  #updated contact in csv format
    updated_row = input_in_valid_format()      #turn it into a list to add to file easily
    #For function to get the updated row index as i
    for i in range (len(users_list)):
        if username == users_list[i]:
            break
    with open(filename, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            #if condition to add the reader rows to a temp file and if the row index is the same as the updated one replace it all
            if index_counter == i:
                updatedlist.append(updated_row)
            else:
                updatedlist.append(row)
            index_counter +=1
        # Adding the temp file to the original file
        with open(filename, "w", newline="") as f:
            Writer = csv.writer(f)
            Writer.writerows(updatedlist)
            print("File has been updated")

def delete():
    updatedlist = []
    #This function prints user names in the csv file
    users_list = list_of_users_in_csvFile(filename)
    print("CONTACTS:", users_list)
    #Main logic for row deleting
    ##Open the file we want to delete from
    with open(filename, newline="") as f:
        reader = csv.reader(f)
        #This block to make sure the user entered a valid input
        while True:
            username = input("Enter the username you want to delete his data from Contacts:")
            if username in users_list:
                break
            else:
                print(username, "DOESN'T EXISTS ENTER A valid ONE")
        ##check for the wanted row and adding other rows to a new file
        for row in reader:
            if username not in row:
                updatedlist.append(row)
        # ADDING THE NEW FILE TO THE OLD FILE BUT WITHOUT THE DELETED ROW
        with open(filename, "w", newline="") as f:
            Writer = csv.writer(f)
            Writer.writerows(updatedlist)
            print(username,"Deleted successfully and File has been updated")

###
###I HAD a PROBLEM IN THIS FUN
###if i add the boto3 module at the begining of the script the .exe file opens and closes immediately
###while running the script from pycharm works fine
def backup(file_name, bucket, object_name=None, folder_name=None):
    from botocore.exceptions import ClientError
    import boto3
    # Upload the file
    try:
        s3_client = boto3.client(service_name='s3', aws_access_key_id="AKIA2J67UWKQ6TGKOK6V",
                                 aws_secret_access_key="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")
        # Upload the file to the s3
        response = s3_client.upload_file(file_name, bucket, file_name)
        print(file_name,"Backed up successfully on S3Bucket:",bucket)
    except ClientError as e:
        print(e)

def show():
    print("SHOWING CONTACTS BOOK\n~~~~~~~~~~~~~~~~~~~~~")
    print(filename,"\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
    with open(filename, "r") as csv_file:
        reader = csv.reader(csv_file)
        for item in reader:
            print(','.join(item))
    print("")


todays_file_exist()
while True:
    cmd_num = welcome()
    cases(cmd_num)
    x= input("DO YOU WANT Another Service?(y,n)")
    if x =="y":
        pass
    else:
        break