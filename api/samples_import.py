import csv
from datetime import datetime
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trauma.settings')
django.setup()

from api.models import Samples, Patients, User  # Replace 'myapp' with your actual app name

def import_books(file_path):
    with open(file_path, 'r') as file:
        
        reader = csv.DictReader(file)
        for row in reader:
            try:
                pati = Patients.objects.get(id_id=row['patientId'])
            except Patients.DoesNotExist:
                print("noooo")
                print(row['patientId'])
                print(row)
                userr = User.objects.get(id = 1)
                Patients.objects.create(
                id_id = row['\ufeffid'],
                user = userr,
                userCreatorName = 'userCreatorName',
                name = row['name'],
                surname = row['surname'],
                kodmeli = row['kodmeli'],
                gender = row['gender'],
                birth = row['birth'],
                is_imported = True,
                date_created = 'date_created',
            )

                continue  # T
            pati = Patients.objects.get(id_id=row['patientId'])
            Samples.objects.create(
                id_id = row['\ufeffid'],
                patient = pati,
                sample_code = row['sample_code'],
                name = row['name'],
                surname = row['surname'],
                kodmeli = row['kodmeli'],
                gender = row['gender'],
                birth = row['birth'],
                is_imported = row['is_imported'],
                sample_date = row['sample_date'],
                expected_result_date = row['expected_result_date'],
                result_date = row['result_date'],
                origin_lab = row['origin_lab'],
                is_sent = row['is_sent'],
                is_received = row['is_received'],
                is_reported = row['is_reported'],
                receiver_lab = row['receiver_lab'],
                emergent_status = row['emergent_status'],
                sample_hour = row['sample_hour'],
                result_hour = row['result_hour'],
                patientId = row['patientId'],

            )
            # Patients.objects.create(
            #     id_id = row['id'],
            #     user = row['patientId'],
            #     userCreatorName = row['userCreatorName'],
            #     name = row['name'],
            #     surname = row['surname'],
            #     kodmeli = row['kodmeli'],
            #     gender = row['gender'],
            #     birth = row['birth'],
            #     is_imported = row['is_imported'],
            #     date_created = row['date_created'],
            # )

if __name__ == '__main__':
    csv_file_path = 'patient_data.csv'  # Replace with your actual file path
    import_books(csv_file_path)
