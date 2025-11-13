from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Household(models.Model):
    """Stores permanent data for each household"""
    name = models.CharField(max_length=200)
    address = models.TextField()
    barangay = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    house_height_meters = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Height of the house in meters"
    )
    house_width_meters = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Width of the house in meters"
    )
    is_4ps_recipient = models.BooleanField(
        default=False,
        help_text="Whether the household is a 4Ps (Pantawid Pamilyang Pilipino Program) recipient"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.barangay}"


class DisasterEvent(models.Model):
    """Lets you create new disasters so the app is reusable"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_occurred = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_occurred']

    def __str__(self):
        return self.name


class DamageAssessment(models.Model):
    """Link between Household and DisasterEvent - stores damage status and ECT amount"""
    
    class DamageStatus(models.TextChoices):
        NONE = 'NONE', 'No Damage'
        PARTIAL = 'PARTIAL', 'Partial Damage'
        TOTAL = 'TOTAL', 'Total Damage'

    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='assessments')
    disaster = models.ForeignKey(DisasterEvent, on_delete=models.CASCADE, related_name='assessments')
    damage_status = models.CharField(max_length=10, choices=DamageStatus.choices, default=DamageStatus.NONE)
    flood_depth_meters = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Depth of flood water in meters at the household location"
    )
    recommended_ect_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10000)]
    )
    notes = models.TextField(blank=True)
    assessed_by = models.CharField(max_length=100, blank=True)
    assessed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['household', 'disaster']
        ordering = ['-assessed_at']

    def save(self, *args, **kwargs):
        """
        Automatically calculates ECT amount based on damage status.
        This is a fallback if model prediction is not available.
        - TOTAL damage = ₱10,000
        - PARTIAL damage = ₱5,000
        - NONE damage = ₱0
        """
        # Only set ECT amount if it hasn't been set by the model prediction
        # (i.e., if it's still 0 or not set)
        if not hasattr(self, '_ect_calculated') or not self._ect_calculated:
            if self.damage_status == self.DamageStatus.TOTAL:
                self.recommended_ect_amount = 10000
            elif self.damage_status == self.DamageStatus.PARTIAL:
                self.recommended_ect_amount = 5000
            else:  # NONE
                self.recommended_ect_amount = 0
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.household.name} - {self.disaster.name}: {self.damage_status} (₱{self.recommended_ect_amount})"