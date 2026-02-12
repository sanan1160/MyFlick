#!/usr/bin/env python3
import sys
from gtts import gTTS


def speak_command(text):

    if text=="":
      return

    res = gTTS(text=text, lang='en')

    phrase=text.replace(" ","_")

    filename = "/home/pi/bin/"+phrase+".wav"

    res.save(filename)



def main():

    args = sys.argv[1:]

    # Validate that at least one argument is provided
    if len(args) == 0:
        print("Usage: python script.py <arg1> <arg2> ...")
        sys.exit(1)

    separator = " " 
    phrase = separator.join(sys.argv[1:])
    print(phrase)
    speak_command(phrase)
    
if __name__ == "__main__":
   main()
