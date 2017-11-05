#!/usr/bin/python
import sys
import codecs
import unicodedata
import xml.etree.ElementTree as ElementTree

def usage():
    return '''
This script converts surname data from Netwerk Naamkunde (licensed CC BY-SA 3.0)
into a format zxcvbn recognizes. To use, first download fn10k_versie1.zip from:

http://www.naamkunde.net/?page_id=294

Unzip the file and then run:

%s fn_10kw.xml ../data/dutch_surnames.txt
''' % sys.argv[0]

def main(input_filename, output_filename):
    '''Separate out the surname prefixes and split everything on spaces to get better results.'''
    root = ElementTree.parse(input_filename).getroot()
    result = {}
    for record in root.findall('record'):
        prefix = record.find('prefix').text
        name = record.find('naam').text.lower()
        if isinstance(name, unicode):
            name = strip_diacritics(name)
        count = int(record.find('n2007').text)

        if prefix:
            lowercase = prefix.lower()
            for part in lowercase.split(' '):
                if part not in result:
                    result[part] = 0
                result[part] += count
            nospaces = lowercase.replace(' ', '')
            if nospaces != lowercase:
                if nospaces not in result:
                    result[nospaces] = 0
                result[nospaces] += count

        for part in name.split(' '):
            if part not in result:
                result[part] = 0
            result[part] += count
        nospaces = name.replace(' ', '')
        if nospaces != name:
            if nospaces not in result:
                result[nospaces] = 0
            result[nospaces] += count

    with codecs.open(output_filename, 'w', 'utf8') as f:
        for item in sorted(result.items(), key=lambda item: -item[1]):
            f.write(item[0] + '\n')

def strip_diacritics(string):
    return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print usage()
    else:
        main(*sys.argv[1:])
    sys.exit(0)
