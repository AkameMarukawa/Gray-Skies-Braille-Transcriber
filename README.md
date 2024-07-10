**Gray Skies  - Braille To Print Translation Program**
This program is intended to take a .BRF or .TXT file as input
and output either a .TXT or .TEX file in print. This program is
able to transcribe both literary Braille (using UEB rules) and
mathematical Braille (Nemeth code).

When transcribing to a .TEX file, there are certain setting the
user can define in the "Latex Settings.txt" file. This allows
the user to create sections and titles in the .TEX file 
automatically. Do not rename this file.

There is a folder named "File Input". This is where the user
should put the input .BRF or .TXT files. The output is 
created in a folder called "File Output". Do not remove or
rename these folders either.

There is also a file called "Shortform Dictionary.txt" (as you
may guess, you should not rename or delete this file). This is
used for whole-word contractions and is necessary for
transcribing contracted UEB correctly.

When transcribing Nemeth Braille, this program is not able to
correctly transcribe spatial arrangements. This means that
transcribing matrices in the traditional way is sadly not
possible. However, in "Latex Settings.txt", the user may specify
a custom format for matrices which they may use instead.

This program assumes that everything in the input file is spelled
correctly and follows the proper rules. There may be cases where
an incorrectly Brailled phrase is translated into the intended
phrase in print, but this is purely coincidental.

There may be a case where a correctly Brailled phrase is 
transcribed incorrectly in print. This is a bug, and is not
intentional and needs to be fixed.

** Log Files **
There is a folder named "Log Files". This is used when there
are disambiguation statements (places where the program will
ask you what the symbol should be as it is transcribing, as
that symbol has multiple meanings which are not discernable
easily by a computer). These only occur when using Nemeth,
not in literary Braille.

A Log File can be created to save the settings for a particular
document so that if you go to transcribe it again, you do not
have to re-do all of the disambiguation statements over. This
is useful for when you are proofreading and may be correcting
mistakes. Although, if the mistake involves adding or removing
one of the ambiguous characters, then you will need to change
the Log File accordingly.

Ambiguous characters (in Nemeth) are:

1. = and κ
2. " (for Baseline Indicator or Multi-Purpose Indicator)
3. "k (for less than sign or another thing)
4. < (for Radical Indicator or Multi-Purpose Above Indicator)
5. +"-, +"+, -"+, -"- (Sign, Baseline, Sign or Sign, Sign)
(This is because +- by itself becomes the +- symbol with the
+ on top of the -, and similarly with -+)

The program will not need to ask you to specify which character
you want for every occurrence, as the program does use some
logic to figure this out. Therefore, if you add or remove one
of these characters, it is best to just re-create the Log File
in the program instead of trying to guess where and how you need
to edit the existing one.
