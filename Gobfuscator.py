import sys, string
from Crypto.Random.random import randrange

#from capstone import *

def stringXOR(plaintext, key):		#Function for a simple XOR encrypt on targeted strings
	length = len(plaintext)			#NOTE: Key needs to be longer than the sting being encrypted so it will be randomly generated to be this parameter
	cipherAscii = ''
	xor = ''

	for i in range (0, length):
		j = ( i % length )
		
		if (plaintext[i] != key[j]):
			xor = ord(plaintext[i]) ^ ord(key[j])
		cipherAscii += (chr(xor))

		
	return(cipherAscii)


###############################################################################################################################################################################

def generateRandomKey(keyLen):
	key = ''
	charPool = string.ascii_letters + string.digits		#Create a string containing all upper and lower case letters and digits from 0-9
	
	key = ''.join( charPool[randrange( len( charPool ) )] for i in range (keyLen) )		#Randomly pick characters from the above string until the specified ;ength is met
	return key


###############################################################################################################################################################################


def findBorders (asmCode, startEndArray): 	#Can't think of a catchier function name 
											#for now but this will find the start and end of the .text segment of the ASM file
	startPoint = asmCode.find('\n_start:') + 8
	startEndArray.append(startPoint)
	
	endPoint = asmCode.find('\nsection', startPoint)
	if ( endPoint != -1 ):		#Ideally want to make this 
		startEndArray.append(endPoint)
	else:
		startEndArray.append(len(asmCode))
		
		
		
	dataSecStart = asmCode.find('\nsection .data') + 14
	startEndArray.append(dataSecStart)
	
	endPoint = asmCode.find('\nsection', dataSecStart, len(asmCode))
	if ( (endPoint) != -1 ):
		startEndArray.append(endPoint)
	else:
		startEndArray.append(len(asmCode))
	
	return startEndArray

##############################################################################################################################################################################


def locateStrings(asmCode, startPoint, endPoint, startOfTextSec):

	startOfString = 0
	endOfString = 0
	
	XORtedOut = ''			#[For building a XORed string in testing]
	
	XORcounter = 0			#Tracks position within the string that is being encrypted
	modCodeList = list(asmCode)		#String that will be used to store the newly modified version of the ASM code in list form so each element can be individually replaced
	newString = True		#This will track if the quotation mark being found next is the start of a new string or the end of the last one
	randomKey = ''			#Will be used to store the randomly generated key for encrypting and decrypting strings
	modCode = ''			#Variable for the altered code which will be returned at the end of the function
	nextLineBreak = 0
	illegalString = False	#Tracks if the output XORed string contains characters that would break the way strings are stored in ASM
	
	varName = ''		#Used to store the names of each string variable so they can be used to decrypt it inside the code later
	
	i = startPoint
	for i in range (startPoint, endPoint):		#Will most likely cause problems with alternation quote-type substrings eg "I would have 'never' thought of that". Fix later#######
		if (asmCode[i] == '"'):
			if (newString == True):
				startOfString = (i+1)				#Mark the found quotation as the beginning of the string
				endOfString = asmCode.find('"', (i+1), endPoint)		#finding the next same-type quotation to close the string
				
				newString = False	#Tells program next quotation mark will be closing not opening
				
				
				######			ENCRYPTION HAPPENING		########
				XORcounter = startOfString
				for XORcounter in range(startOfString, endOfString + 1):	#EndOfString is actually marking the " instead of the final character so 
					XORtedOut += asmCode[XORcounter]					#the loop stops at the last character
				
				illegalString = True
				while(illegalString == True):	#Loop testing for string breaking characters, key will keep being regenerated until string is free of them
					randomKey = generateRandomKey( len(XORtedOut) )		#Key for encryption is generated
					XORtedOut = stringXOR( XORtedOut, randomKey )		#String is put through XOR function
					if (XORtedOut.find('/n') == -1 and XORtedOut.find('"') == -1 and XORtedOut.find(' ') == -1 and XORtedOut.find("'") == -1):
						illegalString = False
				
				XORcounter = startOfString	#Reset this counter to be used again
				
				for XORcounter in range (startOfString, endOfString):	#This loop will be used to write the newly encrypted strings into modCode
					modCodeList[XORcounter] = XORtedOut[XORcounter - startOfString]		#Counter minus the start pos should leave just the index of the letter in the encrypted string

				XORtedOut = ''		#Reset variable to blank 
				
				
				modCode = ''.join( [str(item) for item in modCodeList] )	#Converting the modified code into string format 
				modCodeList = list(modCode)			#Updating the list version of modcode to match the latest version of the code
				
				
				
				####################################################
				
			else:
				newString = True		#Marks that the last string is finished and the next quotation starts a new one
				
				#This section will be used to detect the variable name being used for the string 
				j = startOfString - 6	#minus six spaces should get past the ' dw ' used in defining strings and into the name of the variable
				while (asmCode[j] != '\t' and asmCode[j] != '\n' and asmCode[j] != ' '):
					varName += asmCode[j]
					j -= 1
				
				varName = varName[::-1]		#Simple way to mirror the varName string since it was read in backwards
				
				modCode = addDecoder(modCode, varName, randomKey, startOfTextSec)		#IMPORTANT: Needs to be provided position for start of .text section
				#For some reason this is only producing decoder for most recent string. Not overwriting. Not sure what could be wrong. Investigate further
				
				varName = ''
				
		####################################################################################################################################################################
		elif (asmCode[i] == "'"):		################# This is all effectively the same but for single quotations ##########################
			if (newString == True):
				startOfString = (i+1)				#Mark the found quotation as the beginning of the string
				endOfString = asmCode.find("'", (i+1), endPoint)		#finding the next same-type quotation to close the string
				
				newString = False	#Tells program next quotation mark will be closing not opening
				
				
				######			ENCRYPTION HAPPENING		########
				XORcounter = startOfString
				for XORcounter in range(startOfString, endOfString + 1):	#EndOfString is actually marking the " instead of the final character so 
					XORtedOut += asmCode[XORcounter]					#the loop stops at the last character
				
				illegalString = True
				while(illegalString == True):	#Loop testing for string breaking characters, key will keep being regenerated until string is free of them
					randomKey = generateRandomKey( len(XORtedOut) )		#Key for encryption is generated
					XORtedOut = stringXOR( XORtedOut, randomKey )		#String is put through XOR function
					if (XORtedOut.find('/n') == -1 and XORtedOut.find('"') == -1 and XORtedOut.find(' ') == -1 and XORtedOut.find("'") == -1):
						illegalString = False
				
				XORcounter = startOfString	#Reset this counter to be used again
				
				for XORcounter in range (startOfString, endOfString):	#This loop will be used to write the newly encrypted strings into modCode
					modCodeList[XORcounter] = XORtedOut[XORcounter - startOfString]		#Counter minus the start pos should leave just the index of the letter in the encrypted string

				XORtedOut = ''		#Reset variable to blank 
				
				
				modCode = ''.join( [str(item) for item in modCodeList] )	#Converting the modified code into string format 
				modCodeList = list(modCode)			#Updating the list version of modcode to match the latest version of the code
				
				
				
				####################################################
				
			else:
				newString = True		#Marks that the last string is finished and the next quotation starts a new one
				
				#This section will be used to detect the variable name being used for the string 
				j = startOfString - 6	#minus six spaces should get past the ' dw ' used in defining strings and into the name of the variable
				while (asmCode[j] != '\t' and asmCode[j] != '\n' and asmCode[j] != ' '):
					varName += asmCode[j]
					j -= 1
				
				varName = varName[::-1]		#Simple way to mirror the varName string since it was read in backwards
				
				modCode = addDecoder(modCode, varName, randomKey, startOfTextSec)		#IMPORTANT: Needs to be provided position for start of .text section
				
				varName = ''
		#########################################################################################################################################################################
	return modCode

#####################################################################################################################################
def addDecoder(asmCode, encryptedStringName, key, secStart):
		payload = '\txor ' + encryptedStringName + ', "' + key + '"\n'
		
		splitPos = asmCode.find("\n", secStart)+1		#Finds next available line break and goes one character after it
		firstHalf = asmCode[ :splitPos ]
		secondHalf = asmCode[ splitPos: ]
		
		output = firstHalf + payload + secondHalf
		#print (output)
		return output
		#Something causing only decoder for last string being added in even though the function executes 3 times
		#Does not look like overwritinga dn happens regardless if strings use different quote types from each other 

#####################################################################################################################################
def jumpChain(asmCode, jmpLimit, secStart, secEnd):
	#length = len(asmCode)	#Initialise variables
	i = 0
	j = 0
	jmpCounter = 0
	
	lineBreakPos = []
	splitPos = 0
	
	firstHalf = ""
	secondHalf = ""

	#Create index of all positions where line breaks are found
	for i in range(secStart, secEnd):
		if (asmCode[i] == '\n'):	#Found one!
			lineBreakPos.append(i)	#Add the position into the array
		
	#Randomly select one of the positions 
	while (jmpCounter < jmpLimit):
		splitPos = randrange(1, len(lineBreakPos) - 1)		#Pick a random line break from the array
		
		firstHalf = asmCode[ :lineBreakPos[splitPos] ]		#Split the code into 2 sections around the line break
		secondHalf = asmCode[ lineBreakPos[splitPos]: ]
		
		if (jmpCounter == (jmpLimit - 1)):			#If this is the last label being inserted the code will jump back to the first label
			asmCode = firstHalf + "\nmyL" + str(jmpCounter) + ":\n\tjmp myL0" + secondHalf
		else:
			asmCode = firstHalf + "\nmyL" + str(jmpCounter) + ":\n\t\n\tadd eax 4\n\tsub eax 4\n\tjmp myL" + str(jmpCounter + 1) + secondHalf	#Add/Sub commands are just there to make the uselessness of the JMP less obvious
		
		jmpCounter += 1
		for j in range(splitPos, len(lineBreakPos)):	#Increase all the values in the array after the split
			lineBreakPos[j] += ( len(asmCode) - (len(firstHalf) + len(secondHalf)) )	#by the length of the inserted code 
			
	asmCode = analyserCrasher(asmCode, lineBreakPos)	#Called within this method so the same array of line breaks can be used without calculating it again

	
	return asmCode
#####################################################################################################################################


####################	CRASHER		##########################
def analyserCrasher(myCode, lineBreakArray):
	firstHalf = ""
	secondHalf = ""


	randomBreak = randrange(0, len(lineBreakArray) - 1)			#Minus 1 to stop last entry being picked which causes breaks
	firstHalf = myCode[:lineBreakArray[randomBreak]]
	secondHalf = myCode[lineBreakArray[randomBreak]:]

	payload = '\n\tcmp 2 32\n\tje short 01 103\n\tadd eax 4\n\tsub eax 4\n'		#'$+1' may need to be changed for '$+1' depending on which SHORT jump type is used for NASM syntax
																		#This SHOULD jump 1 byte forward which should be part way through the ADD instruction which would crash the program
	myCode = firstHalf + payload + secondHalf							#This should only happen when being debugged since it is nested in a permanently false conditional
	
	return myCode


####################	CRASHER		##########################


inputFile = input('Please specify the full or relative path to the file you wish to obfuscate ...\n\n\n')
asmFile = open(inputFile)		#Allowing user to specify which file they would like to obfuscate
asmCode = asmFile.read()


params = []	#This array will be used to mark and track the beginning and end of the '.text' and .data segments where the main method of the code should be.

findBorders(asmCode, params)


newCode = locateStrings( asmCode, params[2], params[3] , params[0])	#New code will be the version of asmCode with obfuscations mods made to it


jumpNumber = (len(asmCode) % 4) + 2			#The number of JMP commands that will be inserted into the code - needs to be randomised without exceeding number of available lines
newCode = jumpChain(newCode, jumpNumber, params[0], params[1])		#NOTE Line must be added in to randomise jmpLimit -> [Will need to be based on line count]


outFile = input ('\n\n\nEnter the name you wish to use for the obfuscated file ...\n(Entering the path and name of the original file will just make adjustments to that original)')


##	This will be writing the new code into a file. This needs to be last 
newFile = open(outFile, 'w')	#Checks if specified file for output to be written to exists and, if not, creates it
newFile.write(newCode)		#Writes the mofified code to the file specified by the user.

################################################################################################################################


"""
def disassemble(exe):
	#CODE = b"\x55\x48\x8b\x05\xb8\x13\x00\x00"
	f = open(exe, 'r+b')
	CODE = f.read()

	md = Cs(CS_ARCH_X86, CS_MODE_64)
	for i in md.disasm(CODE, 0x1000):
		print ("%s\t%s" % (i.mnemonic, i.op_str))
"""
