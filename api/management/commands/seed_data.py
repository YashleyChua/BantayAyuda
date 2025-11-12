"""
Management command to seed sample data for BantayAyuda.
Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from api.models import Household, DisasterEvent, DamageAssessment
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seeds the database with sample disaster data, households, and damage assessments'

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed sample data...')
        
        # Create Disaster Event
        disaster, created = DisasterEvent.objects.get_or_create(
            name='Typhoon Rosing',
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
        
        # Sample households in Metro Manila area
        households_data = [
            {
                'name': 'Juan Dela Cruz',
                'address': '123 Rizal Street, Barangay 1',
                'barangay': 'Barangay 1',
                'latitude': Decimal('14.5995'),
                'longitude': Decimal('120.9842'),
                'contact_number': '+639171234567'
            },
            {
                'name': 'Maria Santos',
                'address': '456 Mabini Avenue, Barangay 2',
                'barangay': 'Barangay 2',
                'latitude': Decimal('14.6042'),
                'longitude': Decimal('120.9822'),
                'contact_number': '+639172345678'
            },
            {
                'name': 'Pedro Garcia',
                'address': '789 Bonifacio Street, Barangay 3',
                'barangay': 'Barangay 3',
                'latitude': Decimal('14.5948'),
                'longitude': Decimal('120.9862'),
                'contact_number': '+639173456789'
            },
            {
                'name': 'Ana Rodriguez',
                'address': '321 Quezon Boulevard, Barangay 4',
                'barangay': 'Barangay 4',
                'latitude': Decimal('14.6095'),
                'longitude': Decimal('120.9802'),
                'contact_number': '+639174567890'
            },
            {
                'name': 'Carlos Mendoza',
                'address': '654 Aguinaldo Street, Barangay 5',
                'barangay': 'Barangay 5',
                'latitude': Decimal('14.5895'),
                'longitude': Decimal('120.9882'),
                'contact_number': '+639175678901'
            },
            {
                'name': 'Rosa Villanueva',
                'address': '987 Luna Street, Barangay 1',
                'barangay': 'Barangay 1',
                'latitude': Decimal('14.6025'),
                'longitude': Decimal('120.9852'),
                'contact_number': '+639176789012'
            },
            {
                'name': 'Jose Torres',
                'address': '147 Panganiban Street, Barangay 2',
                'barangay': 'Barangay 2',
                'latitude': Decimal('14.5965'),
                'longitude': Decimal('120.9832'),
                'contact_number': '+639177890123'
            },
            {
                'name': 'Lourdes Fernandez',
                'address': '258 Roxas Avenue, Barangay 3',
                'barangay': 'Barangay 3',
                'latitude': Decimal('14.6075'),
                'longitude': Decimal('120.9812'),
                'contact_number': '+639178901234'
            },
            {
                'name': 'Roberto Cruz',
                'address': '369 Taft Avenue, Barangay 4',
                'barangay': 'Barangay 4',
                'latitude': Decimal('14.5925'),
                'longitude': Decimal('120.9872'),
                'contact_number': '+639179012345'
            },
            {
                'name': 'Carmen Reyes',
                'address': '741 EDSA, Barangay 5',
                'barangay': 'Barangay 5',
                'latitude': Decimal('14.6115'),
                'longitude': Decimal('120.9792'),
                'contact_number': '+639170123456'
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
                self.stdout.write(self.style.SUCCESS(f'✓ Created household: {household.name}'))
        
        self.stdout.write(f'→ Created {created_households} new households')
        
        # Create Damage Assessments with different statuses
        households = Household.objects.all()
        damage_statuses = [
            DamageAssessment.DamageStatus.TOTAL,
            DamageAssessment.DamageStatus.PARTIAL,
            DamageAssessment.DamageStatus.PARTIAL,
            DamageAssessment.DamageStatus.TOTAL,
            DamageAssessment.DamageStatus.NONE,
            DamageAssessment.DamageStatus.PARTIAL,
            DamageAssessment.DamageStatus.TOTAL,
            DamageAssessment.DamageStatus.NONE,
            DamageAssessment.DamageStatus.PARTIAL,
            DamageAssessment.DamageStatus.NONE,
        ]
        
        created_assessments = 0
        for i, household in enumerate(households):
            status = damage_statuses[i % len(damage_statuses)]
            assessment, created = DamageAssessment.objects.get_or_create(
                household=household,
                disaster=disaster,
                defaults={
                    'damage_status': status,
                    'notes': f'Sample assessment for {household.name}',
                    'assessed_by': 'System Admin'
                }
            )
            if created:
                created_assessments += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created assessment: {household.name} - {status} (₱{assessment.recommended_ect_amount})'
                    )
                )
        
        self.stdout.write(f'→ Created {created_assessments} new damage assessments')
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n✓ Sample data seeding completed!'))
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'  - Disasters: {DisasterEvent.objects.count()}')
        self.stdout.write(f'  - Households: {Household.objects.count()}')
        self.stdout.write(f'  - Damage Assessments: {DamageAssessment.objects.count()}')
        self.stdout.write(f'\nYou can now access the dashboard at http://localhost:8000/')

