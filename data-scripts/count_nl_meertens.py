#!/usr/bin/python
import sys
import codecs
import unicodedata

def usage():
    return '''
This script converts first name data from the Meertens Instituut into a format zxcvbn
recognizes. To use, first download Top_eerste_voornamen_NL_2010.zip from:

http://www.meertens.knaw.nl/nvb/veelgesteldevragen

Take note to attribute this data to the "Nederlandse Voornamenbank" of the
"Meertens Instituut KNAW" (http://www.meertens.knaw.nl/nvb).

Unzip the file and then run:

%s Top_eerste_voornamen_NL_2010.csv ../data/dutch_female_names.txt ../data/dutch_male_names.txt
''' % sys.argv[0]

def main(input_filename, output_filename_female, output_filename_male):
    with codecs.open(output_filename_female, 'w', 'utf8') as female:
        with codecs.open(output_filename_male, 'w', 'utf8') as male:
            for line in codecs.open(input_filename, 'r', 'latin_1'):
                rank, female_name, female_count, male_name, male_count = line.strip().split(';')
                if rank == '' or rank == 'Rank':
                    continue
                if female_name != '':
                    female.write(strip_diacritics(female_name.lower()) + '\n')
                if male_name != '':
                    male.write(strip_diacritics(male_name.lower()) + '\n')

def strip_diacritics(string):
    return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print usage()
    else:
        main(*sys.argv[1:])
    sys.exit(0)
