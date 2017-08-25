import json
import argparse
from bs4 import BeautifulSoup


def parse_content(input_html):
    """
    Given some content from a city council meeting,
    extract useful content.
    """
    soup = BeautifulSoup(input_html, 'html.parser')
    output = {}
    for table in soup.find_all('table'):
        numberspace = table.find_next('td')
        number_header = numberspace.text
        textspace = numberspace.find_next('td')
        text_header = textspace.text.split('\n')[0]
        blockquotes = table.find_all_next('blockquote')
        if not blockquotes:
            continue
        block_text = [blockquote.text for blockquote in blockquotes]
        if not number_header or not text_header or not block_text:
            # Nothing to do here
            continue
        output[number_header] = {
            'title': text_header,
            'block_content': block_text
        }

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
            input_html = meeting['content']
            dict_content = parse_content(input_html=input_html)
            output[date] = dict_content
    with open(outfile, 'w') as f:
        json.dump(output, f)
