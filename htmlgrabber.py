#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  written/tested using python 2.7.12

import sys
import json
import argparse
from bs4 import BeautifulSoup
from datetime import date, datetime
import dateutil.parser

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

    absoluteMinDate = datetime(year=2015, month=5, day=20)
    minDate = max(minDate, absoluteMinDate)

    print("Scraping HTML agendas from after {} ...".format(str(minDate)))
    agendaHTMLs = {}
    meeting_type = 'city_council'

    for year, url in AGENDAURLS.items():
        if (year < minDate.year):
          continue
        print("Searching " + str(year) + "...")
        yearHTMLsoup = BeautifulSoup(
            urlopen(url).read(), "html.parser",
        )
        # NOTE JMS: start of the beautiful soup parser currently only reading tables and tr
        linkTable = yearHTMLsoup.find("table", class_="telerik-reTable-2")
        handle_tables_beautifulsoup_parser(linkTable, agendaHTMLs, minDate, meeting_type)

    print("\nDone!\n\n")
    return agendaHTMLs

def handle_tables_beautifulsoup_parser(linkTable, agendaHTMLs, minDate, meeting_type):
    for row in linkTable.find_all("tr"):
        anchor =  row.td.a
        if anchor is None:
            continue
        try:
            a_href = anchor['href']
            a_text = anchor.text
            # Depend on dateutil's fuzzy parser
            # This usually creates a reasonable date out of things.
            meeting_date = dateutil.parser.parse(a_text, fuzzy=True)
            if meeting_date <= minDate:
                continue
            date_str = str(meeting_date)

            # NOTE JMS: does this go through the pdf links on each meeting?
            if (a_href.find("AgendaViewer") >= 0 and a_href.find(".pdf") == -1):
                print(date_str + ": scraping " + a_href)
                agendaHTMLs[date_str] = {
                    'content': urlopen(a_href).read().decode('utf-8'),
                    'type': meeting_type,
                }
            else:
                msg = "*** non-HTML agenda found: {}\t{}"
                msg = msg.format(anchor.string, a_href)


        except TypeError:
            print('Experienced unexpected TypeError')
            pass
        except ValueError:
            print("Experienced non-parseable date")
            pass

#command-line usability (run ""htmlgrabber.py -h" for help, or just read below....)
if __name__ == '__main__':
    import getopt
    d = datetime(year=2015, month=5, day=20)
    append = False
    output = "htmlgrabber_output.json"
    parser = argparse.ArgumentParser('Grab HTML content from council meetings')
    parser.add_argument('-d', '--date', help='Date in <YYYY/MM/DD> format',
                        default='2015/05/20')
    parser.add_argument('-o', '--outfile',
                        help='Outputfile to write HTML data to',
                        default=output,
    )
    parser.add_argument('-a', '--append', help='Appends to existing outfile',
                        action="store_true", default=False)
    args = parser.parse_args()

    input_date = datetime.strptime(args.date, '%Y/%m/%d')

    agendas = grabHTML(input_date)
    if append:
        with open(output, 'r') as f:
            initial_data = json.load(f)
            if not isinstance(initial_data, dict):
                raise TypeError('Appending to non dictionary')
            initial_data.update(agendas)
            agendas = initial_data
    with open(output, 'w') as f:
        json.dump(agendas, f)
