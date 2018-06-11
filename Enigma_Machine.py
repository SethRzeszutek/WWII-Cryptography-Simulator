'''
 Name of file:EncryptDecrypt
 Purpose:Takes a string, rotor, and daily rotor schedule to convert a string, then decrypts it.

 Author: Seth Rzeszutek

 Date Created:March 29th, 2017

'''

import string


class Enigma:


    def __init__(self):
        '''
        Purpose: Calls textedit, organizes and cleans information from User Text File to certain variables, then calls encrypt
        :param:
        :return NONE:

        '''
        textlist = self.textinput()                  #grabs text from file
        self.missingCheck(textlist)                  #Checks for missing data
        day = textlist[0]                       #grabs day from file
        reflectorRequest = textlist[1]          #grabs reflector from file
        rotororder = textlist[2]                #grabs rotor order from file
        ring = textlist[3]                      #grabs ring from file
        ground = textlist[4]                    #grabs ground from file
        plugsIn = textlist[5]
        TR = textlist[6]
        incomingtext = textlist[7]
        self.dayCheck(day)
        reflectorRequest = self.cleantext(reflectorRequest)
        ring = self.cleantext(ring)
        ground = self.cleantext(ground)
        TR = self.cleantext(TR)                      #Cleans TR
        TR = TR.upper()                              #Converts TR to uppercase
        self.checkPlugs(plugsIn)                     #Checks if plugs are in correct format
        self.checkReflector(reflectorRequest)        #Checks for correct Reflector
        message = self.cleantext(incomingtext)       #cleans incoming text
        rotorWheels = self.cleanrotor(rotororder)    #cleans rotororder
        numberOfRotors = self.roterCounter(rotorWheels)      #number of rotors
        self.numberOfRotorsCheck(numberOfRotors)     #checks the number of rotors
        self.wheelCheck(rotorWheels)                 #checks the current rotors selected
        message = self.lengthCheck(message)          #calls length checker to test if it is greater than 250 characters
        plugsInList = plugsIn.split(' ')
        alpha = "." + string.ascii_uppercase
        plugs = self.plugboard(plugsInList, alpha)
        #ringSettingRotor = self.ringSettings(ring, rotorWheels)

        print("Day->", day,"    Plugs->",plugsInList,"    Message->", message)
        print("Number of Rotors->",numberOfRotors, "    Rotor Wheels->",rotorWheels,"    Reflector Request->",reflectorRequest,"    Transmit Or Recieve->",TR)

        print("-----------------------------")
        print("Input message:")
        print(message)
        print("-----------------------------")
        print("Input message grouped:")
        n = 4
        print(' '. join([message[i:i+n] for i in range(0, len(message), n)]))
        if "ERROR" in self.encrypt(plugs, message, numberOfRotors, rotorWheels, reflectorRequest, TR, ring):
            print("-----------------------------")
            print ("Error #111 with Inputs:")
            print("Plugs->",plugs,"    Message->", message,"    NumberofRotors->",numberOfRotors,"    rotorWheels->",rotorWheels,"    reflectorRequest->",reflectorRequest,"    TR->",TR)
            print("Check datatypes and/or amount of character spaces.")
        else:
            print("-----------------------------")


        ###########################################-------CHECKS AND ERRORS-------###########################################


    def lengthCheck(self, message):
        '''
        Purpose: Checks the length of the message
        :param message: The message to be checked
        :return: NONE
        '''
        if len(message) > 250:                  #Limits string to 250 characters
            message = (message[:250] + '') if len(message) > 250 else message
            print("Error #999")
            print("Your file has been limited to 250 characters. Error #100")
            print(message)
        return message

    def dayCheck(self, day):
        '''

        :param day:
        :return:
        '''
        if day.isdigit():
            day=day
        else:
            print("ERROR #207")
            print("Day entered is not an integer.")
            quit()


    def missingCheck(self,textlist):
        '''
        Purpose: Checks if Data is missing
        :param textlist: list to be checked
        :return: NONE
        '''
        errordisplay = ['Day',"Reflector", "Rotor List", "Ground", "Plugs","Receiving or Transmiting","Message to be decoded or encrypted"]
        n = 0
        #errordisplay.insert(0,0)
        for i in range(len(errordisplay)):
            if textlist[i] == '':
                print("ERROR #00", i,": There is a problem with your, ",errordisplay[i], " data. It does is not in the correct format or missing.",  sep='')
                quit()
            n += 1




    def checkReflector(self,reflector):
        '''
        Purpose: Checks if Relfector is a a valid input
        :param reflector: Reflector to check
        :return: NONE
        '''
        reflector = reflector.upper()
        if reflector == 'B' or reflector == 'C':
            reflector = reflector
        else:
            print("ERROR #201: Reflector is neither B or C.")
            quit()




    def checkPlugs(self,plugs):
        '''
        Purpose: Checks if plugs are all letters and if they are pairs
        :param plugs: What is to be tested
        :return: NONE
        '''
        plugs1 = plugs
        strippedplugs = plugs1.replace(" ", "")
        length = len(strippedplugs)
        for letter in strippedplugs:             #checks if characters are in alpha as well as converts to upper
            if not(letter.isalpha()):
                print("ERROR #203: Plugs are not all letters.")
                quit()
            elif not length%2 == 0:
                print("ERROR #204: There are not an even amount of plugs. There needs to be pairs.")
                quit()
            else:
                plugs1 = plugs1




    def wheelCheck(self,wheels):
        '''
        Purpose: Checks if wheels given are between 1 and 8
        :param wheels: What is to be tested
        :return: NONE
        '''
        for i in range(len(wheels)):                #tests to make sure that each wheel given is from 1-8
            if wheels[i] < 0 or wheels[i] > 8:
                print("ERROR #205: Wheels are not numbers 1-8.")
                quit()
            else:
                i=i




    def numberOfRotorsCheck(self,amount):
        '''
        Purpose: Counts the amount of rotors and makes sure it is in between 1 and 4.
        :param amount: What is to be tested.
        :return: NONE
        '''
        if amount != 4:            #Tests that the amount of rotors are in 1 to 4.
            print("ERROR #206: We need 3 rotors.")
            quit()






    ###########################################-------EDITING AND EFFECTING-------##########################################


    def textinput(self):
        '''
        Purpose: Grabs from file, reads it, splits string by new line.
        :param NONE:
        :return: The result of what is in the read file with the new lines stripped.
        '''
        f = open('EnigmaFile.txt', 'r')         #opens EnigmaFile.txt to read
        string = f.read()                       #copies whats in file and sets it to string
        f.close()                               #closes file
        stringsplit = string.split('\n')        #splits input information by new line into a list
        return stringsplit




    def cleantext(self,incomingtext):
        '''
        Purpose: Cleans the rotor and converts it to usable form.
        :param incomingtext: the string to be cleaned and converted
        :return:
        '''
        cleanedoutput= ""
        for letter in incomingtext:             #checks if characters are in alpha as well as converts to upper
            if not(letter.isalpha()):
                cleanedoutput = cleanedoutput
            else:
                cleanedoutput += letter.upper()
        return cleanedoutput




    def cleanrotor(self,incomingrotor):
        '''
        Purpose: Cleans the rotor and converts it to usable form.
        :param incomingrotor: the rotor to be cleaned and converted
        :return:
        '''
        cleanedrotor= ""
        for letter2 in incomingrotor:           #checks if characters are in alpha as well as converts to upper
            if not(letter2.isnumeric()):
                cleanedrotor = cleanedrotor
            else:
                cleanedrotor += letter2.upper()
        rotorWheels = list(cleanedrotor)
        rotorWheels = [int(x) for x in rotorWheels]                   #converts to int
        rotorWheels.insert(0,0)
        '''
        for i in range(len(rotorWheels)):       #lets user enter any number of rotors 1-4 and this takes in account and inserts zeros
            if roterCounter(rotorWheels) != 4:
                rotorWheels.insert(i,0)
                print(rotorWheels)
        '''
        return rotorWheels





    def roterCounter(self,rotors):
        '''
        Purpose: Gets the length of the given rotors.
        :param rotors: Rotors to be counted
        :return: The length of the rotors.
        '''
        length = 0
        for i in range(len(rotors)):            #for loop counts the length of the rotors
            length += 1
        return length







    ###########################################-------GIVEN DATA-------#####################################################


    def getMasterRotorList(self):
        '''
        Purpose: contains rotors I to VIII
        :param NONE:
        :return: the rotors

        '''
        rotorMasterList = [
            list("." + string.ascii_uppercase),             #list of rotors
            list(".EKMFLGDQVZNTOWYHXUSPAIBRCJ"),
            list(".AJDKSIRUXBLHWTMCQGZNPYFVOE"),
            list(".BDFHJLCPRTXVZNYEIWGAKMUSQO"),
            list(".ESOVPZJAYQUIRHXLNFTGKDCMWB"),
            list(".VZBRGITYUPSDNHLXAWMJQOFECK"),
            list(".JPGVOUMFYQBENHZRDKASXLICTW"),
            list(".NZJHGRCXMYSWBOUFAIVLPEKQDT"),
            list(".FKQHTLXOCBJSPDZRAMEWNIUYGV")
        ]
        return rotorMasterList




    def getReflectorList(self):
        '''
        Purpose: contains two reflectors.  The official system calls them 'b' and 'c'
        :param NONE:
        :return: the reflector list

        '''
        reflectorMasterList = [
            list(".YRUHQSLDPXNGOKMIEBFZCWVJAT"),             # this is 'b'
            list(".FVPJIAOYEDRZXWGCTKUQSBNMHL")              # this is 'c'
        ]
        return reflectorMasterList




    def plugboard(self, trans, message):
        '''
        Purpose: replaces the selected letters with what is to be replaced (EX: if 'AK' is on the plugboard all A's are switched to K's)
        :param trans: a list of plugboard pairs
        :param message: the incoming message to be encoded
        :return: the message with the letters swapped

        '''
        for pair in trans:                                  #replaces with the given plugs
            message = message.replace(pair[1], "!")
            message = message.replace(pair[0], pair[1])
            message = message.replace("!", pair[0])
        return message









    ###########################################-------ENCRYPTION-------#####################################################
    def ringSettings(self, rings,rotorwheels):
        '''

        :param ring:
        :param rotorwheels:
        :return:
        '''
        masterList = self.getMasterRotorList()
        rotorwheels.pop(0)
        one = masterList[rotorwheels[0]]
        two = masterList[rotorwheels[1]]
        three = masterList[rotorwheels[2]]
        ringlist = list(rings)
        indexlist = []
        n=0
        letter = 0
        for i in rotorwheels:
            n+=1
            #print(i)
            for l in masterList[i]:
                #print(l)
                pass
            indexlist.append(masterList[i].index(ringlist[letter]))
            letter+=1
            #print(indexlist)
        rotorone = one[indexlist[0]:] + one[1:indexlist[0]]
        rotortwo = two[indexlist[1]:] + two[1:indexlist[1]]
        rotorthree = three[indexlist[2]:] + three[1:indexlist[2]]
        rotorone.insert(0,'.')
        rotortwo.insert(0,'.')
        rotorthree.insert(0,'.')
        masterList[rotorwheels[0]] = rotorone
        masterList[rotorwheels[1]] = rotortwo
        masterList[rotorwheels[2]] = rotorthree
        rotorwheels.insert(0,0)
        return masterList




    def encryptByRotor(self, curRotor, nextRotor, inString):
        '''
        Purpose: Encrypts by given rotor
        :param curRotor: Has current rotor
        :param nextRotor: Has next rotor
        :param inString: String to be encrypted
        :return: The result of inString being encrypted
        '''
        inList = list(inString)                 #Converts whats in the string to a list
        result = ""
        for letter in inList:                   #Converts character by character
            x = curRotor.index(letter)
            ch = nextRotor[x]
            result += ch
        return result




    def encrypt(self, plugs, startingString, numberOfRotors, dailyScheduledRotors, reflectorRequest, TR, ring):
        '''
        Purpose: Encrypts or Decrypts the given string depending on Receiveing or Sending
        :param plugs: the plugboard settings
        :param startingString: The message to be translated
        :param numberOfRotors: How many rotors, including the zeroth one
        :param dailyScheduledRotors:Today's rotor list
        :param reflectorRequest: which reflector
        :param TR: a boolean for transmit/receive
        :return: the encrypted and decrytped message
        '''
        try:
            assert isinstance(plugs, str)                       #test to make sure plugs are a string
            assert isinstance(startingString, str)              #test to see if starting string is a string
            assert isinstance(numberOfRotors, int)              #test to see if number of rotors is integers
            assert all(isinstance(v, int) for v in dailyScheduledRotors) and len(dailyScheduledRotors)==4
            assert isinstance(reflectorRequest, str)            #test if reflector is type string
            assert isinstance(TR, str)                          #test if reflector is type string

            n =4

            if TR == 'T':                                       #if user is transmiting data
                ringtwo =ring
                dailyScheduledRotorstwo = dailyScheduledRotors
                ringSettingRotor = self.ringSettings(ringtwo, dailyScheduledRotorstwo)
                #print(ringSettingRotor)
                rotorMasterList = self.ringSettings(ring,dailyScheduledRotors)          #gets the list of rotors
                reflectorMasterList = self.getReflectorList()        #gets the list of reflectors

                startingString = self.encryptByRotor(rotorMasterList[0], plugs, startingString)          #convert the message using the plug settings
                print("-----------------------------")
                print("Plugs applied: ")

                print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))

                temp = rotorMasterList[0]                       #save the original data in rotor master list
                rotorMasterList[0] = list(plugs)                #save the plug settings to the master rotor list
                print("-----------------------------")
                print("Encrypt: ")
                for i in range(numberOfRotors - 1):             #go through all the rotors one at a time and encrypt
                    #print(i, ": ", str(rotorMasterList(dailyScheduledRotors[i])), i+1, ": ", str(rotorMasterList(dailyScheduledRotors)))           #debug line
                    startingString = self.encryptByRotor(rotorMasterList[dailyScheduledRotors[i]], rotorMasterList[dailyScheduledRotors[i+1]], startingString)
                    print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))
                print("-----------------------------")
                print("Reflect:")
                # no error handling yet
                reflectorRequest = reflectorRequest.upper()     #Converts to uppercase
                if TR == 'T':                                   #Test to see if it is to Tranceive
                    TR = True
                else:
                    TR = False
                                                                #reflect the message and then send the reflection back to the last rotor
                if TR:                                          #Reflects the message across the desired reflector
                    if reflectorRequest == 'B':
                        startingString = self.encryptByRotor(rotorMasterList[dailyScheduledRotors[numberOfRotors-1]], reflectorMasterList[0], startingString)
                    else:
                        startingString = self.encryptByRotor(rotorMasterList[dailyScheduledRotors[numberOfRotors - 1]], reflectorMasterList[1], startingString)          #reflector c
                else:
                    if reflectorRequest == 'B':
                        startingString = self.encryptByRotor(reflectorMasterList[0], rotorMasterList[dailyScheduledRotors[numberOfRotors - 1]], startingString)
                    else:
                        startingString = self.encryptByRotor(reflectorMasterList[1], rotorMasterList[dailyScheduledRotors[numberOfRotors - 1]], startingString)          #reflector c
                print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))
                print("-----------------------------")
                print("Reverse:")

                for i in range(numberOfRotors - 1, 0, -1):      #go from the last rotor back to the zeroth one - which still has the plugboard swap
                    #print(i, ": ", str(rotorMasterList[dailyScheduledRotors[i]], rotorMasterList[dailyScheduledRotors[i-1]], startingString))          #debug
                    startingString = self.encryptByRotor(rotorMasterList[dailyScheduledRotors[i]],rotorMasterList[dailyScheduledRotors[i-1]],startingString)
                    print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))
                rotorMasterList[0] = temp                       #get regular alphabet back
                startingString = self.encryptByRotor(plugs, rotorMasterList[0], startingString)      #change from the plugboard data back to the alphabet
                print("-----------------------------")
                print("Plugs applied:")
                print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))
                print("-----------------------------")
                print("Encrypted:")
                print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))
                return startingString
            elif TR == "R":                                     #Test to see if User is Receiving
                rotorMasterList = self.ringSettings(ring,dailyScheduledRotors)
                reflectorMasterList = self.getReflectorList()
                startingString = self.encryptByRotor(rotorMasterList[0], plugs, startingString)      #convert the message using the plug settings
                print("-----------------------------")
                print("Plugs applied: ")
                print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))
                temp = rotorMasterList[0]                       #save the plug settings to the master rotor list, but also save the original data
                rotorMasterList[0] = list(plugs)
                print("-----------------------------")
                print("Encrypt: ")
                for i in range(numberOfRotors - 1):             #go through all the rotors one at a time and change
                    #print(i, ": ", str(rotorMasterList(dailyScheduledRotors[i])), i+1, ": ", str(rotorMasterList(dailyScheduledRotors)))       #debug
                    startingString = self.encryptByRotor(rotorMasterList[dailyScheduledRotors[i]], rotorMasterList[dailyScheduledRotors[i+1]], startingString)
                    print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))
                print("-----------------------------")
                print("Reflect:")
                # no error handling yet
                reflectorRequest = reflectorRequest.upper()     #Converts to uppercase
                if TR == 'T':
                    TR = True
                else:
                    TR = False
                if TR:                                          #reflect the message and then send the reflection back to the last rotor
                    if reflectorRequest == 'B':
                        startingString = self.encryptByRotor(rotorMasterList[dailyScheduledRotors[numberOfRotors-1]], reflectorMasterList[0], startingString)
                    else:
                        startingString = self.encryptByRotor(rotorMasterList[dailyScheduledRotors[numberOfRotors - 1]], reflectorMasterList[1], startingString)
                else:
                    if reflectorRequest == 'B':
                        startingString = self.encryptByRotor(reflectorMasterList[0], rotorMasterList[dailyScheduledRotors[numberOfRotors - 1]], startingString)
                    else:
                        startingString = self.encryptByRotor(reflectorMasterList[1], rotorMasterList[dailyScheduledRotors[numberOfRotors - 1]], startingString)
                print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))
                print("-----------------------------")
                print("Reverse:")
                for i in range(numberOfRotors - 1, 0, -1):      #go from the last rotor back to the zeroth one - which still has the plugboard swap
                    #print(i, ": ", str(rotorMasterList[dailyScheduledRotors[i]], rotorMasterList[dailyScheduledRotors[i-1]], startingString))      #debug
                    startingString = self.encryptByRotor(rotorMasterList[dailyScheduledRotors[i]],rotorMasterList[dailyScheduledRotors[i-1]],startingString)
                    print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))
                rotorMasterList[0] = temp                       #get regular alphabet back
                startingString = self.encryptByRotor(plugs, rotorMasterList[0], startingString)      #change from the plugboard data back to the alphabet
                print("-----------------------------")
                print("Plugs applied")
                print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))
                print("-----------------------------")
                print("Decrypted:")
                print(' '. join([startingString[i:i+n] for i in range(0, len(startingString), n)]))
                return startingString
            else:
                print("Error #202: User value is neither Transceiver nor Receiver. 'T' or 'R'.")
                quit()
        except:
            error = "ERROR"
            return(error)






###########################################-------MAIN-------###########################################################


def main():
    test = Enigma()


if __name__ == "__main__":
    main()
