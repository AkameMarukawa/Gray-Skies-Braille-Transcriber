import os
import re

# This (mostly) uses UEB rules so don't sue me if your
# thing comes out wrong cause you wrote it in EBAE or
# something.
# ----------------------------------------------------

TwoCharSymb = {'"<':"α", '">':"β", "_/":"γ", "@s":"δ", \
               "@&":"ε", ".<":"ζ", ".>":"η", "@<":"θ", \
               "@>":"ι", "_6":"κ", '"6':"λ", '"-':"μ", \
               '"7':"ν", "@a":"ξ", '"8':"π", '"4':"ρ", \
               '"/':"σ", "@>":"τ", "@<":"υ", ".0":"φ", \
               "^j":"χ", "_[":"ψ", "_?":"ω", "_4":"え", \
               ";8":"8", ';0':"0", "^3e":"☆e", "^3o":"☆", \
               "^3u":"☆u", "^3a":"☆a", "^3i":"☆i", "_*o":"♧"}

TwoCharPunc = {"α":"(", "β":")", "γ":"/", "δ":"\\$", "ε":"&", \
               "ζ":"[", "η":"]", "θ":"\\{", "ι":"\\}", "κ":"$\pm$", \
               "λ":"+", "μ":"-", "ν":"=", "ξ":"@", "π":"*", \
               "ρ":"$\cdot$", "σ":"$\div$", "τ":"$>$", "υ":"$<$", \
               "φ":"%", "χ":"\degree", "ψ":"$\angle$", "ω":"#", \
               "え":"$\bullet$", "☆":'\\"', "♧":"\\o "}

Removal = ["ゆ", "よ", ":", ";", "せ", "そ", "あ", "い", "う", "か", \
           "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", \
           "λ", "μ", "ν", "ξ", "π", "ρ", "σ", "τ", "υ", "φ", \
           "χ", "ψ", "ω", "え", ".", "?", "!", ",", "∑", "œ", "(", \
           ")", "[", "]", "{", "}"]

SingleWordRemoval = ["ゆ", "よ", "2", "3", "せ", "そ", "あ", "い", "う", "か", \
           "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", \
           "λ", "μ", "ν", "ξ", "π", "ρ", "σ", "τ", "υ", "φ", \
           "χ", "ψ", "ω", "え", "4", "8", "6", "1", "0", ",", "∑", "œ"]

SingleWord = {"b":"but", "c":"can", "d":"do", "e":"every", \
              "f":"from", "g":"go", "h":"have", "j":"just", \
              "k":"knowledge", "l":"like", "m":"more", "n":"not", \
              "p":"people", "q":"quite", "r":"rather", "s":"so", \
              "t":"that", "u":"us", "v":"very", "w":"will", \
              "x":"it", "y":"you", "z":"as", "*":"child", "/":"still",
              "%":"shall", "?":"this", ":":"which", "\\":"out"}

Beginning = {"2":"bbe", "3":"con", "4":"dis"}

MoreWords = {'"d':"day", '"e':"ever", '"f':"father", '"h':"here", \
             '"k':"know", '"l':"lord", '"m':"mother", '"n':"name", \
             '"o':"one", '"p':"part", '"q':"question", '"r':"right", \
             '"s':"some", '"t':"time", '"u':"under", '"w':"work", '"y':"young", \
            '"!':"there", '"*':"character", '"?':"through", \
             '":':"where", '"\\':"ought", "^u":"upon", "^w":"word", \
             "^!":"these", "^?":"those", "^:":"whose", "_c":"cannot", \
             "_h":"had", "_m":"many", "_s":"spirit", "_w":"world", \
             "_!":"their", ".d":"ound", ".e":"ance", ".n":"sion", \
             ".s":"less", ".t":"ount", ";e":"ence", ";g":"ong", \
             ";l":"ful", ";n":"tion", ";s":"ness", ";t":"ment", \
             ";y":"ity", "3":"て", "2":"ふ", "6":"く", "&":"and", \
             "=":"for", "(":"of", "!":"the", ")":"with", \
             "*":"ch", "%":"sh", "?":"th", ":":"wh", "\\":"ou", \
             "/":"st", "<":"gh", "$":"ed", "]":"er", "[":"ow", \
             ">":"ar", "+":"ing", "7":"gg", "5":"en", "9":"in"}

Obnoxious = {"3":"て", "1":"に"}

EndPunc = {"8":"?", "4":".", "0":'ゆ', "に":",", "6":"!", \
           "ふ":";", "て":":", "か":"か", "そ":"そ", "フ":";", \
           "テ":":", "く":"!", "ク":"!", "ニ":","}

EndPuncLine = "840162てかそふテフくクにニœ"

Numbers = {"a":"1", "b":"2", "c":"3", "d":"4", "e":"5", \
           "f":"6", "g":"7", "h":"8", "i":"9", "j":"0", \
           ",":",", ".":".", "4":".", "に":",", "ニ":","}

NumberLine = "abcdefghij,.41にニ"

StartPunc = "よαζθ',あいう"

StartPuncII = "\"([{'あいう"

Alphabet = "abcdefghijklmnopqrstuvwxyzαβγδεζηθικλμνξてふテフくクにニπρστυφχψωえ"

AllTheNumbers = "1234567890"

EnglishAlphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

GreekAlphabet = "αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"

HebrewAlphabet = "אבגדהוזחטיכלמנסעפצקרשת"

CyrillicAlphabet = "абвгдежзиклмнопрстуфхцчшщыэюяАБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"

lower = "abcdefghijklmnopqrstuvwxyz"

UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

RealLetters = "abcdefghijklmnopqrstuvwxyz*%=&!?95+>[]$</\\)(:7"

GreekLetters = {".,a":"Α", ".,b":"Β", ".,g":"Γ", ".,d":"Δ", ".,e":"Ε", ".,z":"Ζ", \
                ".,:":"Η", ".,?":"Θ", ".,i":"Ι", ".,k":"Κ", ".,l":"Λ", ".,m":"Μ", \
                ".,n":"Ν", ".,x":"Ξ", ".,o":"Ο", ".,p":"Π", ".,r":"Ρ", ".,s":"Σ", \
                ".,t":"Τ", ".,u":"Υ", ".,f":"Φ", ".,&":"Χ", ".,y":"Ψ", \
                ".,w":"Ω", ".a":"α", ".b":"β", ".g":"γ", ".d":"δ", ".e":"ε", ".z":"ζ", \
                ".:":"η", ".?":"θ", ".i":"ι", ".k":"κ", ".l":"λ", ".m":"μ", \
                ".n":"ν", ".x":"ξ", ".o":"ο", ".p":"π", ".r":"ρ", ".s":"σ", \
                ".t":"τ", ".u":"υ", ".f":"φ", ".&":"χ", ".y":"ψ", ".w":"ω"}

RomanLetters = {",a":"A", ",b":"B", ",c":"C", ",d":"D", \
                    ",e":"E", ",f":"F", ",g":"G", ",h":"H", \
                    ",i":"I", ",j":"J", ",k":"K", ",l":"L", \
                    ",m":"M", ",n":"N", ",o":"O", ",p":"P", \
                    ",q":"Q", ",r":"R", ",s":"S", ",t":"T", \
                    ",u":"U", ",v":"V", ",w":"W", ",x":"X", \
                    ",y":"Y", ",z":"Z"}

HebrewLetters = {",,a":"א", ",,v":"ב", ",,g":"ג", ",,d":"ד", ",,h":"ה", ",,w":"ו", \
                 ",,z":"ז", ",,x":"ח", ",,t":"ט", ",,j":"י", ",,l":"ל", ",,m":"מ", \
                 ",,n":"נ", ",,s":"ס", ",,f":"פ", ",,q":"ק", ",,r":"ר", \
                 ",,ch":"כ", ",,ed":"ע", ",,the":"צ", ",,wh":"ש", ",,th":"ת"}

HebrewLatex = {"א":"\\aleph ", "ב":"\\bet ", "ג":"\\gimel ", "ד":"\\dalet ", "ה":"\\he ", "ו":"\\vav ", "ז":"\\zayin ", "ח":"\\chet ", "ט":"\\tet ", "י":"\\yod ", "כ":"\\kaf ", "ל":"\\lamed ", "מ":"\\mem ", "נ":"\\nun ", "ס":"\\samekh ", "ע":"\\ayin ", "פ":"\\pe ", "ץ":"\\tsadi ", "ק":"\\qof ", "ר":"\\resh ", "ש":"\\shin ", "ת":"\\tav "}
               
CyrillicLatex = {"А":"\\Cyr{A}", "Б":"\\Cyr{B}", "В":"\\Cyr{V}", "Г":"\\Cyr{G}", \
                "Д":"\\Cyr{D}", "Е":"\\Cyr{E}", "Ж":"\\Cyr{Z1}", "З":"\\Cyr{Z}", \
                "И":"\\Cyr{I}", "К":"\\Cyr{K}", "Л":"\\Cyr{L}", "М":"\\Cyr{M}", \
                "Н":"\\Cyr{N}", "О":"\\Cyr{O}", "П":"\\Cyr{P}", "Р":"\\Cyr{R}", \
                "С":"\\Cyr{S}", "Т":"\\Cyr{T}", "У":"\\Cyr{U}", "Ф":"\\Cyr{F}", \
                 "Х":"\\Cyr{H}", "Ц":"\\Cyr{C}", "Ч":"\\Cyr{Q}", "Ш":"\\Cyr{Sh}", \
                 "Щ":"\\Cyr{Shch}", "Ы":"Y", "Э":"\\Cyr{E1}", "Ю":"\\Cyr{Yu}", \
                 "Я":"\\Cyr{Ya}", "а":"\\Cyr{a}", "б":"\\Cyr{b}", "в":"\\Cyr{v}", \
                 "г":"\\Cyr{g}", "д":"\\Cyr{d}", "е":"\\Cyr{e}", "ж":"\\Cyr{z1}", \
                 "з":"\\Cyr{z}", "и":"\\Cyr{i}", "к":"\\Cyr{k}", "л":"\\Cyr{l}", \
                 "м":"\\Cyr{m}", "н":"\\Cyr{n}", "о":"\\Cyr{o}", "п":"\\Cyr{p}", \
                 "р":"\\Cyr{r}", "с":"\\Cyr{s}", "т":"\\Cyr{t}", "у":"\\Cyr{u}", \
                 "ф":"\\Cyr{f}", "х":"\\Cyr{h}", "ц":"\\Cyr{c}", "ч":"\\Cyr{q}", \
                 "ш":"\\Cyr{sh}", "щ":"\\Cyr{shch}", "ы":"\\Cyr{y}", "э":"\\Cyr{e1}", \
                 "ю":"\\Cyr{yu}", "я":"\\Cyr{ya}"}

CyrillicLetters = {"@@a":"а", "@@b":"б", "@@w":"в", "@@g":"г", "@@d":"д", \
                   "@@e":"е", "@@j":"ж", "@@z":"з", "@@i":"и", "@@k":"к", \
                   "@@l":"л", "@@m":"м", "@@n":"н", "@@o":"о", "@@p":"п", \
                   "@@r":"р", "@@s":"с", "@@t":"т", "@@u":"у", "@@f":"ф", \
                   "@@h":"х", "@@c":"ц", "@@q":"ч", "@@:":"ш", "@@x":"щ", \
                   "@@!":"ы", "@@[":"э", "@@\\":"ю", "@@$":"я", "@@,a":"А", \
                   "@@,b":"Б", "@@,w":"В", "@@,g":"Г", "@@,d":"Д", "@@,e":"Е", \
                   "@@,j":"Ж", "@@,z":"З", "@@,i":"И", "@@,k":"К", "@@,l":"Л", \
                   "@@,m":"М", "@@,n":"Н", "@@,o":"О", "@@,p":"П", "@@,r":"Р", \
                   "@@,s":"С", "@@,t":"Т", "@@,u":"У", "@@,f":"Ф", "@@,h":"Х", \
                   "@@,c":"Ц", "@@,q":"Ч", "@@,:":"Ш", "@@,x":"Щ", "@@,!":"Ы", \
                   "@@,[":"Э", "@@,\\":"Ю", "@@,$":"Я"}
                   
GreekLatex = {"α":"\\alpha ", "β":"\\beta ", "γ":"\\gamma ", \
                "δ":"\\delta ", "ε":"\\epsilon ", "ζ":"\\zeta ", \
                "η":"\\eta ", "θ":"\\theta ", "ι":"\\iota ", \
                "κ":"\\kappa ", "λ":"\\lambda ", "μ":"\\mu ", \
                "ν":"\\nu ", "ξ":"\\xi ", "ο":"o", \
                "π":"\\pi ", "ρ":"\\rho ", "σ":"\\sigma ", \
                "τ":"\\tau ", "υ":"\\upsilon ", "φ":"\\phi", \
                "χ":"\\chi ", "ψ":"\\psi ", "ω":"\\omega ", \
                "Α":"A", "Β":"B", "Γ":"\\Gamma ", \
                "Δ":"\\Delta ", "Ε":"E", "Ζ":"Z", \
                "Η":"H", "Θ":"\\Theta ", "Ι":"I", \
                "Κ":"K", "Λ":"\\Lambda ", "Μ":"M", \
                "Ν":"N", "Ξ":"\\Xi ", "Ο":"O", \
                "Π":"\\Pi ", "Ρ":"P", "Σ":"\\Sigma ", \
                "Τ":"T", "Υ":"\\Upsilon ", "Φ":"\\Phi ", \
                "Χ":"X", "Ψ":"\\Psi ", "Ω":"\\Omega "}

TwoCharTemp = {'"k:':"リ", ".1:":"ル", '"k':"こ", \
               ".1":"さ", "/.k":"し", "$o":"す",  \
               "$3o":"す", "$33o]":"せ", "$33o":"せ", "$[33":"そ", \
               "$[33o":"た", "$[33o]":"た", "@,(":"⇶", "@,)":"⇇", \
               "\\":"ち", ",(":"⚀", ",)":"⚁", "@(":"つ", "@)":"て", "..(":"と", \
               "..)":"な", ".(":"に", ".)":"ぬ", "@h":"ね", \
               ".$":"の", "@d":"は", ",=":"ひ", "@,a":"ふ", \
               "!@$c]":"へ", "_=":"ほ", "$_":"ま", "$p":"み", \
               "@s@s":"む", "_;":"チ", ".;":"ツ", "@*":"め", \
               "'''":"ᛦ", "+-":"も", "-+":"や", "./":"ゆ", "_&":"よ", \
               "@#":"ら", ".#":"り", "__]":"れ", "_]":"る", \
               "_/":"/", "@:":"ろ", "_#":"キ", ".#":"ト", \
               "$[359o]":"メ", "$[359o":"メ", "$935o]":"ム", "$935o":"ム", \
               "$[359]":"ミ", "$[359":"ミ", "$<[33o]":"モ", "$<[33o":"モ", \
               "$<33o]":"マ", "$<33o":"マ", "$%33o]":"ホ", "$%33o":"ホ", \
               "_<":"ピ"}
                   
PutThemBack = {"あ":";", "い":":", "う":".", "え":"!", "お":"?", \
               "!":"\\int ", "&":"!", "*":"\\cdot ", "し":" \\neq ", "さ":" > ", \
               "こ":" < ", "す":"\\to ", "せ":"\\rightarrow ", \
               "そ":"\\leftarrow ", "た":"\\leftrightarrow ", \
               "ち":"|", "つ":"[", "て":"]", "と":"\\langle ", "⚁":"\\bigg)", \
               "な":"\\rangle ", "に":"\\{ ", "ぬ":"\\} ", "⚀":"\\bigg(", \
               "ね":"\\hbar ", "の":"\\nabla ", "は":"\\partial ", \
               "ひ":"\\infty ", "ふ":"\\text{\\AA} ", "へ":"\\oint ", \
               "ほ":"\\propto ", "ま":"\\parallel ", "み":"\\perp ", \
               "む":"\\approx ", "ᚢ":"&", "め":"\\times ", "ᛦ":"\\cdots ", \
               "も":"\\pm ", "や":"\\mp ", "ゆ":"\\div ", "よ":"\\& ", \
               "ら":"*", "り":"\\# ", "る":"\\dagger ", \
               "れ":"\\ddagger ", "ろ":"\\sim ", "ム":"\\rightsquigarrow ", \
               "ミ":"\\leftsquigarrow ", "メ":"\\leftrightsquigarrow",
               "モ":"\\updownarrow ", "マ":"\\uparrow ", "ホ":"\\downarrow ", \
               "リ":"\\leq ", "ル":"\\geq ", "⇶":"\\bigg[", "⇇":"\\bigg]"}

UpperCustom = {"::":"\\Ooverline{", ":":"\\overline{", \
               "た":"\\overleftrightarrow{", "$33o":"\\overrightarrow{", \
               "そ":"\\overleftarrow{", "す":"\\overrightarrow", \
               "ろ":"\\widetilde{", "に":"\\overbrace{", "つ":"\\overbracket{", "ピ":"\\widehat{"}

UpperCustomSingle = {"\\overset{::}{":"\\Ooverline{", "\\overset{:}{":"\\overline{", \
               "\\overset{た}{":"\\overleftrightarrow{", "\\overset{$33o}{":"\\overrightarrow{", \
               "\\overset{そ}{":"\\overleftarrow{", "\\overset{す}{":"\\overrightarrow{", \
               "\\overset{ろ}{":"\\widetilde{", "\\overset{に}{":"\\overbrace{", \
               "\\overset{つ}{":"\\overbracket{", "\\overset{ピ}{":"\\widehat{"}

LowerCustom = {"::":"\\Uunderline{", ":":"\\underline{", \
               "た":"\\underleftrightarrow{", "$33o":"\\underrightarrow{", \
               "そ":"\\underleftarrow{", "す":"\\underrightarrow{", \
               "ぬ":"\\underbrace{", "て":"\\underbracket{", "ろ":"\\undertilde{"}

LowerCustomSingle = {"\\underset{::}{":"\\Uunderline{", "\\underset{:}{":"\\underline{", \
               "\\underset{た}{":"\\underleftrightarrow{", "\\underset{$33o}{":"\\underrightarrow{", \
               "\\underset{そ}{":"\\underleftarrow{", "\\underset{す}{":"\\underrightarrow{", \
               "\\underset{ろ}{":"\\undertilde{", "\\underset{に}{":"\\underbrace{", \
               "\\underset{つ}{":"\\underbracket{"}

# ----------------------------------------------------
# NEMETH BRAILLE FUNCTIONS
# -------------------------------------------------
"""
---------------------------------------------------
This is where we replace single letters using a
Letter Indicator (;) which is exactly the same as
the subscript indicator for some ungodly reason.

The difference is that we will have a space before
a single letter using this so we can check for
that.

We will also replace punctuation using the
punctuation indicator to be replaced later.

This is also where the regular capital letters and
Greek letters are dealt with too.
---------------------------------------------------
"""
def ReplaceSingleLetters(Expression):

    Punctuation = {"2":"あ", "3":"い", "4":"う", "6":"え", "8":"お"}

    Thing = [" ", "%", ">", ",", "."]

    for X in Thing:
        for Letter in lower:
            if(X+";,"+Letter in Expression):
                Expression = Expression.replace(X+";,"+Letter, X+" "+Letter.upper())

            if(X+";"+Letter in Expression):
                Expression = Expression.replace(X+";"+Letter, X+" "+Letter)


    for Letter in lower:
        if(Expression[0:1] == ";" and Expression[1:2] == "," and Expression[2:3] == Letter):
            Expression = Letter.upper() + Expression[3:]
            
        if(Expression[0:1] == ";" and Expression[1:2] == Letter):
            Expression = Expression[1:]
        

    for letter in lower:
        if(",," + letter in Expression):
            Expression = Expression.replace(",,"+letter, "ん"+letter)

    Expression = Expression.replace(",,*", ",,ch")
    Expression = Expression.replace(",,$", ",,ed")
    Expression = Expression.replace(",,!", ",,the")
    Expression = Expression.replace(",,:", ",,wh")
    Expression = Expression.replace(",,?", ",,th")

    for Key in HebrewLetters:
        if(Key in Expression):
            Expression = Expression.replace(Key, HebrewLetters[Key])

    for Key in GreekLetters:
        if(Key in Expression):
            Expression = Expression.replace(Key, GreekLetters[Key])

    for Key in CyrillicLetters:
        if(Key in Expression):
            Expression = Expression.replace(Key, CyrillicLetters[Key])

    for Key in RomanLetters:
        if(Key in Expression):
            Expression = Expression.replace(Key, RomanLetters[Key])

    Expression.replace("_,8","'") # Apostrophe
    Expression.replace("_,0","'")
    Expression.replace("_'","'")

    for Thing in Punctuation: # _ is the punctuation marker
        if("_" + Thing in Expression):
            Expression.replace("_"+Thing, Punctuation[Thing])

    return Expression
# ----------------------------------------------------
"""
------------------------------------------------------
This function is used to truncate symbols which
appear multiple times in a row down to just one of
that symbol.

An example is for complex fractions. You use ? to
open a fraction and ,? to open a complex fraction and
,,? to open a hypercomplex fraction. In print,
however, LaTeX will write fractions within fractions
all the same way, so these symbols can all be replaced
with the regular fraction opener (?).
------------------------------------------------------
"""
def TruncateHigher(Word):

    Truncations = [[",","?","?"], [",","#","#"], [".",">",">"], \
                   [".","]","]"], [".","<","<"], [",","/","/"], \
                   ["<","<","<"], ["%","%","%"]]

    for List in Truncations:
        i = 1
        High = 0

        while(True):
            if(List[0]*i + List[1] in Word):
                High += 1
                i += 1
            else:
                i -= 1
                break

        while(High > 0):
            Word = Word.replace((List[0]*High + List[1]), List[2])
            High -= 1

    return Word
# ----------------------------------------------------
def ReplaceStuff(Word):

    for Key in GreekLatex:
        if(Key in Word):
            Word = Word.replace(Key, GreekLatex[Key])

    for Key in CyrillicLatex:
        if(Key in Word):
            Word = Word.replace(Key, CyrillicLatex[Key])

    return Word
# ----------------------------------------------------
"""
------------------------------------------------------
This is where we replace some of the common symbols
that we didn't replace earlier.
------------------------------------------------------
"""
def ReplaceCharacters(Word, Switch):
    if(Switch):
        for Key in TwoCharTemp:
            if(Key in Word):
                Word = Word.replace(Key, TwoCharTemp[Key])
    else:
        for Key in PutThemBack:
            if(Key in Word):
                Word = Word.replace(Key, PutThemBack[Key])

    return Word
# ----------------------------------------------------
def FindMultiPurpose(Word, LogLine, OriginalExpression):
    if(Word[0:1] == '"'): # First Letter - Definitely a multipurpose
        Word = "⇰" + Word[1:]

    [Word, LogLine] = Ambiguity(Word, '"', "Baseline Indicator/Text", "Multipurpose Indicator", '"', "⇰", LogFile, Read, LogLine, OriginalExpression)
            
    return Word, LogLine
        
# ----------------------------------------------------
def Ambiguity(Word, Sign, One, Two, Mean1, Mean2, LogFile, Read, LogLine, OriginalExpression):
    NewThing = ""

    Ambiguous = {"κ":".k", "こ":'"k', "ゑ":'-"+', "を":'-"-', \
                 "ぷ":'+"+', "ゐ":'+"-', "ヿ":'"k', "⇰":'"', \
                 "↑":"<", "↓":"%", "☜":"]", "➸":",'"}

    for i in range(len(Word)):
        if(Word[i] == Sign):
            if(Read): # We are reading from LogFile                
                for Bit in LogFile:
                    Bit = Bit.strip()
                    Bit = Bit.split(" EQUALS ")
                    NewThing += Bit[0]
                    LogLine += 1
                    break                
            else:
                print("\nThere is a potential ambiguity.")
                print("Does %s mean %s or %s?\n" % (Sign, One, Two))

                Preview = Word[i-5:i] + "  ⥤" + Word[i] + "⥢  " + Word[i+1:i+5]

                Temp = Word[:i] + "  ⥤" + Word[i] + "⥢  " + Word[i+1:]
                Q = ""

                for Key in TwoCharTemp:
                    Temp = Temp.replace(TwoCharTemp[Key], Key)

                for Key in Ambiguous:
                    Temp = Temp.replace(Key, Ambiguous[Key])

                for T in Temp:
                        Q += T + " "
            
                print(Q)
                
                K = input("Press 0 for %s\nPress 1 for %s\n" % (One, Two))

                if(K == "1"):
                    NewThing += Mean2
                    if(Read == False and LogFile != "nothing"): # Creating Log File
                        LogFile.write(Mean2 + " EQUALS " + Preview +"\n")
                        
                else:
                    NewThing += Mean1
                    if(Read == False and LogFile != "nothing"): # Creating Log File
                        LogFile.write(Mean1 + " EQUALS " + Preview +"\n")
                        
        else:
            NewThing += Word[i]

    return NewThing, LogLine
# ----------------------------------------------------
"""
------------------------------------------------------
This is where we handle MultiPurpose Expressions. They
are really annoying and this function took like three
days to write oh my god.
------------------------------------------------------
"""
def MakeMultiPurpose(Word):
    Boo = []
    Level = -1
    StartLevel = 0

    Phrase = ""
    Previous = ""
    NonPhrase = False

    for Letter in Word:
        if(Letter == "⇰"):
            if(NonPhrase): # Previous Thing Not An MP
                if(Phrase != ""):
                    Boo.append([Phrase, -1])
                    NonPhrase = False
                    Phrase = ""
            else:
                if(Phrase != ""):
                    if(Previous == "↑" or Previous == "↓"):
                        Phrase = Phrase[:-1]
                        
                    Boo.append([Phrase, Level])

                    if(Previous == "↑" or Previous == "↓"):
                        Phrase = Previous
                    else:
                        Phrase = ""

            Level += 1
            StartLevel = Level
            Boo.append([Letter, Level])
            
        elif(Letter == "☜"):
            Phrase += Letter
            Level -= 1
        else:
            if(Previous == "☜"): # Not Part Of Thing
                Boo.append([Phrase, StartLevel])
                Phrase = ""
                NonPhrase = True
                StartLevel -= 1
                Phrase += Letter
            else:
                Phrase += Letter

        Previous = Letter

    if("☜" in Phrase):
        Boo.append([Phrase, StartLevel])
        
    Temp = []

    for Entry in Boo:
        if(Entry[0] != "⇰"):
            Temp.append(Entry)

    Boo = Temp

    List = []
    
    PhraseNum = -1
    
    MainExp = ""
    Upper = ""
    Lower = ""

    Up = False
    Down = False

    BigTemp = []
    Temp = []

    if(len(Boo) > 1): # If the list is > 1, then we always will move the first to the end
        if(len(Boo) == 2): # Only Two Entries
            Order = [1,0]
            Boo = [Boo[i] for i in Order]
        else: # More than three entries, need to swap stuff
            Temp = []
            
            Count = -1
            for i in range(len(Boo)): # Keep the things with consecutive levels together
                Entry = Boo[i]
                if(Entry[1] != Count + 1):
                        BigTemp.append(Temp)
                        Temp = []
                        Temp.append(Entry)
                        Count = Entry[1]
                else: # Entry is equal
                    Temp.append(Entry)

            BigTemp.append(Temp)

            for i in range(len(BigTemp)):
                BigList = BigTemp[i]
                SmallTemp = []
                
                for j in range(len(BigList)-1, -1, -1):
                    SmallTemp.append(BigList[j])

                BigTemp[i] = SmallTemp

            if(len(BigTemp) == 1): # One Thing - already finished
                Boo = BigTemp
            elif(len(BigTemp) == 2): # Two Groups - switch the two things
                Order = [1,0]
                BigTemp = [BigTemp[i] for i in Order]
            else:
                Order = [0]*len(BigTemp)
                for i in range(len(BigTemp)):
                    if(i == 0):
                        Order[i] = len(BigTemp)-1
                    else:
                        Order[i] = i-1

                BigTemp = [BigTemp[i] for i in Order]

            Boo = []
            for i in range(len(BigTemp)):
                for j in range(len(BigTemp[i])):
                    Boo.append(BigTemp[i][j])
 
    for Piece in Boo:
        List.append([0, "", [""], [""]]) # Main, Up, Down
        PhraseNum += 1

        List[PhraseNum][0] = Piece[1]

        if(Piece[1] < 0):
            List[PhraseNum][1] = Piece[0]
            continue

        for X in range(len(Piece[0])):
            Letter = Piece[0][X]            

            if((X == 0 and Letter == "↑")):
               if(Piece[0].count("↑") > 1):
                   continue

            if((X == 0 and Letter == "↓")):
               if(Piece[0].count("↓") > 1):
                    continue
            
            if(Up):
                if(Letter == "↑"): # Going Up Again
                    List[PhraseNum][2].append(Upper) # Add New Upper Exp
                    Upper = "" # Reset Upper
                    continue
                if(Letter == "↓"): # Changing Direction
                    List[PhraseNum][2].append(Upper)
                    Upper = ""
                    Up = False
                    Down = True
                    continue
                elif(Letter == "☜" or X == len(Piece[0])-1):
                    if(X == len(Piece[0])-1 and not Letter == "☜"):
                        Upper += Letter
                    List[PhraseNum][2].append(Upper)
                    Lower = ""
                    Upper = ""
                    MainExp = ""
                    Down = False
                    Up = False
                    break
                else:
                    Upper += Letter
                    continue
    
            if(Down):
                if(Letter == "↓"): # Going Down Again
                    List[PhraseNum][3].append(Lower) # Add New Upper Exp
                    Lower = "" # Reset Lower
                    continue
                elif(Letter == "↑"): # Changing Direction
                    List[PhraseNum][3].append(Lower)
                    Lower = ""
                    Down = False
                    Up = True
                    continue
                elif(Letter == "☜" or X == len(Piece[0])-1):
                    if(X == len(Piece[0])-1 and not Letter == "☜"):
                        Lower += Letter
                    List[PhraseNum][3].append(Lower)
                    Lower = ""
                    Upper = ""
                    MainExp = ""
                    Down = False
                    Up = False
                    break
                else:
                    Lower += Letter
                    continue
                    
            if(Letter == "↑"):
                List[PhraseNum][1] = MainExp # Put Main Expression In
                MainExp = ""
                Up = True # Filling Upper Phrase
            elif(Letter == "↓"):
                List[PhraseNum][1] = MainExp # Put Main Expression In
                MainExp = ""
                Down = True # Filling Upper Phrase
            else:
                MainExp += Letter

    NewThing = ""

    for i in range(len(List)):
        PhraseList = List[i]
        LowerItems = PhraseList[3]
        UpperItems = PhraseList[2]
        MainPhrase = PhraseList[1]
        Level = PhraseList[0]

        Temp = []

        for Boop in LowerItems:
            if(Boop == ''): #Empty
                continue
            else:
                Temp.append(Boop)

        LowerItems = Temp

        Temp = []

        for Boop in UpperItems:
            if(Boop == ''): #Empty
                continue
            else:
                Temp.append(Boop)

        UpperItems = Temp

        if(Level < 0): # Phrase Not MP Expression
            NewThing += " " + MainPhrase + " "
            continue

        UpperLevel = 0
        LowerLevel = 0

        UpperLevel += Boo[i][0].count("↑")
        LowerLevel += Boo[i][0].count("↓")

        UT = []
        LT = []
        AVariable = 0
        UseNext = False
        BEEP = False
        Temp = ""

        for Entry in UpperItems[::-1]:
            if(UseNext):
                Temp += Entry + "}"
                UT.append(Temp)
                Temp += ""
                UpperLevel -= 1
                UseNext = False
                continue
            
            if(len(UpperItems) > 1): # Not single Item
                if(AVariable != len(UpperItems)-1): # Not last item
                    for Key in UpperCustom:
                        if(Entry == Key):
                            Temp += UpperCustom[Key]
                            BEEP = True
                            UseNext = True
                            break

                    if(BEEP):
                        BEEP = False
                    else:
                        UT.append(Entry)
                        
                else: # Last Item in UpperItems
                    for Key in UpperCustom:
                        if(Entry == Key):
                            if(len(LowerItems) == 0):
                                MainPhrase = UpperCustom[Key] + MainPhrase
                                BEEP = True
                                UpperLevel -= 1
                                break
                            else:
                                UpperLevel -= 1
                                UT.append(UpperCustom[Key] + "ゟ")
                                BEEP = True
                        
                    if(BEEP):
                        BEEP = False
                    else:
                        UT.append(Entry)
                        
            else:
                UT.append(Entry)


            AVariable += 1

        AVariable = 0
        UseNext = False
        BEEP = False
        Temp = ""

        for Entry in LowerItems[::-1]:
            if(UseNext):
                Temp += Entry + "}"
                LT.append(Temp)
                Temp += ""
                UseNext = False
                LowerLevel -= 1
                continue
            
            if(len(LowerItems) > 1): # Not single Item
                if(AVariable != len(LowerItems)-1): # Not last item
                    for Key in LowerCustom:
                        if(Entry == Key):
                            Temp += LowerCustom[Key]
                            UseNext = True
                            BEEP = True
                            break

                    if(BEEP):
                        BEEP = False
                    else:
                        LT.append(Entry)
                    
                else: # Lats Item
                    for Key in LowerCustom:
                        if(Entry == Key):
                            MainPhrase = LowerCustom[Key] + MainPhrase
                            UseNext = True
                            BEEP = True
                            LowerLevel -= 1
                            break
                        
                    if(BEEP):
                        BEEP = False
                    else:
                        LT.append(Entry)

            else:
                LT.append(Entry)


            AVariable += 1

        LowerItems = LT[::-1]
        UpperItems = UT[::-1]

        LenUp = len(UpperItems)
        LenLow = len(LowerItems)

        if(LenUp % 2 != 0):
            LenUp += 1

        if(LenLow % 2 != 0):
            LenLow += 1

        LL = LenLow
        UU = LenUp

        for D in range(UpperLevel):
            NewThing += "\\overset{"

        iiiii = 0
        for BeepBoopBop in UpperItems: # Close any open brackets in upper items
            while(BeepBoopBop.count("{") > BeepBoopBop.count("}")):
                BeepBoopBop += "}"

            UpperItems[iiiii] = BeepBoopBop

            iiiii += 1

        iiiii = 0
        for BeepBoopBop in LowerItems: # Close any open brackets in lower items
            while(BeepBoopBop.count("{") > BeepBoopBop.count("}")):
                BeepBoopBop += "}"

            LowerItems[iiiii] = BeepBoopBop

            iiiii += 1
                
        if(UpperLevel > 0): # If there are upper items at all
            if(len(UpperItems) == 1): # Single Thing
                if(len(LowerItems) == 0): # No Lower Items
                    NewThing += UpperItems[0] + "}{" + MainPhrase
                    if(MainPhrase != ""):
                        NewThing += "}"
                        if(Level > 1):
                            NewThing += "}{"

                        if("☜" not in Boo[i][0]):
                            NewThing += "}"
                else:
                    NewThing += UpperItems[0] + "}{"
                    
            else:
                for Thing in UpperItems[::-1]:
                    if((len(UpperItems) % 2 == 0 and LenUp == 1) or (len(UpperItems) % 2 != 0 and LenUp == 2)): # Last Item
                        if(MainPhrase != ""):
                            if(len(LowerItems) == 0):
                                NewThing += MainPhrase + "}"
                            else:
                                if("ゟ" not in Thing):
                                    NewThing += Thing + "}}{"
                                else:
                                    NewThing += Thing
                        break
                                
                    if(LenUp > 1):
                        if(LenUp % 2 == 0):
                            if(LenUp == UU): # First Item
                                NewThing += Thing + "}{"
                            else:
                                NewThing += Thing + "}}{"
                                
                        else:
                            NewThing += Thing + "}}{"
                    LenUp -= 1

        for D in range(LowerLevel):
            NewThing += "\\underset{"

        if(LowerLevel > 0): # If there are upper items at all
            if(len(LowerItems) == 1): # Single Thing
                NewThing += LowerItems[0] + "}{" + MainPhrase
                if(MainPhrase != ""):
                    NewThing += "}"
                    if(Level > 1):
                        NewThing += "}{"

                    if("☜" not in Boo[i][0]):
                        NewThing += "}"
                    
            else:
                for Thing in LowerItems[::-1]:
                    if((len(LowerItems) % 2 == 0 and LenLow == 1) or (len(LowerItems) % 2 != 0 and LenLow == 2)): # Last Item
                        NewThing += Thing + "}}{" + MainPhrase
                        break
                                
                    if(LenLow > 1):
                        if(LenLow % 2 == 0):
                            if(LenLow == LL): # First Thing
                                NewThing += Thing + "}{"
                            else:
                                NewThing += Thing + "}}{"
                        else:
                            NewThing += Thing + "}}{"

                    LenLow -= 1
        
    while(NewThing.count("{") > NewThing.count("}")):
        NewThing += "}"

    for Key in UpperCustomSingle:
        NewThing = NewThing.replace(Key, UpperCustomSingle[Key])

    for Key in LowerCustomSingle:
        NewThing = NewThing.replace(Key, LowerCustomSingle[Key])

    NewThing = NewThing.replace("☜","")
    NewThing = NewThing.replace("ゟ","")

    return NewThing
# ----------------------------------------------------
def FindMoreMultiPurpose(Expression):

    MPSymbols = ["す", "::", ":", "$33o", "た", "そ", "ろ", "に", "つ", "ピ"]

    for Symbol in MPSymbols:
        for Letter in EnglishAlphabet:
            Expression = Expression.replace('"' + Letter + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('",' + Letter + "<" + Symbol + "]", "⇰," + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")
            Expression = Expression.replace('",' + Letter + "%" + Symbol + "]", "⇰," + Letter + "↓" + Symbol + "☜")

            for Number in AllTheNumbers:
                Expression = Expression.replace('"' + Letter + Number + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
                Expression = Expression.replace('"' + Letter + Number + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")

            Expression = Expression.replace('"' + Letter + "'" + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "''" + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "'" + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "''" + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")
            
        for Letter in GreekAlphabet:
            Expression = Expression.replace('"' + Letter + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")

            for Number in AllTheNumbers:
                Expression = Expression.replace('"' + Letter + Number + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
                Expression = Expression.replace('"' + Letter + Number + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")

            Expression = Expression.replace('"' + Letter + "'" + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "''" + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "'" + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "''" + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")
            
        for Letter in HebrewAlphabet:
            Expression = Expression.replace('"' + Letter + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")

            for Number in AllTheNumbers:
                Expression = Expression.replace('"' + Letter + Number + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
                Expression = Expression.replace('"' + Letter + Number + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")

            Expression = Expression.replace('"' + Letter + "'" + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "''" + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "'" + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "''" + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")
            
        for Letter in CyrillicAlphabet:
            Expression = Expression.replace('"' + Letter + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")

            for Number in AllTheNumbers:
                Expression = Expression.replace('"' + Letter + Number + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
                Expression = Expression.replace('"' + Letter + Number + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")

            Expression = Expression.replace('"' + Letter + "'" + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "''" + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "'" + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "''" + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")

        for Letter in AllTheNumbers:
            Expression = Expression.replace('"' + Letter + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")

            for Number in AllTheNumbers:
                Expression = Expression.replace('"' + Letter + Number + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
                Expression = Expression.replace('"' + Letter + Number + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")

            Expression = Expression.replace('"' + Letter + "'" + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "''" + "<" + Symbol + "]", "⇰" + Letter + "↑" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "'" + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")
            Expression = Expression.replace('"' + Letter + "''" + "%" + Symbol + "]", "⇰" + Letter + "↓" + Symbol + "☜")

    return Expression

# ----------------------------------------------------
"""
------------------------------------------------------
This is where Math Mode will be handled. There are two
pieces of this function. The first is the part which
will handle the setting up of Math Mode.

If the Nemeth Starter is on its own line, then we will
format it as an equation. If not, then we will format
it as an in-line equation using $$.
------------------------------------------------------
"""
def DoNemeth(HasEquals, Line, LATEX, New, Skip, Verbose, LogFile, Read, LogLine):

    Settings = open(os.getcwd() + "/Latex Settings.txt", "r")

    # Flags = four elements
    # 0 = use title flag
    # 1 = title marker (string)
    # 2 = how many lines
    # 3 = auto first line title
    List = [] 

    for FLOBBLE in Settings:
        FLOBBLE = FLOBBLE.strip()

        if("#" in FLOBBLE or FLOBBLE == ""):
            continue
        else:
            FLOBBLE = FLOBBLE.split(" = ")
            if(FLOBBLE[1] == "True"):
                List.append(True)
            elif(Line[1] == "False"):
                List.append(False)
            else:
                List.append(FLOBBLE[1])

    # 5 = Matrix Start
    # 6 = Matrix End
    # 7 = Matrix NewLine
    # 8 = Matrix Space
    # 9 = Case Start
    # 10 = Case End
    # 11 = Case Newline
    # 12 = Case Space
    # 13 = Determinant Begin
    # 14 = Determinant End

    Word = ""

    Equation = False
    InLine = True

    if(Line[0] == "_%" and Line[len(Line)-1]) == "_:":
        # Stand-alone equation
        Word += "\n\\Equ{"
        Equation = True
        InLine = False
    else:
        Word += "$"
        
    Start = False
    End = False
    X = 0

    Expression = ""
    After = ""

    EndPunc = {"1":",", "4":".", "2":";", "3":":", "6":"!", "8":"?", \
               '">':")", ".>":"\}", ",>":"]", "'":"'"}

    PhraseNum = Line.count("_%")

    AmountOfLinesToSkipNoOtherVariableIsNamedThis = 0

    for Thing in Line:
        if("_%" in Thing):
            Before = Thing.replace("_%","")

            for Key in TwoCharSymb:                
                 if(Key in Before):
                     Before = Before.replace(Key, TwoCharSymb[Key])
                 
            if(Skip > AmountOfLinesToSkipNoOtherVariableIsNamedThis):
                AmountOfLinesToSkipNoOtherVariableIsNamedThis += 1
                continue
            else:
                Start = True
                AmountOfLinesToSkipNoOtherVariableIsNamedThis += 1
                continue

        if(Start):
            X += 1

        if(Start):
            if("_:" in Thing):
                Start = False
                After = Thing.replace("_:","")
                
                for Key in EndPunc:
                    if(Key in After):
                        After = After.replace(Key, EndPunc[Key])
                    
                break

        if(Start):
            Expression += Thing + " "

# ----------------------------------------------------
# MATH BRAILLE TIME

    A = 0
    B = 0
    C = 0
    D = False
    E = False
    
    Text = False # Text Mode Flag
    Fraction = 0
    Radical = False
    SubSuper = False
    Space = False
    Matrix = False
    Cases = False

    NumberSub = False
    
    MultiPurpose = False
    Modifying = False

    Bold = 0
    Italics = 0
    
    Ignore = 0
    MainExp = ""
    
    TextString = ""
    NewExp = ""

    CurrentLevelString = ""
    LevelString = ""

    Previous = ""

    RadicalIndex = ""

    Level = 0

    OriginalExpression = Expression

    NoMPAtAll = False
    NoBLAtAll = False

    Expression = Expression.replace(List[4], "ᛞ") # Begin Matrix
    Expression = Expression.replace(List[5], "ᛝ") # End Matrix
    Expression = Expression.replace(List[6], "ᛒ") # NewLine
    Expression = Expression.replace(List[7], "ᛔ") # Spacing

    Expression = Expression.replace(List[8], "ᚵ") # Begin Cases
    Expression = Expression.replace(List[9], "ᚴ") # End Cases

    Expression = Expression.replace(List[10], "ᛪ") # Begin Determinant
    Expression = Expression.replace(List[11], "ᛝ") # End Determinant

    Expression = Expression.replace('"k:',"リ")

    Expression = Expression.replace('"k',"こ")

    if('こ' in Expression):
        [Expression, LogLine] = Ambiguity(Expression, 'こ', "Less Than Sign", "Something Else", "こ", 'ヿ', LogFile, Read, LogLine, OriginalExpression)

    Expression = ReplaceCharacters(Expression, True)
    
    Expression = ReplaceSingleLetters(Expression)

    Expression = Expression.replace("ヿ",'"k')

    Expression = Expression.replace('-"+', "ゑ")
    Expression = Expression.replace('-"-', "を")
    Expression = Expression.replace('+"-', "ゐ")
    Expression = Expression.replace('+"+', "ぷ")

    if("ゑ" in Expression):
        [Expression, LogLine] = Ambiguity(Expression, "ゑ", "Minus Sign, Baseline, Plus Sign", "Minus and Plus Sign", 'ゑ', "-+", LogFile, Read, LogLine, OriginalExpression)

    if("を" in Expression):
        [Expression, LogLine] = Ambiguity(Expression, "を", "Minus Sign, Baseline, Minus Sign", "Two Minus Signs", 'を', "--", LogFile, Read, LogLine, OriginalExpression)

    if("ゐ" in Expression):
        [Expression, LogLine] = Ambiguity(Expression, "ゐ", "Plus Sign, Baseline, Minus Sign", "Plus and Minus Sign", 'ゐ', "+-", LogFile, Read, LogLine, OriginalExpression)

    if("ぷ" in Expression):
        [Expression, LogLine] = Ambiguity(Expression, "ぷ", "Plus Sign, Baseline, Plus Sign", "Two Plus Signs", 'ぷ', "++", LogFile, Read, LogLine, OriginalExpression)

    if("%" not in Expression and "<" not in Expression): # " always baseline never MP
        NoMPAtAll = True

    if(not NoMPAtAll):
        Expression = FindMoreMultiPurpose(Expression)

    if(not NoMPAtAll):
        Expression = Expression.replace('""', '"⇰')
        Expression = Expression.replace('"Σ%', "⇰Σ%")
        Expression = Expression.replace('"Σ<', "⇰Σ↑")
        Expression = Expression.replace('"Π%', "⇰Π%")
        Expression = Expression.replace('"Π<', "⇰Π↑")
        Expression = Expression.replace('"!%', "⇰!%")
        Expression = Expression.replace('"!<', "⇰!↑")
        Expression = Expression.replace('"lim%', "⇰lim%")

        Expression = Expression.replace("%", "↓")
        Expression = Expression.replace("]","☜")

        if(">" in Expression and "<" in Expression): # Could Have Radicals
            [Expression, LogLine] = Ambiguity(Expression, "<", "Radical Index/Text", "Multipurpose Upwards Indicator", "<", "↑", LogFile, Read, LogLine, OriginalExpression)
        
        else: # No radicals, all < are up
            Expression = Expression.replace("<","↑")

    if("^" in Expression or ";" in Expression):        
        if(not NoMPAtAll): # If we have not concluded that there are no MP indicators
            Expression = Expression.replace(';"',";⇰")
            Expression = Expression.replace('^"',"^⇰")
            [Expression, LogLine] = FindMultiPurpose(Expression, LogLine, OriginalExpression)

    else: # No BL at all, all " are MP
        Expression = Expression.replace('"',"⇰")

    Expression = Expression.replace("ゑ", '-"+')
    Expression = Expression.replace("を", '-"-')
    Expression = Expression.replace("ゐ", '+"-')
    Expression = Expression.replace("ぷ", '+"+')

    Expression = TruncateHigher(Expression)

    Expression = Expression.replace(",'","➸") # Text Mode Indicator

    Expression = Expression.replace("ちEqu{","\\Equ")

    Expression = Expression.replace("]","☜")
    Expression = Expression.replace("%", "↓")

    NumberListThingForgotToDefineIt = "1234567890,."

    if("κ" in Expression):
        if(HasEquals):
            Expression = Expression.replace("κ", " ⇋ ")
        else:
            [Expression, LogLine] = Ambiguity(Expression, "κ", "=", "κ", " ⇋ ", "\\kappa ", LogFile, Read, LogLine, OriginalExpression)

    for Part in Expression:
        
        if(Bold == 1): # Single Symbol Bold
            NewExp += Part + "}"
            Bold = 0
            Previous = Part
            continue

        if(Italics == 1):
            NewExp += Part + "}"
            Italics = 0
            Previous = Part
            continue

        if(Bold == 2): # Bold Number
            if(Part not in NumberListThingForgotToDefineIt):
                NewExp += "}" + Part
                Bold = 0
                Previous = Part
                continue

        if(Italics == 2): # Italics Number
            if(Part not in NumberListThingForgotToDefineIt):
                NewExp += "}" + Part
                Italics = 0
                Previous = Part
                continue

        NumberPunc = ",.^;"

        if(NumberSub):
            if(Part in AllTheNumbers or Part in NumberPunc): # Don't Close
                if(Part == "^"):
                    NewExp += "}^{"
                    NumberSub = False
                    Previous = Part
                    continue
                elif(Part == ";"):
                    NewExp += "}_{"
                    NumberSub = False
                    Previous = Part
                    continue
                else:
                    NewExp += Part
                    Previous = Part
                    continue

            else: # Do Close
                NumberSub = False
                NewExp += "}"
                Level -= 1

        if(Radical):
            if(Part == ">"):
                NewExp += "]{"
                Previous = Part
                Radical = False
                continue
            
        if(MultiPurpose):
            if(Part == "⇰"): # New Multi
                Ignore += 1
                NewExp += Part
                Previous = Part
                continue

            elif(Part == "☜"): # Terminator
                if(Ignore > 0):
                    Ignore -= 1
                    NewExp += Part
                    Previous = Part
                    continue
                else:
                    NewExp += Part
                    MainExp = NewExp.replace(MainExp, "")
                    MultiPurpose = False
                    CurrentLevelString = ""
                    LevelString = ""
                    Level = 0
                    NewExp = NewExp.replace(MainExp, MakeMultiPurpose(MainExp))
                    NumberSub = False
                    Previous = Part
                    continue

        if(Text):
            if(Part == " "):
                TextString = TextString.replace("ち","\\")
                TextString = TextString.replace("↓","%")
                TextString = TextString.replace("↑", "<")
                TextString = TextString.replace("⇰", '"')
                TextString = TextString.replace("☜","]")

                for Key in HebrewLetters:
                    if(HebrewLetters[Key] in TextString):
                        TextString = TextString.replace(HebrewLetters[Key], Key)

                [TextString, A, B, C, D, E, LATEX] = TextMode(TextString, 0, 0, 0, False, False, LATEX)
                NewExp += TextString + " } "
                TextString = ""
                Text = False
                Previous = Part
                continue
            else:
                TextString += Part
                Previous = Part
                continue
    
        # ----------------------------      

        if(Space):
            if(Part == "^"):
                Space = False
                Previous = Part
                continue
            elif(Part == ";"):
                Space = False
                Previous = Part
                continue
            else: # Break levels
                LevelString = ""
                CurrentLevelString = ""
                
                while(Level > 0):
                    NewExp += "}"
                    Level -= 1
                    
                Space = False

        if(Cases):
            if(Part == "ᚴ"): # End Cases
                NewExp += "}"
                Previous += Part
                Cases = False
                continue
            elif(Part == "ᛔ"): # Next Element
                NewExp += " ᚢ "
                Previous = Part
                continue

            elif(Part == "ᛒ"): # New Line
                NewExp += " \\\\ "
                Previous = Part
                continue 

        if(SubSuper): # Non-baseline level
            if(Part == "^" or Part == ";"):
                LevelString += Part
                Previous = Part
                continue
            
            else:
                if(CurrentLevelString == ""): # First Level
                    if(LevelString == "^"):
                        NewExp += "^{"
                        Level += 1
                        
                    if(LevelString == ";"):
                        NewExp += "_{"
                        Level += 1

                elif(LevelString == CurrentLevelString): # Exact Same = Continuation
                    CurrentLevelString = LevelString
                    LevelString = ""
                    SubSuper = False
                    NewExp += Part

                elif(len(LevelString) > len(CurrentLevelString)): # Raise Level or Switch
                    if("^" in LevelString and not ";" in LevelString): # Raise Super
                        NewExp += "^{"
                        Level += 1

                    elif(";" in LevelString and not "^" in LevelString): # Raise Sub
                        NewExp += "_{"
                        Level += 1
                        
                    elif(LevelString[-1] == CurrentLevelString[-1]): # Level NoSwitch No{}
                        if(LevelString[-1] == "^"):
                            NewExp += "^{"
                        else:
                            NewExp += "_{"

                        Level += 1
                    else: #(LevelString[-1] != CurrentLevelString[-1]): # NoLevel Switch {}
                        if(LevelString[-1] == "^"):
                            NewExp += "^{"
                        else:
                            NewExp += "_{"

                        Level += 1

                elif(len(LevelString) < len(CurrentLevelString)): # Lower Level or Switch
                    if("^" in LevelString and not ";" in LevelString): # Lower Super
                        NewExp += "} "
                        Level -= 1

                    elif(";" in LevelString and not "^" in LevelString): # Lower Sub
                        NewExp += "} "
                        Level -= 1
                        
                    elif(LevelString[-1] == CurrentLevelString[-1]): # DownLevel Switch {}
                        NewExp += "}"
                        if(LevelString[-1] == "^"):
                            NewExp += "}^{"
                            Level -= 1
                        else:
                            NewExp += "}_{"
                            Level -= 1
                        
                    else: #(LevelString[-1] != CurrentLevelString[-1]): # DownLevel Switch {}
                        L = Level
                        while(Level > L - (len(CurrentLevelString)-len(LevelString))):
                            NewExp += "}"
                            Level -= 1

                        if(LevelString[-1] == "^"):
                            NewExp += "}^{"
                        else:
                            NewExp += "}_{"

                else: # Current Level and New Level are the same length but not equal verbatim
                    if(LevelString[-1] == "^"):
                        NewExp += "}^{"
                    else:
                        NewExp += "}_{"

                CurrentLevelString = LevelString
                LevelString = ""
                SubSuper = False

        if(Matrix):
            if(Part == "ᛝ"):
                NewExp += "}"
                Matrix = False                
                Previous = Part
                continue

            elif(Part == "ᛔ"): # Next Element
                NewExp += " ᚢ "
                Previous = Part
                continue

            elif(Part == "ᛒ"): # New Line
                NewExp += " \\\\ "
                Previous = Part
                continue

        # ----------------------------

        if(Part == "➸"):
            Text = True
            NewExp += " \\text{ "
            Previous = Part
            continue

        elif(Part == "⇰"):
            MultiPurpose = True
            MainExp = NewExp
            NewExp += Part
            Previous  = Part
            continue

        elif(Part == "キ"):
            Bold = 2
            Previous = Part
            continue

        elif(Part == "ト"):
            Italics = 2
            Previous = Part
            continue

        elif(Part == "ᛞ"): # Begin Matrix
            NewExp += "\\M{"
            Matrix = True
            Previous = Part
            continue

        elif(Part == "ᛪ"): # Begin Determinant
            NewExp += "\\Det{"
            Matrix = True
            Previous = Part
            continue

        elif(Part == "ᚵ"): # Begin Cases
            NewExp += "\\Cases{"
            Cases = True
            Previous = Part
            continue

        elif(Part == "ツ"): # Italic Single Letter
            NewExp += "\\mathit{"
            Italics = 1
            Previous = Part
            continue

        elif(Part == "チ"): # Bold Single Letter
            NewExp += "\\mathbf{"
            Bold = 1
            Previous = Part
            continue

        elif(Part in AllTheNumbers):
            if(Previous in EnglishAlphabet or Previous in GreekAlphabet or Previous in HebrewAlphabet or Previous in CyrillicAlphabet or Previous == "'"):
                if(Previous == ""):
                    NewExp += Part
                else:
                    NewExp += "_{" + Part
                    Level += 1
                    NumberSub = True

                Previous = Part
                continue
            else:
                NewExp += Part
                Previous = Part
                continue

        elif(Part == '"'): # Baseline Indicator
            while(Level > 0):
                NewExp += "}"
                Level -= 1

            LevelString = ""
            CurrentLevelString = ""
            Previous = Part
            continue

        elif(Part == '⇰'): # Multi-Purpose Indicator
            MultiPurpose = True
            MultiExp = NewExp
            Previous = Part
            continue

        elif(Part == "?"):
            NewExp += "\\frac{"
            Fraction += 1
            Previous = Part
            continue
        
        elif(Part == "/"):
            NewExp += "}{"
            Previous = Part
            continue
            
        elif(Part == "#"):
            if(Fraction > 0):
                NewExp += "}"
                Fraction -= 1
                Previous = Part
                continue

    # -------------------------

        elif(Part == "<"):
            Radical = True
            NewExp += "\\sqrt["
            Previous = Part
            continue

        elif(Part == ">"):
            NewExp += "\\sqrt{"
            Previous = Part
            continue

        elif(Part == "☜"):
            while(Level > 0):
                NewExp += "}"
                Level -= 1
                
            NewExp += "}"
            Previous = Part
            continue
            
    
    # -------------------------

        elif(Part == "^"):
            SubSuper = True
            LevelString += Part
            Previous = Part
            continue

        elif(Part == ";"):
            SubSuper = True
            LevelString += Part
            Previous = Part
            continue

        elif(Part == " "):
            Space = True
            NewExp += " "
            Previous = Part
            continue

        else:
            NewExp += Part
            Previous = Part
            continue

    # -------------------------

    while(NewExp.count("{") > NewExp.count("}")):
        NewExp += "}"

    NewExp = ReplaceStuff(NewExp)

    NewExp = ReplaceCharacters(NewExp, False)

    NewExp = NewExp.replace("⇰", "")

    NewExp = NewExp.replace("{lim}", "{\\lim}")
    NewExp = NewExp.replace("{\Sigma }", "{\\sum}")
    NewExp = NewExp.replace("{\Pi }", "{\\prod}")
    NewExp = NewExp.replace("arcsin", "\\arcsin")
    NewExp = NewExp.replace("arccos", "\\arccos")
    NewExp = NewExp.replace("arctan", "\\arctan")
    NewExp = NewExp.replace("arccot", "\\arccot")
    NewExp = NewExp.replace("arcsec", "\\arcsec")
    NewExp = NewExp.replace("arccsc", "\\arccsc")
    NewExp = NewExp.replace("ln(", "\\ln(")
    NewExp = NewExp.replace("sin", "\\sin")
    NewExp = NewExp.replace("cos", "\\cos")
    NewExp = NewExp.replace("tan", "\\tan")
    NewExp = NewExp.replace("cot", "\\cot")
    NewExp = NewExp.replace("sec", "\\sec")
    NewExp = NewExp.replace("csc", "\\csc")

    NewExp = NewExp.replace("⇋", "=")

    Ending = ""

    if(Equation):
        Ending = "}"
    else:
        Ending = "$"

    if(Before != "" and After != ""):
        Word = Before + Word + NewExp + Ending + After
    elif(Before != "" and After == ""):
        Word = Before + Word + NewExp + Ending
    elif(Before == "" and After != ""):
        Word = Word + NewExp + Ending + After
    else:
        Word = Word + NewExp + Ending

    while(Word.count("{") > Word.count("}")):
        Word += "}"

    if(Verbose):
        print(Word)

    New.write(Word+" ")
    
    return X, AmountOfLinesToSkipNoOtherVariableIsNamedThis, LogLine

# ----------------------------------------------------
# LITERARY BRAILLE FUNCTIONS
# ----------------------------------------------------
"""
------------------------------------------------------
This is where we substitute all of the groupsigns like
'ch' and 'for' and stuff.

All we need to do here is replace the things in the
Braille word with the corresponding print letters.
------------------------------------------------------
"""
def WordGroupsigns(Word):

    EndSignsList = [";e", ";g", ";l", ";n", ";s", ";t", ";y"]

    WordList = Word.split("-") # Pieces of Hyphens separate words
    NewWord = ""

    for Word in WordList:
        for Key in MoreWords:
            if(Key in Word):
                if(Key in EndSignsList):
                    for i in range(len(Word)):
                        if(Word[i] == ";"):
                            if(Word[i-1:i] in RealLetters and Word[0] != ";"):
                                Word = Word.replace(Key, MoreWords[Key])
                else:
                    Word = Word.replace(Key, MoreWords[Key])

        NewWord += Word + "-"

    NewWord = NewWord[:-1]

    return NewWord
# ----------------------------------------------------
"""
------------------------------------------------------
This is where we deal with single wordsigns in words
that are hyphenated.

If there is no hyphen in the word, then we leave.

If there is, then first we split it up by the Hyphens.

Then we loop through the pieces and create a version
of the piece with no other punctuation.

We compare this version to all the keys in the Single
Wordsign dictionary and if it is identical to any of
them, then we replace the piece with the proper
translation.

Then we merge all of the pieces and hyphens together
again with the proper punctuation.

This is called before any capitalisation or end
punctuation functions are called.
------------------------------------------------------
"""
def HyphenWordsigns(Word):
    if("-" not in Word):
        return Word
    else:
        New = Word.replace("-", "∆-∆")
        New = New.split("∆")

        Letter = ""

        for Piece in New:
            NoPunc = Piece

            if(Piece == "-"):
                Letter += Piece
                continue

            for Thing in SingleWordRemoval:
                if(Thing in NoPunc):
                    NoPunc = NoPunc.replace(Thing, "")

            for Key in SingleWord:
                if(NoPunc.lower() == Key.lower()):
                    Piece = Piece.replace(NoPunc, SingleWord[Key])

            Letter += Piece

        Word = Letter

        return Word

# ----------------------------------------------------
"""
------------------------------------------------------
This is for 'cc' and 'dd' which are only valid in the
middle of words except not in number mode cause then
they gotta be ':' and '.' and therefore they are
annoying and stupid and a disappointment to everyone.
------------------------------------------------------
"""
def AnnoyingGroupsigns(Word):
    for Key in Obnoxious:
        if(Key in Word):
            Word = Word.replace(Key, Obnoxious[Key])
            
    return Word
# ----------------------------------------------------
"""
------------------------------------------------------
This is where we fix the single-letter grade 1
indicators which would still be left in the text.
------------------------------------------------------
"""
def Grade1Letters(Word):
    for letter in lower:
        if(";"+letter in Word):
            Word = Word.replace(";"+letter, letter)

    for LETTER in UPPER:
        if(";"+LETTER in Word):
            Word = Word.replace(";"+LETTER, LETTER)
            
    return Word

# ----------------------------------------------------
"""
------------------------------------------------------
There are three contractions which are only used at
the beginning of a word: 'dis', 'con' and 'be'.

We first take away any beginning punctuation and just
leave the word. Then we see the first character of
that word and if it is '4', '3', or '2', then we
change it to 'dis', 'con' or 'be' respectively.
------------------------------------------------------
"""
def StartingContractions(Word):

    New = Word
    Change = Word

    #print(Word)
    
    for Symbol in StartPunc:
        if(Symbol in New):
            New = New.replace(Symbol, "")
            
    if(len(New) == 0):
        return Word

    if(New[0].lower() == "4"):
        Change = "dis" + New[1:]
    elif(New[0].lower() == "3"):
        Change = "con" + New[1:]
    elif(New[0].lower() == "2"):
        Change = "bbe" + New[1:]
    else:
        Change = New

    Word = Word.replace(New, Change)
    return Word

# ----------------------------------------------------
"""
------------------------------------------------------
This function deals with "whole word contractions".

These are contractions which are stand-alone words.
They need to be dealt with separately from the other
contractions which are not always by themselves.

First, we remove all of the beginning and ending
punctuation to just have the word itself. Then we
loop through the dictionary to see if the word matches
any of the known stand-alone words.

If so, then we replace the contraction with the full
word and return it.
------------------------------------------------------
"""
def WholeWord(Word, Caps):

    NoPunc = Word
    New = Word

    for Thing in Removal:
        if(Thing in NoPunc):
            NoPunc = NoPunc.replace(Thing, "")

    Dictionary = open(os.getcwd() + "/Shortform Dictionary.txt", "r")

    Shortforms = []

    for Line in Dictionary:
        Line = Line.strip()
        Line = Line.split(" = ")
        Shortforms.append(Line)

    Dictionary.close()

    if(New == "ゆ"):
        New = "was"

    if(New == "よ"):
        New = "his"

    for Key in Shortforms:
        if(NoPunc.lower() == Key[0].lower()):
            if(Caps):
                New = Word.replace(NoPunc, Key[1].upper())
            elif(NoPunc.isupper() and len(NoPunc) == 1):
                New = Word.replace(NoPunc, Key[1].capitalize())
            elif(NoPunc.isupper() and len(NoPunc) > 1):
                New = Word.replace(NoPunc, Key[1].upper())
            elif(NoPunc[0].isupper()):
                New = Word.replace(NoPunc, Key[1].capitalize())
            else:
                New = Word.replace(NoPunc, Key[1]) 

    return New


# ----------------------------------------------------
"""
------------------------------------------------------
This is where we account for a single letter in a
different typeface (bold, underline and italics).
------------------------------------------------------
"""
def TypefaceSingle(Word):
    X = 0
    New = ""
    for Letter in Word:
        if(Letter == "あ"):
            X += 1
            New += Letter
            continue

        if(Letter == "い"):
            X += 1
            New += Letter
            continue

        if(Letter == "う"):
            X += 1
            New += Letter
            continue

        New += Letter

        if(X > 0):
            for i in range(X):
                New += "}"
            X = 0

    return New

# ----------------------------------------------------
"""
------------------------------------------------------
The purpose of this function is to convert the
punctuation and symbols which take up two characters
in Braille and only one in print.

An example is the dollar sign (Dot4 + Dots234).

Anyway, we use a dictionary to find all instances of
these characters in a word and convert them to a dummy
character (a Greek letter). We need to use Greek
letters since they do not appear in normal ASCII
Braille, so they will not be confused with other
letters later on.

This function is also used to translate them all back
at the end of the transcription.
------------------------------------------------------
"""

def TwoLetterPunctuation(Word, PutBack):
    if(PutBack):
        Dictionary = TwoCharSymb
    else:
        Dictionary = TwoCharPunc

    for Key in Dictionary:
        if(Key in Word):
            Word = Word.replace(Key, Dictionary[Key])

    return Word
    

# ----------------------------------------------------
"""
------------------------------------------------------
By the time we get here, the only instances of 3, 1
and 4 will be for colons, commas and full-stops
respectively. So we can replace them here.

Number Mode is broken by colons, hyphens, and anything
other than a full-stop or comma. But there may be more
than one Number Mode activation in the word given.
------------------------------------------------------
"""
def NumberMode(Word):

    NumWord = ""

    Num = False

    if(len(Word) > 1):
        if(Word[1] == "-"):
            NumWord += "-"
            Word = Word[0] + Word[2:]

    for Letter in Word:
        if(Letter == "#"):
            Num = True
            continue
        elif(Letter == ";"):
            Num = False
            continue
        else:
            if(Num):
                if(Letter not in NumberLine):
                    Num = False

                    if(Letter == "て"):
                        NumWord += ":"
                    else:
                        NumWord += Letter
                        
                    continue
                else:
                    for Key in Numbers:
                        if(Letter == Key):
                            NumWord += Numbers[Key]
            else:
                NumWord += Letter

    NumWord = NumWord.replace("て","cc")
    NumWord = NumWord.replace("に","ea")

    return NumWord

# ----------------------------------------------------
"""
------------------------------------------------------
Here we deal with individual capital letters. By this
point, we will have dealt with the word and passage
capital indicators so we don't need to worry about
mixing them up.

We go through letter by letter, and if the letter is
"," (the capital indicator), then we skip it and the
next letter is capitalised.
------------------------------------------------------
"""
def IndividualCaps(Word):

    CAPSWORD = ""

    Caps = False

    for Letter in Word:
        if(Letter == ","):
            Caps = True
            continue
        else:
            if(Caps):
                CAPSWORD += Letter.upper()
                Caps = False
            else:
                CAPSWORD += Letter

    return CAPSWORD

# ----------------------------------------------------
"""
------------------------------------------------------
Here is where we deal with ending punctuation. We need
this because certain characters are punctuation at
the end of the word, but something different at the
beginning or in the middle of the word.

First, we flip the word backwards. Then, we loop
through it and once we reach a character that is not
end punctuation, we stop.

While we have end punctuation characters, we convert
those and add them to the dummy string. At the end,
we merge the dummy string and the rest of the letters
and flip the whole word back around again.

Ex: ,cat68 (Cat!?)

1. 86tac,
2. 86 -> ?!
3. ?1 + tac, = ?!tac,
4. ,cat!? (Capital letter converted later)
------------------------------------------------------
"""
def EndPunctuation(Word):

    Drow = Word[::-1]
    Tnirp = ""
    Set = 0

    for Rettel in Drow:
        if(Rettel not in EndPuncLine): # End Punc Stops
            break
        
        for Key in EndPunc:
            if(Rettel == Key):
                Tnirp += EndPunc[Key]
                Drow = Drow[1:]

    Drow = Tnirp+Drow
    
    return Drow[::-1]

# ----------------------------------------------------
"""
------------------------------------------------------
This function is supposed to deal with the Capitalised
Word indicators.

If you have two or more letters in a row which need
to be capitalised, you use ",,".

It is broken by a capital terminator (,') or by a
hyphen (-), a single capital letter (,X) or by
anything which is not another letter actually.

First, we replace any instances of ,, with Alpha and
any instances of the capital terminator with Beta
just to have everything in one character
------------------------------------------------------
"""
def CapsWord(Word):

    Caps = False

    Word = Word.replace(",,", "®")
    Word = Word.replace(",'", "©")

    New = ""

    for Letter in Word:
        if(Letter == "®"):
            Caps = True
            continue
        elif(Letter == "©"):
            Caps = False
            continue
        else:
            if(Letter in Alphabet):
                if(Caps):
                    if(Letter == "ふ"):
                        New += "フ"
                    elif(Letter == "て"):
                        New += "テ"
                    elif(Letter == "く"):
                        New += "ク"
                    elif(Letter == "に"):
                        New += "ニ"
                    else:
                        New += Letter.upper()
                else:
                    New += Letter.lower()
            else:
                New += Letter.lower()
                Caps = False

    return New
    

# ----------------------------------------------------
"""
------------------------------------------------------

------------------------------------------------------
"""
def Grade1Words(Word, Caps):
    Grade1 = False

    Grades = []
    Pieces = []

    String = ""

    for Letter in Word:
        if(Letter == "∑"):
            Grade1 = True
            Grades.append(True)

            if(String != ""):
                Pieces.append(String)
                
            String = ""
            continue
        elif(Letter == "œ"):
            Grade1 = False
            Grades.append(False)

            if(String != ""):
                Pieces.append(String)
                
            String = ""
            continue
        else:
            String += Letter

    Pieces.append(String)

    X = 0
    New = ""
    
    for Element in Pieces:
        Thing = Element
        if(not Grades[X]):
            Thing = StartingContractions(Thing)
            Thing = WordGroupsigns(Thing)
            Thing = AnnoyingGroupsigns(Thing)
            Thing = HyphenWordsigns(Thing)
            Thing = WholeWord(Thing, Caps)
            New += Thing
        else:
            New += Element

        X += 1

    return New
# ----------------------------------------------------
def TextMode(Word, Bold, Italics, Underline, Caps, Grade1, LATEX):    
    Word = Word.replace(",-","げ")
    Word = Word.replace('",-',"ゲ")

    Word = Word.replace("@.<","せ")
    Word = Word.replace("@.>","そ")

    # Passage Indicators
    if(";;" in Word):
        Grade1 = True
        Word = Word.replace(";;","∑")

    if(";'" in Word):
        LastGrade1 = True
        Word = Word.replace(";'", "œ")

    if("^1" in Word):
        Bold = 2
        Word = Word.replace("^1","あ")

    if("^2" in Word):
        Bold = 1
        Word = Word.replace("^2","あ")

    if("_1" in Word):
        Underline = 2
        Word = Word.replace("_1","い")

    if("_2" in Word):
        Underline = 1
        Word = Word.replace("_2","い")

    if(".1" in Word):
        Italics = 2
        Word = Word.replace(".1","う")

    if(".2" in Word):
        Italics = 1
        Word = Word.replace(".2","う")

    Word = Word.replace("^'","か")
    Word = Word.replace("_'","か")
    Word = Word.replace(".'","か")

    Word = TwoLetterPunctuation(Word, True)

    if(Word[0] == "8"):
        Word = 'よ' + Word[1:]

    Word = Word.replace(",8", ",his")
    Word = Word.replace(",0", ",was")

    if(not Grade1):
        Word = StartingContractions(Word)

    if(not Grade1):
        Word = WordGroupsigns(Word)

    if(not Grade1):
        Word = AnnoyingGroupsigns(Word)

    if(not Grade1):
        Word = HyphenWordsigns(Word)

    if(",'" in Word):
        LastCap = True

    Word = TwoLetterPunctuation(Word, False)

    Word = CapsWord(Word)

    Word = Word.replace(",て","Cc")
    Word = Word.replace(",ふ","Bb")
    Word = Word.replace(",く","Ff")
    Word = Word.replace(",に","Ea")

    Word = IndividualCaps(Word)

    Word = EndPunctuation(Word)

    if(not Grade1):
        Apple = True

        for Pineapple in StartPuncII:
            if(Word[0:len(Pineapple)+1] == Pineapple+";"):
                Apple = False

            elif(Word[0] == ";"):
                Apple = False
                
        if(Apple):
            Word = WholeWord(Word, Caps)
            Word = Word.replace("bbe", "be")
            Word = Word.replace("BBE", "BE")
            Word = Word.replace("Bbe", "Be")

        Apple = True

    if("∑" in Word):
        Word = Grade1Words(Word, Caps)

    if("#" in Word):
        Word = NumberMode(Word)
    else:
        Word = Word.replace("て","cc")
        Word = Word.replace("テ","CC")
        Word = Word.replace("ふ","bb")
        Word = Word.replace("フ","BB")
        Word = Word.replace("く","ff")
        Word = Word.replace("ク","FF")
        Word = Word.replace("に","ea")
        Word = Word.replace("ニ","EA")

    if(Caps == True):
        Word = Word.upper()

    Word = Grade1Letters(Word)

    if(Bold == 1 or Underline == 1 or Italics == 1):
        Word = TypefaceSingle(Word)
        Bold = 0
        Underline = 0
        Italics = 0

    Word = Word.replace("あ","\\textbf{")
    Word = Word.replace("い","\\ul{")
    Word = Word.replace("う","\\textit{")

    if(Bold == 2 or Underline == 2 or Italics == 2):
        if("か" in Word):
            Word = Word.replace("か","}")
        else:
            if(Bold == 2):
                Word += "}"
            if(Underline == 2):
                Word += "}"
            if(Italics == 2):
                Word += "}"

        Bold = 0
        Underline = 0
        Italics = 0

    if(Bold == 3):
        if("か" in Word):
            Bold = 0
            Word = Word.replace("か", "}")

    if(Underline == 3):
        if("か" in Word):
            Underline = 0
            Word = Word.replace("か", "}")

    if(Italics == 3):
        if("か" in Word):
            Italics = 0
            Word = Word.replace("か", "}")

    if(LATEX):
        Word = Word.replace("せ","\\DoLine \n\n\\textbf{Transcriber's Note:} ")
        Word = Word.replace("%","\%")
        Word = Word.replace("#","\#")
    else:
        Word = Word.replace("\\$", "$")
        Word = Word.replace("せ","[[TRANSCRIBER'S NOTE: ")

    if(LATEX):
        Word = Word.replace("そ", "\n\n\\DoLine")
    else:
        Word = Word.replace("そ","]]")

    Word = Word.replace("ゆ",'"')
    Word = Word.replace("よ",'"')
    Word = Word.replace("げ", "--")
    Word = Word.replace("ゲ", "---")

    if("∑" in Word):
        Grade1 = False
        
    Word = Word.replace("∑", "")
    Word = Word.replace("œ", "")

    return Word, Bold, Italics, Underline, Caps, Grade1, LATEX
# ----------------------------------------------------
"""
------------------------------------------------------
This is the main function. First, we set all of the
flags for the various indicators (Capital Mode, Number
Mode, Nemeth Mode, etc.

Then, we loop through each line in the file (each
portion that is separated by a newline).

For each line, we loop through each word. A word is
here defined as "continuous block of characters
separated by spaces". So, "Jean-Phillipe" is one word
and "white gorilla" is two.

Here is where we call the other functions which deal
with punctuation and contractions and other such fun
stuff.
------------------------------------------------------
"""
def Transcribe(Old, New, Latex, Verbose, LogFile, Read, MakeFile):

    HasEquals = True

    if(MakeFile == "2" or MakeFile == "1"):
        HasEquals = input("Are all instances of .k in the file an equals sign?\n0 = Yes\n1 = No\nIf you are not sure, select 1.\n")

        if(HasEquals == "1"):
            HasEquals = False
        else:
            HasEquals = True

    LogLine = 0

    if(Latex == "1"):
        LATEX = True
    else:
        LATEX = False

    Settings = open(os.getcwd() + "/Latex Settings.txt", "r")

    # Flags = four elements
    # 0 = use title flag
    # 1 = title marker (string)
    # 2 = how many lines
    # 3 = auto first line title
    Flags = []

    for Line in Settings:
        Line = Line.strip()

        if("#" in Line or Line == ""):
            continue
        else:
            Line = Line.split(" = ")
            if(Line[1] == "True"):
                Flags.append(True)
            elif(Line[1] == "False"):
                Flags.append(False)
            else:
                Flags.append(Line[1])

    Caps = False
    Num = False

    LastCap = False
    
    Bold = 0
    Italics = 0
    Underline = 0

    FirstLine = True

    MakingTitle = False

    Grade1 = False
    LastGrade1 = False

    Table = False
    TableSection = 0
    TableLine = 0

    T = -1
    SkipPhrase = 0
    
    for Line in Old:
        Line = Line.strip()

        Caps = False
        Grade1 = False

        if(Line == ""):
            New.write("")
            continue

        if(MakingTitle):
            if(T == 0):
                MakingTitle = False
                New.write("}\n\n")
                T = -1
            elif(T > 0):
                T -= 1
            else:
                T = T

        if(LATEX):
            if(Flags[0]): # Use Title
                if(FirstLine and Flags[3]):
                    FirstLine = False
                    New.write("\\NewTitle{")
                    T = 0
                    MakingTitle = True
                else:
                    if(Line == Flags[1]):
                        New.write("\\NewSection{")
                        T = int(Flags[3])
                        MakingTitle = True
                        continue

        Line = Line.split()

        Print = ""

        SkipLetter = 0
        SkipPhrase = 0
        
        for Word in Line:

            if("_%" in Word):
                if(Bold == 3):
                    Bold = 0
                    Word += "}"

                if(Italics == 3):
                    Italics = 0
                    Word += "}"

                if(Underline == 3):
                    Underline = 0
                    Word += "}"
                    
                [SkipLetter, SkipPhrase, LogLine] = DoNemeth(HasEquals, Line, LATEX, New, SkipPhrase, Verbose, LogFile, Read, LogLine)
                continue

            if(SkipLetter > 0):
                SkipLetter -= 1
                continue

            if(Table):                
                if(Word == "..."): # Start new table section
                    if(TableSection == 0): # Ending title
                        New.write("}{")
                        TableSection = 1
                        continue
                    elif(TableSection == 1): # Ending row #
                        TableSection = 2
                        continue
                    else: # Actual Table Part
                        if(TableLine == 0): # First Line ending
                            New.write("\\\\ \n \\hline \n")
                            TableLine = 1
                            continue
                        else:
                            New.write("\\\\ \n")
                            continue

                if(TableSection == 1): # We are on row number
                    RowNum = int(Word[1:])
                    New.write("c"*RowNum + "}{\n")
                    continue

                if(Word == "&&"):
                    New.write(" & ")
                    continue

                if(Word == ".).)t"): # Table ending
                    New.write("}\n")
                    Table = False
                    TableSection = 0
                    TableLine = 0
                    continue                

            if(Word == "t.(.("): # Table Start
                Table = True
                New.write("\\MakeTab{")
                continue

            if(LastCap):
                LastCap = False
                Caps = False

            if(LastGrade1):
                LastGrade1 = False
                Grade1 = False

            if(",,," in Word):
                Caps = True
                Word = Word.replace(",,,","")

            if(";;;" in Word):
                Grade1 = True
                Word = Word.replace(";;;","")
                
            if("^7" in Word):
                Bold = 3
                Word = Word.replace("^7","あ")

            if("_7" in Word):
                Underline = 3
                Word = Word.replace("_7","い")

            if(".7" in Word):
                Italics = 3
                Word = Word.replace(".7","う")

            [Word, Bold, Italics, Underline, Caps, Grade1, LATEX] = TextMode(Word, Bold, Italics, Underline, Caps, Grade1, LATEX)

            if(Verbose):
                print(Word)

            New.write(Word + " ")

        if(not MakingTitle):
            New.write("\n")
            if(LATEX):
                New.write("\n")

        Bold = 0
        Underline = 0
        Italics = 0

# ----------------------------------------------------
def WriteLatexPreamble(New):
    New.write("\\documentclass[17pt]{extarticle}\n\n")

    New.write("\\usepackage{soul}\n")
    New.write("\\usepackage{amsmath}\n")
    New.write("\\usepackage[letterpaper, total={7in, 10in}]{geometry}\n")
    New.write("\\usepackage{mathtools}\n")
    New.write("\\usepackage{amssymb}\n")
    New.write("\\usepackage{gensymb}\n")
    New.write("\\usepackage[russian,english]{babel}\n")
    New.write("\\usepackage[OT2,T1]{fontenc}\n")
    New.write("\\usepackage{accents}\n")
    New.write("\\usepackage{hyperref}\n\n")

    New.write("\\DeclareFontFamily{U}{rcjhbltx}{}\n")
    New.write("\\DeclareFontShape{U}{rcjhbltx}{m}{n}{<->rcjhbltx}{}\n")
    New.write("\\DeclareSymbolFont{hebrewletters}{U}{rcjhbltx}{m}{n}\n\n")

    New.write("\\DeclareMathSymbol{\\aleph}{\\mathord}{hebrewletters}{39}\n")
    New.write("\\DeclareMathSymbol{\\bet}{\\mathord}{hebrewletters}{98}\n")
    New.write("\\DeclareMathSymbol{\\gimel}{\\mathord}{hebrewletters}{103}\n")
    New.write("\\DeclareMathSymbol{\\dalet}{\\mathord}{hebrewletters}{100}\n")
    New.write("\\DeclareMathSymbol{\\he}{\\mathord}{hebrewletters}{104}\n")
    New.write("\\DeclareMathSymbol{\\vav}{\\mathord}{hebrewletters}{110}\n")
    New.write("\\DeclareMathSymbol{\\zayin}{\\mathord}{hebrewletters}{115}\n")
    New.write("\\DeclareMathSymbol{\\chet}{\\mathord}{hebrewletters}{120}\n")
    New.write("\\DeclareMathSymbol{\\tet}{\\mathord}{hebrewletters}{84}\n")
    New.write("\\DeclareMathSymbol{\\yod}{\\mathord}{hebrewletters}{121}\n")
    New.write("\\DeclareMathSymbol{\\kaf}{\\mathord}{hebrewletters}{107}\n")
    New.write("\\DeclareMathSymbol{\\lamed}{\\mathord}{hebrewletters}{108}\n")
    New.write("\\DeclareMathSymbol{\\mem}{\\mathord}{hebrewletters}{109}\n")
    New.write("\\DeclareMathSymbol{\\nun}{\\mathord}{hebrewletters}{110}\n")
    New.write("\\DeclareMathSymbol{\\samekh}{\\mathord}{hebrewletters}{115}\n")
    New.write("\\DeclareMathSymbol{\\ayin}{\\mathord}{hebrewletters}{96}\n")
    New.write("\\DeclareMathSymbol{\\pe}{\\mathord}{hebrewletters}{112}\n")
    New.write("\\DeclareMathSymbol{\\tsadi}{\\mathord}{hebrewletters}{118}\n")
    New.write("\\DeclareMathSymbol{\\qof}{\\mathord}{hebrewletters}{113}\n")
    New.write("\\DeclareMathSymbol{\\resh}{\\mathord}{hebrewletters}{114}\n")
    New.write("\\DeclareMathSymbol{\\shin}{\\mathord}{hebrewletters}{152}\n")
    New.write("\\DeclareMathSymbol{\\tav}{\\mathord}{hebrewletters}{116}\n\n")                                                                                               

    New.write("\\newcommand{\\NewTitle}[1]{\\huge \\begin{center} \\ul{#1} \\end{center} \\normalsize \\phantomsection \\addcontentsline{toc}{section}{#1}} \n\n")
    New.write("\\newcommand{\\NewSection}[1]{\\section*{#1} \\phantomsection \\addcontentsline{toc}{subsection}{#1}}\n\n")
    New.write("\\newcommand{\\MakeTab}[3]{\\begin{center} \\subsubsection*{#1} \\end{center} \\begin{center} \\begin{tabular}{#2} #3 \\end{tabular} \\end{center}}\n\n")
    New.write("\\newcommand{\\Equ}[1]{\\begin{equation*} \\begin{aligned} #1 \\end{aligned} \\end{equation*}}\n\n")
    New.write("\\newcommand{\\M}[1]{\\begin{bmatrix} #1 \\end{bmatrix}}\n\n")
    New.write("\\newcommand{\\Det}[1]{\\begin{vmatrix} #1 \\end{vmatrix}}\n\n")
    New.write("\\newcommand{\\Cyr}[1]{\\foreignlanguage{russian}{\\textup{#1}}}\n\n")
    New.write("\\newcommand{\\DoLine}{\\begin{center} \\rule{8cm}{0.4pt} \\end{center}}\n\n")
    New.write("\\newcommand{\\Cases}[1]{\\begin{cases} #1 \\end{cases}}\n\n")
    New.write("\\newcommand{\\Ooverline}[1]{\\overline{\\overline{#1}}}\n\n")
    New.write("\\newcommand{\\Uunderline}[1]{\\underline{\\underline{#1}}}\n\n")

    New.write("\\begin{document}\n\n")
    New.write("\\tableofcontents\n\n\\newpage\n\n")
# ----------------------------------------------------  
Done = False

print("Welcome to the Braille To Print Transcriber.\n")
print("You can input a BRF or TXT file with ASCII Braille")
print("and get out a TXT file with the corresponding print.\n")
print("This program assumes that you are using UEB and that")
print("you used proper spelling and formatting for everything.\n")
print("Also, things such as Nemeth and different typefaces (bold,")
print("italics, etc.) are written in LaTeX format.")

while(not Done):
    while True:
        Name = input("Enter the name of the file: ")
        E = (input("File type?\n0 = BRF\n1 = TXT\n"))
        if(E == "1"):
            Extension = ".txt"
        else:
            Extension = ".brf"

        try:
            Old = open(os.getcwd()+"/File Input/"+Name+Extension, "r")
            break
        except:
            print("File does not exist.\n")

    print("Make this a LaTeX file?")
    print("This will create a .TEX file instead of a .TXT file.")
    print("This is for when you want equations or extra typefaces (bold, italic, underline).")
    Latex = input("Press 1 for a LaTeX file.\n")

    print("If a print file with the same name exists, would you like to overwrite it?\n")
    Overwrite = input("Press 1 to NOT overwrite.\n")

    if(Latex == "1"):
        Ending = " Print.tex"
    else:
        Ending = " Print.txt"

    Version = 1

    while True:
        if(Overwrite == "1"):
            try:
                New = open(os.getcwd()+ "/File Output/" + Name + Ending, "w")
            except FileExistsError:
                Name += " " + str(Version)
                Version += 1
            else:
                break
        else:
            New = open(os.getcwd() + "/File Output/" + Name + Ending, "w")
            break

    Verbose = input("Print finished words to console?\nPress 1 to do so.\n")

    if(Verbose == "1"):
        Verbose = True
    else:
        Verbose = False

    while True:
        MakeFile = input("Use/Create Disambiguation File?\n0 = Don't use\n1 = Use existing\n2 = Make new one\n")

        if(MakeFile == "1"):
            try:
                LogFile = open(os.getcwd() + "/Log Files/" + Name + " Disambiguation File.txt", "r", encoding="utf-8")
            except FileNotFoundError:
                print("File does not exist.\n")
            else:
                Read = True
                break
        elif(MakeFile == "2"):
            LogFile = open(os.getcwd() + "/Log Files/" + Name + " Disambiguation File.txt", "w", encoding="utf-8")
            Read = False
            break
        else:
            LogFile = "nothing"
            Read = False
            break

    if(Latex == "1"):
        WriteLatexPreamble(New)

    Transcribe(Old, New, Latex, Verbose, LogFile, Read, MakeFile)

    if(Latex == "1"):
        New.write("\n\\end{document}")

    if(LogFile != "nothing"):
        LogFile.close()

    New.close()

    Again = input("Transcribe another file?\nPress 1 to quit.\n")
    if(Again == "1"):
        Done = True
