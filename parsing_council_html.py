import re
import json
import argparse
import lxml.html
from collections import defaultdict


def parse_content(input_html):
    """
    Given some content from a city council meeting,
    extract useful content.
    """
    root = lxml.html.fromstring(input_html)
    output = defaultdict(dict)
    current_key = None
    previous_was_key = False


    for x in root.xpath('//div | //td'):
        text = x.text
        if text in ('None', None):
            continue
        text = text.lstrip().rstrip()
        match = re.match('\d+.\d*', text)
        if not match and current_key:
            if x.tag == 'td' and previous_was_key:
                output[current_key]['header'].append(text)
            else:
                output[current_key]['content'].append(text)
        elif match:
            # Grab what matched the regex.
            # That should be a number with a decimal
            # Such as 5.1 or 2.
            # It should also start the string.
            # This should be seen as the seciton number.
            current_key = match.group(0)
            output[current_key] = {
                'content': [],
                'header': [],
            }

        if match:
            previous_was_key = True
        else:
            previous_was_key = False

    return output            
            

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        'Given extracted HTML, find important features'
    )
    argparser.add_argument('--infile', help='Input file with JSON html content')
    argparser.add_argument('--outfile',
                           help='Output file for JSON output')
    args = argparser.parse_args()

    infile = args.infile
    outfile = args.outfile
    output = {}
    with open(infile, 'r') as f:
        data = json.load(f)
        for date, meeting in data.items():
            print(meeting.keys())
            input_html = meeting['content']
            dict_content = parse_content(input_html=input_html)
            output[date] = dict_content
    with open(outfile, 'w') as f:
        json.dump(output, f)
