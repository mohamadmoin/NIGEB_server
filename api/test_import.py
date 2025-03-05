import csv
from datetime import datetime
import os
import django
import argparse
import sys

sys.path.append('/Users/macbookpro/nigeb_server')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trauma.settings')
django.setup()

from api.models import TestInfos  # Replace 'myapp' with your actual app name

def import_books(file_path):
    with open(f"/Users/macbookpro/nigeb_server/media/{file_path}", 'r') as file:
        
        reader = csv.DictReader(file)
        TestInfos.objects.all().delete()
        for row in reader:
            TestInfos.objects.create(
            # id_id = row['\ufeffid'],
            
            # testCode = row['testCode'],
            testName = row['\ufefftest'],
            group = row['group'],
            unit = row['unit'],
            # description = row['description'],
            normal_range = row['normalrange'],
            # k_total = row['k_total'],
            # k_fani = row['k_fani'],
            # k_herfe = row['k_herfe'],
            # testCost1 = row['testCost1'],
            # testCost2 = row['testCost2'],
            # testCost3 = row['testCost3'],
            # testCost4 = row['testCost4'],
        )

              
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('file_path',type=str,help='')
    args = parser.parse_args() # Replace with your actual file path
    import_books(args.file_path)
