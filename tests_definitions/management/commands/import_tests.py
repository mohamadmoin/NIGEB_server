import csv
from django.core.management.base import BaseCommand
from tests_definitions.models import TestInfo

class Command(BaseCommand):
    help = 'Import test data from CSV file'

    def handle(self, *args, **kwargs):
        with open('tests_definitions/management/testscopy.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                test_name = row['test'].strip()
                test_code = row['Abbr'].strip()
                unit = row['unit'].strip() if row['unit'] else ''
                normal_range = row['normalrange'].strip() if row['normalrange'] else ''
                group = row['group'].strip() if row['group'] else ''

                # Create or update the TestInfo object
                test_info, created = TestInfo.objects.update_or_create(
                    test_code=test_code,
                    defaults={
                        'test_name': test_name,
                        'unit': unit,
                        'normal_range': normal_range,
                        'group': group,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created test: {test_name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated test: {test_name}'))