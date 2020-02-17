import re
import os

# This is a programme to convert a .BRF (Braille Ready File) into a
# .TXT (Plain Text File).
# We do so by going word by word, line by line.
# The word gets split up into pieces based on punctuation, numbers,
# and capitalisation.

Brackets = {"^8":"B", "^0":"B", '"<':"C", '">':"D", ",-":"--", "'8":"E", "'7":"E", ".<":"F", ".>":"G"}

TwoLetters = {"_/":"A", '"9':"H", "@l":"I", "@s":"J", "@e":"K", "@y":"L"}

Caps_to_ASCII = {"A":"/", "B":'"', 'C':'(', 'D':')', "E":"'", "F":"[", "G":"]", "H":"*", "I":"£", "J":"$", "K":"€", "L":"¥"}

EndPunctuation = {"4":".", "6":"!","8":"?", "1":",", "-":"-", "3":":", "2":";"}

Number = {"a":"1", "b":"2", "c":"3", "d":"4", "e":"5", "f":"6", "g":"7", "h":"8", "i":"9", "j":"0", "4":".", "1":","}
# ------------------------------------------------------------
def ConvertStuff(Translate, Type, Word, L):
    for Key in Caps_to_ASCII:
        Word = Word.replace(Key, Caps_to_ASCII[Key])

    Translate[L] = 3
# ------------------------------------------------------------
def BracketsAndStuff(Translate, Type, Word, Passage, WordCap):
# This function replaces all the brackets in the word
# with capital letters (which can't occur in the BRF
# file naturally). 
# This also splits the word by brackets
# Example: ("Hello") -> [(, ", Hello, ", )]

    Caps = 'BCDEFG'
    Temp = []
    TempType = []
    Piece = ""

    for i in range(len(Word)):
        for Key in Brackets:
            if(Word[i:i+2] == Key):
                Word = Word.replace(Key, Brackets[Key])

    for i in range(len(Word)):
        for Key in Brackets:
            if(Word[i:i+2] == Key):
                Word = Word.replace(Key, Brackets[Key])

    X = -1

    for Letter in Word:
        X += 1
        if(Letter in Caps):
            if(Piece != ""):
                Temp.append(Piece)

                if(Passage == True or WordCap == True):
                    TempType.append(3.1)
                else:
                    TempType.append(3.0)

                Piece = ""
                
            Temp.append(Letter)
            TempType.append(2.0)
        else:
            Piece += Letter

    if(Piece != ""):
            Temp.append(Piece)

            if(Passage == True or WordCap == True):
                TempType.append(3.1)
            else:
                TempType.append(3.0)
            Piece = ""

    for i in Temp:
        Translate.append(i)

    for i in TempType:
        Type.append(i)

    return Translate, Type
# ------------------------------------------------------------
def Quotations(Translate, Type, Word, L, Passage, WordCap):

    A = bool(Word[0] == "8")
    B = bool(Word[-1] == "0")

    if(A and not B):
        Translate[L] = "B"
        Type[L] = 2.0

        Translate = InsertInList(Translate, L, Word[1:])

        if(Passage == True or WordCap == True):
            Type = InsertInList(Type, L, 3.1)
        else:
            Type = InsertInList(Type, L, 3.0)

    elif(B and not A):
        Translate[L] = Word[:-1]
        Type[L] = 3.0

        Translate = InsertInList(Translate, L, "B")
        Type = InsertInList(Type, L, 2.0)

    elif(A and B):
        Translate[L] = "B"
        Type[L] = 2.0

        Translate = InsertInList(Translate, L, "B")
        Type = InsertInList(Type, L+1, 2.0)

        Word = Word[1:]
        Word = Word[:-1]

        Translate = InsertInList(Translate, L, Word)

        if(Passage == True or WordCap == True):
            Type = InsertInList(Type, L, 3.1)
        else:
            Type = InsertInList(Type, L, 3.0)   

    else:
        pass

    return Translate, Type
# ------------------------------------------------------------
def InsertInList(List, Place, Element):
# This puts the Element into the List at a certain Place
    Temp = [0]*(len(List)+1)

    List.append(0)

    for y in range(len(Temp)):
        if(y <= Place):
            Temp[y] = List[y]
        elif(y == (Place+1)):
            Temp[y] = Element
        else:
            Temp[y] = List[y-1]

    List = Temp
    
    return List  
# ------------------------------------------------------------
def Hyphens(Translate, Type, Word, L, Passage, WordCap):
    WordPieces = Word.split("-")

    Temp = []
    TypeTemp = []

    for Piece in WordPieces:
        Temp.append(Piece)

        if(Passage == True or WordCap == True):
            TypeTemp.append(3.1)
        else:
            TypeTemp.append(3.0)

        
        Temp.append("-")
        TypeTemp.append(2.0)

    del Temp[-1]
    del TypeTemp[-1]

    Translate[L] = Temp[0]
    Type[L] = TypeTemp[0]

    del Temp[0]
    del TypeTemp[0]

    for i in range(len(Temp)):
        Translate = InsertInList(Translate, L+i, Temp[i])

    for i in range(len(TypeTemp)):
        Type = InsertInList(Type, L+i, TypeTemp[i])

    return Translate, Type
# ------------------------------------------------------------
def EndPunc(Translate, Type, Word, L, Passage, WordCap):
    Word = Word.replace(",,", "")
    Word = Word.replace(",'", "")

    Drow = Word[::-1]
    Pmet = ""
    PmetEpyt = []

    for Rettel in Drow:
        if(Rettel not in "4681-32"):
            break
        else:
            for Key in EndPunctuation:
                if(Rettel == Key):
                    Pmet += EndPunctuation[Key]

    Drow = Drow[len(Pmet):]
    Translate[L] = Drow[::-1]

    if(Passage == True or WordCap == True):
        Type[L] = 3.1
    else:
        Type[L] = 3.0

    if(Pmet != ""):
        Translate = InsertInList(Translate, L, Pmet[::-1])
        Type = InsertInList(Type, L, 2.0)

    return Translate, Type
# ------------------------------------------------------------
def Numbers(Translate, Type, Word, L):
    Temp = ""
    Set = 0
    
    for Letter in Word:
        if(Letter == "#"):
            Set = 1
            continue

        if(Set == 1):
            if(Letter not in "abcdefghij41"):
                Set = 0
                Temp += Letter
            else:
                for Key in Number:
                    if(Letter == Key):
                        Temp += Number[Key]

        else:
            Temp += Letter

    Translate[L] = Temp

    return Translate, Type
# ------------------------------------------------------------
def Translate(Braille, Text):
    for Line in Braille:
        Passage = False
        Delay = 0

        Line = Line.strip()
        Line = Line.split()

        if(Line == []):
            Text.write("\n")
            continue

        for Word in Line:
            Translate = []
            Type = []
            WordCap = False

            if(",,," in Word):	#	Caps Passage
                Passage = True

            if(",'" in Word):
                Passage = False

            if((",," in Word) and not (",,," in Word)):
                WordCap = True

            [Translate, Type] = BracketsAndStuff(Translate, Type, Word, Passage, WordCap)
            # Split up based on punctuation that are
            # A. two-character, and B. can occur anywhere in the word.

            TempType = Type

            for i in range(len(Translate)):
                if(TempType[i] == 3.0 or TempType[i] == 3.1):
                    [Translate, Type] = Quotations(Translate, Type, Translate[i], i, Passage, WordCap)
            # This is to make sure that the single-character quotation marks
            # are accounted for. This will be important for later.

            TempType = Type     

            for i in range(len(Translate)):
                if(TempType[i] == 3.0 or TempType[i] == 3.1):
                    [Translate, Type] = Hyphens(Translate, Type, Translate[i], i, Passage, WordCap)
            # Split up words separated by hyphens
            # Hyphens can occur anywhere in the word too.

            TempType = Type

            for i in range(len(Translate)):
                if(TempType[i] == 3.0 or TempType[i] == 3.1):
                    [Translate, Type] = EndPunc(Translate, Type, Translate[i], i, Passage, WordCap)
            # This processes the end punctuation (?, !, ., etc.)
            # This needs to be done first because the symbols for
            # end punctuation can also be letters.

            TempType = Type

            for i in range(len(Translate)):
                if(TempType[i] == 3.0 or TempType[i] == 3.1):
                    [Translate, Type] = Numbers(Translate, Type, Translate[i], i)
            # This processes the numbers

            for Key in Caps_to_ASCII:
                X = [Caps_to_ASCII.get(x, x) for x in Translate]
            Translate = X

            i = -1
            for Word in Translate:
                i += 1
                if(Type[i] == 3.1):
                    Translate[i] = Word.upper()

            Set = 0

            i = -1

            for Word in Translate:
                TempWord = ""
                i += 1
                if(Type[i] == 3.0 or Type[i] == 3.1):
                    for j in range(len(Word)):
                        if(Set > 0):
                            Set -= 1
                            TempWord += Word[j].upper()
                            continue

                        if(Word[j] == ","):
                            Set = 1
                            continue
                        else:
                            TempWord += Word[j]
                    Translate[i] = TempWord

            for Word in Translate:
                Text.write(Word)

            Text.write(" ")

        Text.write("\n")
# ------------------------------------------------------------
Continue = 0

while(Continue != "1"):
    Name = input("Enter name of BRF file: ")
    print(" ")

    BrailleFile = open(Name + ".brf", "r")
    TextFile = open(Name + ".txt", "w")

    Translate(BrailleFile, TextFile)

    TextFile.close()

    print("Done!")
    print(" ")

    Continue = input("Do another file? 1 to quit. ")
    print(" ")

print("Goodbye!")
