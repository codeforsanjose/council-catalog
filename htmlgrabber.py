#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  written/tested using python 2.7.12

import sys
from bs4 import BeautifulSoup
from datetime import date

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    from urllib import urlopen
    sys.setdefaultencoding("utf8")

# fix utf8 - related encoding errors

MONTHS = ["January", "February", "March", "April", "May",
          "June", "July", "August", "September", "October",
          "November", "December"]

AGENDAURLS = {
    2017:"http://www.sanjoseca.gov/index.aspx?NID=5322",
    2016:"http://www.sanjoseca.gov/index.aspx?NID=4858",
    2015:"http://www.sanjoseca.gov/index.aspx?NID=4535",
}

def grabHTML(minDate):
    """
    Collects all HTML-based agendas from sanjoseca.gov since the
    specified date and outputs the raw HTML of those agendas in a
    list of Strings.
    
    Args:
        minDate: a datetime.date object telling the function to ignore
        agendas with dates equal to or earlier than the given date.
    Returns:
        a list of Strings, each String containing all the raw HTML
        for a single agenda
    """
    
    absoluteMinDate = date(2015, 5, 20)
    minDate = min(minDate, absoluteMinDate)
        
    print("Scraping HTML agendas from after {} ...".format(str(minDate)))
    agendaHTMLs = []
          
    for year, url in AGENDAURLS.items():
        if (year < minDate.year):
          continue
        print("Searching " + str(year) + "...")
        yearHTMLsoup = BeautifulSoup(
            urlopen(url).read(), "html.parser",
        )
        linkTable = yearHTMLsoup.find("table", class_="telerik-reTable-2")
        for row in linkTable.find_all("tr"):
          anchor =  row.td.a
          month = 0
          day = 0
          try:
              a_href = anchor['href']
              a_text = anchor.text
              print('A_TEXT: ', a_text)
              for i in range(len(MONTHS)):
                  if a_text.startswith(MONTHS[i]):
                      month = i+1
                      break
                  monthCharLength = len(MONTHS[month-1])
                  day = int(a_text[monthCharLength+1:monthCharLength+3].rstrip(',- '))
                        
                  currentDate = date(year, month, day)
                  if (currentDate > minDate):
                      if (a_href.find("AgendaViewer") >= 0 and a_href.find(".pdf") == -1):
                          print(str(currentDate) + ": scraping " + a_href)
                          agendaHTMLs.append(urlopen(a_href).read())
                      else:
                          print("*** non-HTML agenda found: " + anchor.string + "\t" + a_href)
          except TypeError:
              pass
    
    print("\nDone!\n\n")
    return agendaHTMLs
    

#command-line usability (run ""htmlgrabber.py -h" for help, or just read below....)
if __name__ == '__main__':
    import getopt
    d = date(2015,5,20)
    append = False
    output = "htmlgrabber_output.txt"
    try: 
        opts, args = getopt.getopt(sys.argv[1:],"hd:o:a")
    except getopt.GetoptError:
        print("Error - please use this format:\n\tpython htmlgrabber.py -d <YYYY/MM/DD> -o <outputfile.txt>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            #print("""\nhtmlgrabber.py - command line interface\n\n\Collects all html-based agendas from the San Jose City Council website\n\after the given date, and spits them out as a single, continuous text file\n\(raw html).\n\n\usage: htmlgrabber.py -d <YYYY/MM/DD> -o <outputfile.txt>\n\t\ -a :\tappends new HTML to the existing outputfile\n\n""")
            sys.exit()
        elif opt == '-d':
            year = int(arg[0:4])
            month = int(arg[5:7])
            day = int(arg[8:])
            d = date(year, month, day)
        elif opt == '-o':
            output = arg
        elif opt == '-a':
            append = True
    agendas = grabHTML(d)
    outputContent = ""
    for a in agendas:
        outputContent += a
    if append:
        f = open(output, 'a')
    else:
        f = open(output, 'w')
    f.write(outputContent)
    f.close()
    sys.exit()
