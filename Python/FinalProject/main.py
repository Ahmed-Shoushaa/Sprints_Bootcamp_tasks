import csv
from datetime import date
import os
from botocore.exceptions import ClientError
import boto3

today = date.today()
filename = "ContactBook_" + str(today) + ".csv"
header = ["username", "email", "phone numbers", "address", "insertion date"]

def list_of_users_in_csvFile(file):  #Function to list all the users in file
    names = []
    with open(file, 'r') as ff:
        read = csv.reader(ff)
        for row in read:
            names.append(row[0])
    return names

def welcome():
# This is a welcome function to let the user decide what he wants to do in the app
    print("WELCOME BACK TO YOUR CONTACT BOOK\n=================================")
    print("What do you need to do?\n.......................")
    print("1-Create New Contact\n2-Update Old Contact\n3-Delete a Contact\n4-Backup Contact Book\n5-Show Contact Book")
    cmd = input("Enter Command Number:")
    print("=====================")
    return cmd

def cases(cmd_num):
# Take welcome function output and feed it to the cases function to decide the program flow
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
        backup(filename,"ahmedadelelsayed")
    elif cmd_num == "5":
        show()
    else:
        print("Please enter number between 1 and 5")

def create():
    print("How do you want to add data?\n...........................\n1-Add manually\n2-Add from file")
    a = input("ENTER COMMAND NUMBER:")
    #Condition 1 for manual data entry
    if a == "1":
        print(".................\nMANUAL DATA ENTRY\n.................")
        print("ENTER YOUR CONTACT IN CSV FORMAT \nUserName,Email,Number,Address(the insertion date will be added automatically)")
        #Take User Input
        x = input() + ',' + str(today)    # x will be at csv format
        added_line = x.split(",")         # turn x elements into a list to add easily to the file
        # open file in append mode to add the new line
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(added_line)
        print('CONTACT:'+ x ,'ADDED SUCCESSFULLY')
    #Condition 2 for data entry from a file
    elif a == "2":
        print(".....................\nIMPORT DATA FROM FILE\n.....................")
        file = input("Enter File Name with it's extension:")
        #open the imported file in read mode and the original file in write mode then loop over imported file rows and add to the original one
        with open(file, mode="r") as old_file:
            reader = csv.reader(old_file)
            with open(filename, mode="a", newline='') as new_file:
                writer = csv.writer(new_file)
                for data in reader:
                    writer.writerow(data)
        print(file,"IMPORTED SUCCESSFULLY")
    else:
        print("You entered wrong command number")
    return filename

def update():
    updatedlist =[]
    index_counter = 0
    #This function prints user names in the csv file
    users_list = list_of_users_in_csvFile(filename)
    print("CONTACTS:",users_list)
    #take input from user name and updated data from user
    username = input("Enter the user you want to update his data from user list above:")
    print("Enter your updated data in CSV format\nUserName,Email,Number,Address,(the insertion date will be added automatically)")
    x = input() + ',' + str(today)  #updated contact in csv format
    updated_row = x.split(",")      #turn it into a list to add to file easily
    #For function to get the upsated row index as i
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
    print("CONTACTS:",list_of_users_in_csvFile(filename))
    #Main logic for row deleting
    ##Open the file we want to delete from
    with open(filename, newline="") as f:
        reader = csv.reader(f)
        username = input("Enter the username from the list above to remove from file:")
        ##check for the wanted row and adding other rows to a new file
        for row in reader:
            if username not in row:
                updatedlist.append(row)
        # ADDING THE NEW FILE TO THE OLD FILE BUT WITHOUT THE DELETED ROW
        with open(filename, "w", newline="") as f:
            Writer = csv.writer(f)
            Writer.writerows(updatedlist)
            print("File has been updated")

def backup(file_name, bucket, object_name=None, folder_name=None):
    # Upload the file
    try:
        s3_client = boto3.client(service_name='s3', aws_access_key_id="AKIA2J67UWKQ6TGKOK6V",
                                 aws_secret_access_key="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")
        # Upload the file to the s3
        response = s3_client.upload_file(file_name, bucket, file_name)
        print("Backup succeeded")
    except ClientError as e:
        print(e)

def show():
    with open(filename, mode="r") as csv_file:
        reader = csv.reader(csv_file)
        for item in reader:
            print(','.join(item))


tt= input('ggg')
cmd_num = welcome()
cases(cmd_num)
input('Press ENTER to exit')