'''
Script:  Rainbow Table Generator
Date:    April 2022
Version: 1.0
Purpose: Given criteria set by user input, create a dynamic rainbow table of all passwords 
         along with the md5 hash of each password. Store them in a Python dictionary, serialize 
         the resulting table, and store it in the specified file. Finally, print the first five 
         and last five hashes and their corresponding passwords in a prettytable.
'''

''' IMPORT STANDARD LIBRARIES '''
import time       # Time Conversion Methods
import hashlib    # Hash Messages
import itertools  # Generate a product
import pickle     # Serialize python objects

''' IMPORT 3RD PARTY LIBRARIES '''
from prettytable import PrettyTable  # pip install prettytable
                                     # display data in table layout
                                     
import pyfiglet                      # pip install pyfiglet
                                     # Print ASCII Art
''' PSEUDO CONSTANTS '''
asciiBanner = pyfiglet.figlet_format("RAINBOW TABLE GENERATOR", font="straight") # Setup for Banner Art

tbl = PrettyTable(['MD5 HASH VALUE', 'PASSWORD']) # The Sample Prettytable Setup

''' MAIN ENTRY POINT '''

if __name__ == '__main__':
    
    print(asciiBanner)
    
    minValue = input("Enter Minimum Password Length: ")               # allow users to input the minimum password length
    maxValue = input("Enter Maximum Password Length: ")               # allow users to input the maximum password length
    criteria = input("Enter Password Criteria (ex: abc123!): ")       # allow users to input the specific password criteria
    fileName = input("Enter Serialized Filename: ")                   # allow users to enter the specific database filename
    
    minValueInt = int(minValue)    # convert the minimum length to integer
    maxValueInt = int(maxValue)    # convert the maximum length to integer
    
    actualMinValue = minValueInt
    actualMaxValue = (maxValueInt + 1)  # add "1" to the maximum length for itertools processing
    actualFileName = (fileName+ '.db')  # add the ".db" file extension to the specified filename
    
    print("\nCreating Rainbow Table: ")
    
    rainbowTable = {}                     # starting a rainbowTable with no entries
    
    startTime = time.time()               # record the start time of creating the rainbow table
    
    for variations in range(actualMinValue,actualMaxValue):
        for pwTuple in itertools.product(criteria, repeat=variations):
            pw = ""
            md5Hash = hashlib.md5()            # create an md5 Hash Object
            for eachChr in pwTuple:
                pw = pw+"".join(eachChr)       # extract the next generated password
            pwForHash = bytes(pw, 'ascii')     # convert to bytes
            md5Hash.update(pwForHash)          # update with new password
            md5Digest = md5Hash.hexdigest()    # obtain the digest
            rainbowTable[md5Digest] = pw       # key = digest, value = associated password
            
    endTime = time.time()                 # record the end time of creating the rainbow table
    elapsedTime = endTime - startTime     # record the time taken to create the rainbow table
    rainbowSize = len(rainbowTable)       # record the raibow table size
    
    print("Rainbow Table has been Successfully Created")
    print("Elapsed Time: ", elapsedTime, "seconds")
    print("Rainbow Size: ", '{:,}'.format(rainbowSize), "bytes\n")
    
    pickleFileWrite = open(actualFileName, 'wb')               # open the destination File (write binary)
    
    print("Serializing Rainbow Table:")
    pickle.dump(rainbowTable, pickleFileWrite)               # serialize the list and DUMP to file     
    pickleFileWrite.close() 
    print(actualFileName, "has been successfully created\n")
    
    firstFive = list(rainbowTable.items())[:5]
    lastfive  = list(rainbowTable.items())[-5:]              # creating a list of the first 5 & last 5 hashes/passwords
    sampleList = firstFive + lastfive
    
    for eachItem in sampleList:
        md5Value  = eachItem[0]
        pswdValue = eachItem[1]                              # adding the first 5 & last 5 hashes/passwords to a prettytable
        tbl.add_row( [ md5Value, pswdValue])
    
    print("Sample Rainbow Table:")
    tbl.align = "l"                     # format the table - left align
    resultString = tbl.get_string()     # store formatted values in a sorted variable resultString
    print(resultString)