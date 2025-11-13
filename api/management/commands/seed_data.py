"""
Management command to seed sample data for BantayAyuda.
Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from api.models import Household, DisasterEvent, DamageAssessment
from api.views import preprocess_and_predict
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seeds the database with sample disaster data, households, and damage assessments'

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed sample data...')
        
        disaster, created = DisasterEvent.objects.get_or_create(
            name='Typhoon Uwan',
            defaults={
                'description': 'A severe typhoon that affected multiple barangays in Metro Manila',
                'date_occurred': '2024-11-01',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created disaster: {disaster.name}'))
        else:
            self.stdout.write(f'→ Disaster already exists: {disaster.name}')
        
        # Sample households in Metro Manila area with house dimensions
        households_data = [
            {
                'name': 'Juan Dela Cruz',
                'address': '123 Rizal Street, Barangay 1',
                'barangay': 'Barangay 1',
                'latitude': Decimal('14.5995'),
                'longitude': Decimal('120.9842'),
                'contact_number': '+639171234567',
                'house_height_meters': Decimal('4.50'),
                'house_width_meters': Decimal('6.00'),
                'is_4ps_recipient': True
            },
            {
                'name': 'Maria Santos',
                'address': '456 Mabini Avenue, Barangay 2',
                'barangay': 'Barangay 2',
                'latitude': Decimal('14.6042'),
                'longitude': Decimal('120.9822'),
                'contact_number': '+639172345678',
                'house_height_meters': Decimal('3.80'),
                'house_width_meters': Decimal('5.50'),
                'is_4ps_recipient': False
            },
            {
                'name': 'Pedro Garcia',
                'address': '789 Bonifacio Street, Barangay 3',
                'barangay': 'Barangay 3',
                'latitude': Decimal('14.5948'),
                'longitude': Decimal('120.9862'),
                'contact_number': '+639173456789',
                'house_height_meters': Decimal('5.20'),
                'house_width_meters': Decimal('7.00'),
                'is_4ps_recipient': True
            },
            {
                'name': 'Ana Rodriguez',
                'address': '321 Quezon Boulevard, Barangay 4',
                'barangay': 'Barangay 4',
                'latitude': Decimal('14.6095'),
                'longitude': Decimal('120.9802'),
                'contact_number': '+639174567890',
                'house_height_meters': Decimal('4.00'),
                'house_width_meters': Decimal('6.50'),
                'is_4ps_recipient': False
            },
            {
                'name': 'Carlos Mendoza',
                'address': '654 Aguinaldo Street, Barangay 5',
                'barangay': 'Barangay 5',
                'latitude': Decimal('14.5895'),
                'longitude': Decimal('120.9882'),
                'contact_number': '+639175678901',
                'house_height_meters': Decimal('3.50'),
                'house_width_meters': Decimal('5.00'),
                'is_4ps_recipient': True
            },
            {
                'name': 'Rosa Villanueva',
                'address': '987 Luna Street, Barangay 1',
                'barangay': 'Barangay 1',
                'latitude': Decimal('14.6025'),
                'longitude': Decimal('120.9852'),
                'contact_number': '+639176789012',
                'house_height_meters': Decimal('4.75'),
                'house_width_meters': Decimal('6.75'),
                'is_4ps_recipient': False
            },
            {
                'name': 'Jose Torres',
                'address': '147 Panganiban Street, Barangay 2',
                'barangay': 'Barangay 2',
                'latitude': Decimal('14.5965'),
                'longitude': Decimal('120.9832'),
                'contact_number': '+639177890123',
                'house_height_meters': Decimal('3.90'),
                'house_width_meters': Decimal('5.75'),
                'is_4ps_recipient': True
            },
            {
                'name': 'Lourdes Fernandez',
                'address': '258 Roxas Avenue, Barangay 3',
                'barangay': 'Barangay 3',
                'latitude': Decimal('14.6075'),
                'longitude': Decimal('120.9812'),
                'contact_number': '+639178901234',
                'house_height_meters': Decimal('5.00'),
                'house_width_meters': Decimal('7.25'),
                'is_4ps_recipient': False
            },
            {
                'name': 'Roberto Cruz',
                'address': '369 Taft Avenue, Barangay 4',
                'barangay': 'Barangay 4',
                'latitude': Decimal('14.5925'),
                'longitude': Decimal('120.9872'),
                'contact_number': '+639179012345',
                'house_height_meters': Decimal('4.25'),
                'house_width_meters': Decimal('6.25'),
                'is_4ps_recipient': True
            },
            {
                'name': 'Carmen Reyes',
                'address': '741 EDSA, Barangay 5',
                'barangay': 'Barangay 5',
                'latitude': Decimal('14.6115'),
                'longitude': Decimal('120.9792'),
                'contact_number': '+639170123456',
                'house_height_meters': Decimal('3.70'),
                'house_width_meters': Decimal('5.25'),
                'is_4ps_recipient': False
            },
            {
                'name': 'Miguel Ocampo',
                'address': '852 Ayala Avenue, Barangay 1',
                'barangay': 'Barangay 1',
                'latitude': Decimal('14.6008'),
                'longitude': Decimal('120.9865'),
                'contact_number': '+639181234567',
                'house_height_meters': Decimal('4.60'),
                'house_width_meters': Decimal('6.25'),
                'is_4ps_recipient': True
            },
            {
                'name': 'Sofia Reyes',
                'address': '963 Makati Road, Barangay 2',
                'barangay': 'Barangay 2',
                'latitude': Decimal('14.6055'),
                'longitude': Decimal('120.9835'),
                'contact_number': '+639182345678',
                'house_height_meters': Decimal('3.95'),
                'house_width_meters': Decimal('5.80'),
                'is_4ps_recipient': False
            },
            {
                'name': 'Fernando Lopez',
                'address': '147 BGC Road, Barangay 3',
                'barangay': 'Barangay 3',
                'latitude': Decimal('14.5965'),
                'longitude': Decimal('120.9875'),
                'contact_number': '+639183456789',
                'house_height_meters': Decimal('5.10'),
                'house_width_meters': Decimal('7.15'),
                'is_4ps_recipient': True
            },
            {
                'name': 'Angelica Bautista',
                'address': '258 Ortigas Center, Barangay 4',
                'barangay': 'Barangay 4',
                'latitude': Decimal('14.6105'),
                'longitude': Decimal('120.9815'),
                'contact_number': '+639184567890',
                'house_height_meters': Decimal('4.10'),
                'house_width_meters': Decimal('6.60'),
                'is_4ps_recipient': False
            },
            {
                'name': 'David Gutierrez',
                'address': '369 Commonwealth Avenue, Barangay 5',
                'barangay': 'Barangay 5',
                'latitude': Decimal('14.5910'),
                'longitude': Decimal('120.9890'),
                'contact_number': '+639185678901',
                'house_height_meters': Decimal('3.65'),
                'house_width_meters': Decimal('5.35'),
                'is_4ps_recipient': True
            },
            {
                'name': 'Elena Villanueva',
                'address': '741 Cubao Avenue, Barangay 1',
                'barangay': 'Barangay 1',
                'latitude': Decimal('14.6038'),
                'longitude': Decimal('120.9850'),
                'contact_number': '+639186789012',
                'house_height_meters': Decimal('4.80'),
                'house_width_meters': Decimal('6.90'),
                'is_4ps_recipient': False
            },
            {
                'name': 'Ricardo Sanchez',
                'address': '852 Pasay Road, Barangay 2',
                'barangay': 'Barangay 2',
                'latitude': Decimal('14.5975'),
                'longitude': Decimal('120.9825'),
                'contact_number': '+639187890123',
                'house_height_meters': Decimal('3.85'),
                'house_width_meters': Decimal('5.65'),
                'is_4ps_recipient': True
            },
            {
                'name': 'Graciela Morales',
                'address': '963 Libis Street, Barangay 3',
                'barangay': 'Barangay 3',
                'latitude': Decimal('14.6085'),
                'longitude': Decimal('120.9865'),
                'contact_number': '+639188901234',
                'house_height_meters': Decimal('5.05'),
                'house_width_meters': Decimal('7.35'),
                'is_4ps_recipient': False
            },
            {
                'name': 'Antonio Navarro',
                'address': '147 Suez Road, Barangay 4',
                'barangay': 'Barangay 4',
                'latitude': Decimal('14.5935'),
                'longitude': Decimal('120.9860'),
                'contact_number': '+639189012345',
                'house_height_meters': Decimal('4.30'),
                'house_width_meters': Decimal('6.40'),
                'is_4ps_recipient': True
            },
            {
                'name': 'Mariana Diaz',
                'address': '258 Kamagayan Street, Barangay 5',
                'barangay': 'Barangay 5',
                'latitude': Decimal('14.6125'),
                'longitude': Decimal('120.9800'),
                'contact_number': '+639180123456',
                'house_height_meters': Decimal('3.75'),
                'house_width_meters': Decimal('5.45'),
                'is_4ps_recipient': False
            },
        ]
        
        created_households = 0
        for household_data in households_data:
            household, created = Household.objects.get_or_create(
                name=household_data['name'],
                address=household_data['address'],
                defaults=household_data
            )
            if created:
                created_households += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created household: {household.name} '
                        f'(Height: {household.house_height_meters}m, Width: {household.house_width_meters}m)'
                    )
                )
        
        self.stdout.write(f'→ Created {created_households} new households')
        self.stdout.write('')
        
        # Create Damage Assessments with different statuses and flood depths
        households = Household.objects.all()
        assessment_data = [
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('2.50')},
            {'status': DamageAssessment.DamageStatus.TOTAL, 'flood_depth': Decimal('0.85')},
            {'status': DamageAssessment.DamageStatus.TOTAL, 'flood_depth': Decimal('0.95')},
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('2.75')},
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('0.20')},
            {'status': DamageAssessment.DamageStatus.TOTAL, 'flood_depth': Decimal('0.75')},
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('2.30')},
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('0.15')},
            {'status': DamageAssessment.DamageStatus.TOTAL, 'flood_depth': Decimal('1.05')},
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('0.10')},
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('2.65')},
            {'status': DamageAssessment.DamageStatus.TOTAL, 'flood_depth': Decimal('0.90')},
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('2.45')},
            {'status': DamageAssessment.DamageStatus.TOTAL, 'flood_depth': Decimal('0.80')},
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('0.25')},
            {'status': DamageAssessment.DamageStatus.TOTAL, 'flood_depth': Decimal('1.15')},
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('2.55')},
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('0.18')},
            {'status': DamageAssessment.DamageStatus.TOTAL, 'flood_depth': Decimal('0.88')},
            {'status': DamageAssessment.DamageStatus.PARTIAL, 'flood_depth': Decimal('0.12')},
        ]
        
        created_assessments = 0
        for i, household in enumerate(households):
            data = assessment_data[i % len(assessment_data)]
            status = data['status']
            flood_depth = data['flood_depth']
            
            assessment, created = DamageAssessment.objects.get_or_create(
                household=household,
                disaster=disaster,
                defaults={
                    'damage_status': status,
                    'flood_depth_meters': flood_depth,
                    'notes': f'Sample assessment for {household.name}. Flood depth: {flood_depth}m',
                    'assessed_by': 'DSWD Assessment Team'
                }
            )
            if created:
                created_assessments += 1
                
                try:
                    ect_amount = preprocess_and_predict(assessment)
                    assessment.recommended_ect_amount = ect_amount
                    assessment._ect_calculated = True
                    assessment.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Created assessment: {household.name} - {status} | '
                            f'Flood: {flood_depth}m | ECT: ₱{ect_amount}'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠ Created assessment: {household.name} - {status} | '
                            f'Flood: {flood_depth}m | ECT: ₱{assessment.recommended_ect_amount} (error: {str(e)})'
                        )
                    )
        
        self.stdout.write('')
        self.stdout.write(f'→ Created {created_assessments} new damage assessments')
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n✓ Sample data seeding completed!'))
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'  - Disasters: {DisasterEvent.objects.count()}')
        self.stdout.write(f'  - Households: {Household.objects.count()}')
        self.stdout.write(f'  - Damage Assessments: {DamageAssessment.objects.count()}')