import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from datetime import timedelta
from patients.models import Patient
from labs.models import Lab
from tests_definitions.models import TestInfo
from samples.models import Sample, SampleTest  # Adjust the import based on your app name
from samples.models import SAMPLE_STATUSES  # Import SAMPLE_STATUSES


class Command(BaseCommand):
    help = 'Generate fake patient data and associated samples'

    def add_arguments(self, parser):
        parser.add_argument('--patients', type=int, help='Number of patients to create', default=100)
        parser.add_argument('--samples_per_patient', type=int, help='Number of samples per patient', default=2)
        parser.add_argument('--tests_per_sample', type=int, help='Number of tests per sample', default=3)

    def handle(self, *args, **options):
        fake = Faker()
        num_patients = options['patients']
        samples_per_patient = options['samples_per_patient']
        tests_per_sample = options['tests_per_sample']

        # Pre-fetch labs and tests to optimize DB queries
        origin_labs = list(Lab.objects.all())
        receiver_labs = list(Lab.objects.all())
        test_infos = list(TestInfo.objects.all())

        if not origin_labs:
            self.stdout.write(self.style.ERROR('No labs found. Please add labs before running this command.'))
            return

        if not test_infos:
            self.stdout.write(self.style.ERROR('No tests found. Please add tests before running this command.'))
            return

        used_ssns = set()  # Track used SSNs to ensure uniqueness
        used_sample_codes = set()  # Track used sample codes to ensure uniqueness


        for _ in range(num_patients):
            # Generate realistic patient data
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            # Ensure unique SSN
            national_id = fake.ssn()
            while national_id in used_ssns:
                national_id = fake.ssn()
            used_ssns.add(national_id)

            # date_of_birth = fake.date_of_birth(minimum_age=0, maximum_age=100)
            date_of_birth = fake.date_time_between(start_date='-100y', end_date='today')
    
            gender = random.choice(['M', 'F', 'Other'])
            phone_number = fake.phone_number()

            patient = Patient.objects.create(
                first_name=first_name,
                last_name=last_name,
                national_id=national_id,
                date_of_birth=date_of_birth,
                gender=gender,
                phone_number=phone_number
            )
            self.stdout.write(self.style.SUCCESS(f'Created Patient: {patient}'))
            for _ in range(samples_per_patient):
                # Ensure unique sample code
                sample_code = fake.bothify(text='SAMPLE-#####')
                while sample_code in used_sample_codes:
                    sample_code = fake.bothify(text='SAMPLE-#####')
                used_sample_codes.add(sample_code)

                origin_lab = random.choice(origin_labs)
                receiver_lab = random.choice(receiver_labs + [None])  # Some samples may not have a receiver lab
                status = random.choice([choice[0] for choice in SAMPLE_STATUSES])
                emergent_status = random.choice([True, False])
                history = fake.text(max_nb_chars=200)
                sample_type = random.choice(['Blood', 'Urine', 'Saliva', 'Tissue', 'Other'])
                sample_date = fake.date_time_between(start_date='-1y', end_date='now')
                expected_result_date = sample_date + timedelta(days=random.randint(1, 7))
                result_date = None
                if status in ['COMPLETED', 'REPORTED']:
                    result_date = expected_result_date + timedelta(days=random.randint(0, 3))

                sample = Sample.objects.create(
                    sample_code=sample_code,
                    patient=patient,
                    origin_lab=origin_lab,
                    receiver_lab=receiver_lab,
                    status=status,
                    emergent_status=emergent_status,
                    history=history,
                    sample_type=sample_type,
                    sample_date=sample_date,
                    expected_result_date=expected_result_date,
                    result_date=result_date
                )

            # for _ in range(samples_per_patient):
            #     # Generate realistic sample data
            #     sample_code = fake. unique.bothify(text='SAMPLE-#####')
            #     origin_lab = random.choice(origin_labs)
            #     receiver_lab = random.choice(receiver_labs + [None])  # Some samples may not have a receiver lab
            #     status = random.choice([choice[0] for choice in SAMPLE_STATUSES])
            #     emergent_status = random.choice([True, False])
            #     history = fake.text(max_nb_chars=200)
            #     sample_type = random.choice(['Blood', 'Urine', 'Saliva', 'Tissue', 'Other'])
            #     sample_date = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.utc)
            #     expected_result_date = sample_date + timedelta(days=random.randint(1, 7))
            #     result_date = None
            #     if status in ['COMPLETED', 'REPORTED']:
            #         result_date = expected_result_date + timedelta(days=random.randint(0, 3))

            #     sample = Sample.objects.create(
            #         sample_code=sample_code,
            #         patient=patient,
            #         origin_lab=origin_lab,
            #         receiver_lab=receiver_lab,
            #         status=status,
            #         emergent_status=emergent_status,
            #         history=history,
            #         sample_type=sample_type,
            #         sample_date=sample_date,
            #         expected_result_date=expected_result_date,
            #         result_date=result_date
            #     )

                self.stdout.write(self.style.SUCCESS(f'  Created Sample: {sample}'))

                # Assign tests to the sample
                selected_tests = random.sample(test_infos, min(tests_per_sample, len(test_infos)))
                for test_info in selected_tests:
                    result_value = fake.random_number(digits=5) if test_info.unit else None
                    result_file = None  # You can handle file attachments if needed
                    started_at = sample_date + timedelta(hours=random.randint(1, 24))
                    completed_at = started_at + timedelta(hours=random.randint(1, 48))
                    notes = fake.sentence()

                    SampleTest.objects.create(
                        sample=sample,
                        test_info=test_info,
                        result_value=str(result_value) if result_value else None,
                        started_at=started_at,
                        completed_at=completed_at,
                        notes=notes
                    )

                self.stdout.write(self.style.SUCCESS(f'    Assigned {len(selected_tests)} tests to Sample {sample.sample_code}'))

        self.stdout.write(self.style.SUCCESS('Fake data generation completed successfully.'))
