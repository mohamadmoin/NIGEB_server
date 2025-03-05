# from labs.models import Lab
# from tests_definitions.models import TestInfo

# # Create some labs
# Lab.objects.create(
#     name='Central Lab', 
#     address='123 Main St, Downtown', 
#     phone_number='123-456-7890', 
#     email='central@labs.com'
# )

# Lab.objects.create(
#     name='East Lab', 
#     address='456 East St, Eastside', 
#     phone_number='234-567-8901', 
#     email='east@labs.com'
# )

# Lab.objects.create(
#     name='West Lab', 
#     address='789 West St, Westend', 
#     phone_number='345-678-9012', 
#     email='west@labs.com'
# )

# Lab.objects.create(
#     name='North Lab', 
#     address='101 North St, Northside', 
#     phone_number='456-789-0123', 
#     email='north@labs.com'
# )

# Lab.objects.create(
#     name='South Lab', 
#     address='202 South St, Southside', 
#     phone_number='567-890-1234', 
#     email='south@labs.com'
# )

# # Create some tests
# # TestInfo.objects.create(test_code='TST001', test_name='Complete Blood Count', unit='cells/mcL', test_cost=50.00)
# # TestInfo.objects.create(test_code='TST002', test_name='Liver Function Test', unit='U/L', test_cost=75.00)
# # TestInfo.objects.create(test_code='TST003', test_name='Blood Glucose', unit='mg/dL', test_cost=20.00)
# # Add more tests as needed
from django.core.management.base import BaseCommand
from labs.models import Lab
from tests_definitions.models import TestInfo

class Command(BaseCommand):
    help = 'Generate fake labs and tests'

    def handle(self, *args, **kwargs):
        # Create some labs with all fields filled
        Lab.objects.create(
            name='NIGEB Lab', 
            address='123 Main St, Downtown', 
            phone_number='123-456-7890', 
            email='central@labs.com'
        )

        Lab.objects.create(
            name='ARAMESH Lab', 
            address='456 East St, Eastside', 
            phone_number='234-567-8901', 
            email='east@labs.com'
        )

        Lab.objects.create(
            name='IRANIAN Lab', 
            address='789 West St, Westend', 
            phone_number='345-678-9012', 
            email='west@labs.com'
        )

        Lab.objects.create(
            name='MASOOD Lab', 
            address='101 North St, Northside', 
            phone_number='456-789-0123', 
            email='north@labs.com'
        )

        Lab.objects.create(
            name='PARSEH Lab', 
            address='202 South St, Southside', 
            phone_number='567-890-1234', 
            email='south@labs.com'
        )

        # Create some tests
        # TestInfo.objects.create(test_code='TST001', test_name='Complete Blood Count', unit='cells/mcL', test_cost=50.00)
        # TestInfo.objects.create(test_code='TST002', test_name='Liver Function Test', unit='U/L', test_cost=75.00)
        # TestInfo.objects.create(test_code='TST003', test_name='Blood Glucose', unit='mg/dL', test_cost=20.00)
        # Add more tests as needed

        self.stdout.write(self.style.SUCCESS('Successfully generated fake labs and tests'))