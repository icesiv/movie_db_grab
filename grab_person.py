import argparse
from data_grab.run_scraper import Scraper

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='enter start index')

args = parser.parse_args()
print("Starting from index ", args.integers)

scraper = Scraper()
scraper.run_spiders(args.integers[0])
