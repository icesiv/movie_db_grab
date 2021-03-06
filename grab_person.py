import argparse
from data_grab.run_scraper import Scraper

from data_grab.spiders.s_person import GetPerson

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='enter start index')

args = parser.parse_args()
print("Starting from index ", args.integers)

scraper = Scraper()
scraper.run_spiders(GetPerson , args.integers[0], 'https://www.bmdb.com.bd/person/')