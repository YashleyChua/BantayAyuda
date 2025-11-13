from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.conf import settings
import requests
import json
from .models import Household, DisasterEvent, DamageAssessment
from .serializers import HouseholdSerializer, DisasterEventSerializer, DamageAssessmentSerializer

import pandas as pd
import numpy as np
from catboost import CatBoostClassifier


# --- MODEL UTILITY FUNCTIONS (Incorporated from ect_utils.py) ---


# IMPORTANT: Ensure your trained CatBoost model is saved as
# 'ect_decision_engine.cbm' and placed in a location accessible by the Django process.


def load_model(file_path):
   """
   Loads the trained CatBoost model using the load_model() method.
   If loading fails, it returns None.
   """
   try:
       # Initializing CatBoostClassifier() and then loading the model
       loaded_model = CatBoostClassifier(verbose=0)
       loaded_model.load_model(file_path)
       print(f"Model loaded from {file_path}")
       return loaded_model
   except Exception as e:
       # This occurs if the model file is missing or corrupted
       print(f"ERROR: Failed to load CatBoost model from {file_path}. Please check file location. Error: {e}")
       return None


# Attempt to load the model artifact once when the module loads
loadModel = load_model('models/ect_allocation_model_v1.bin')



def preprocess_and_predict(assessment_instance):
   """
   Prepares the input data from a Django model instance for the CatBoost model
   and returns the predicted ECT amount.

   NOTE: This function assumes the DamageAssessment instance or its linked Household
   object provides the required fields (e.g., flood_depth_meters, house_height_meters).
   """
   # Assuming assessment_instance (DamageAssessment) and its linked Household (assessment_instance.household)
   # provide the required fields for prediction logic.
  
   # 1. Gather raw data into a dictionary matching feature names
   raw_data = {
       'Barangay_ID': [assessment_instance.household.barangay],
       'Latitude': [assessment_instance.household.latitude],
       'Longitude': [assessment_instance.household.longitude],
       'Flood_Depth_Meters': [assessment_instance.flood_depth_meters],
       'House_Height_Meters': [assessment_instance.household.house_height_meters],
       'House_Width_Meters': [assessment_instance.household.house_width_meters],
       'Damage_Classification': [assessment_instance.damage_status],
       'Is_4Ps_Recipient': [int(assessment_instance.household.is_4ps_recipient)],
   }

   # 2. Convert to DataFrame (CatBoost compatible format)
   X_new = pd.DataFrame(raw_data)
  
   # 3. FEATURE ENGINEERING: Calculate the essential 'Flood_Height_Ratio'
   X_new['Flood_Height_Ratio'] = np.minimum(
       X_new['Flood_Depth_Meters'] / X_new['House_Height_Meters'],
       1.0
   )
  
   # 4. PREDICTION
   if loadModel is not None:
       prediction = loadModel.predict(X_new).flatten()[0]
   else:
       damage = str(X_new['Damage_Classification'].iloc[0]).upper().strip()
       ratio = float(X_new['Flood_Height_Ratio'].iloc[0])
       
       # Rule-based fallback
       if damage == 'NONE':
           prediction = 0
       elif damage == 'PARTIAL':
           if ratio >= 0.4 & ratio < 0.8:
               prediction = 5000
       elif damage == 'TOTAL':
           if ratio >= 0.8:
               prediction = 10000
       else:
           prediction = 0
      
   return int(prediction)

class HouseholdViewSet(viewsets.ModelViewSet):
    """
    REST API ViewSet for Household model.
    Provides CRUD operations and a custom GeoJSON endpoint for the map.
    """
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer

    @action(detail=False, methods=['get'])
    def geojson(self, request):
        """
        CRITICAL IMPLEMENTATION: Custom GeoJSON endpoint for Leaflet.js map.
        This is the "magic" that builds your map.
        
        When frontend calls /api/households/geojson/?disaster_id=1, this function:
        1. Gets all Household locations
        2. Finds their DamageAssessment for that specific disaster
        3. Bundles it all into a single GeoJSON file that Leaflet.js can read
        
        Returns GeoJSON with colored markers based on damage_status:
        - Red: Total Damage (₱10,000)
        - Orange: Partial Damage (₱5,000)
        - Green: No Damage (₱0)
        """
        disaster_id = request.query_params.get('disaster_id', None)
        
        if not disaster_id:
            return Response(
                {'error': 'disaster_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            disaster = DisasterEvent.objects.get(pk=disaster_id)
        except DisasterEvent.DoesNotExist:
            return Response(
                {'error': 'Disaster not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Build GeoJSON structure
        features = []
        
        households = Household.objects.all()
        for household in households:
            # Get assessment for this household and disaster
            try:
                assessment = DamageAssessment.objects.get(
                    household=household,
                    disaster=disaster
                )
                damage_status = assessment.damage_status
                ect_amount = float(assessment.recommended_ect_amount)
            except DamageAssessment.DoesNotExist:
                damage_status = 'NONE'
                ect_amount = 0

            # Determine color based on damage status
            if damage_status == 'TOTAL':
                color = '#dc3545'  # Red
                marker_color = 'red'
            elif damage_status == 'PARTIAL':
                color = '#fd7e14'  # Orange
                marker_color = 'orange'
            else:
                color = '#28a745'  # Green
                marker_color = 'green'

            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        float(household.longitude),
                        float(household.latitude)
                    ]
                },
                'properties': {
                    'id': household.id,
                    'name': household.name,
                    'address': household.address,
                    'barangay': household.barangay,
                    'contact_number': household.contact_number or '',
                    'damage_status': damage_status,
                    'ect_amount': ect_amount,
                    'marker_color': marker_color,
                    'popup_content': f"""
                        <strong>{household.name}</strong><br>
                        {household.address}<br>
                        <strong>Status:</strong> {damage_status}<br>
                        <strong>ECT Amount:</strong> ₱{ect_amount:,.2f}
                    """
                }
            }
            features.append(feature)

        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }

        return JsonResponse(geojson)


class DisasterEventViewSet(viewsets.ModelViewSet):
    """REST API ViewSet for DisasterEvent model."""
    queryset = DisasterEvent.objects.all()
    serializer_class = DisasterEventSerializer


class DamageAssessmentViewSet(viewsets.ModelViewSet):
    """REST API ViewSet for DamageAssessment model."""
    queryset = DamageAssessment.objects.all()
    serializer_class = DamageAssessmentSerializer

    def get_queryset(self):
        """
        Optionally filter by disaster_id or household_id
        """
        queryset = DamageAssessment.objects.all()
        disaster_id = self.request.query_params.get('disaster_id', None)
        household_id = self.request.query_params.get('household_id', None)
        
        if disaster_id:
            queryset = queryset.filter(disaster_id=disaster_id)
        if household_id:
            queryset = queryset.filter(household_id=household_id)
            
        return queryset


# Gemini API endpoint for SMS generation
@api_view(['POST'])
def generate_sms(request):
    """
    LLM Integration: Generate SMS using Gemini API.
    This implements the "Innovation" and "AI/LLM" criteria from the PDFs.
    
    Takes household data and generates an empathetic SMS message in Filipino/Tagalog.
    """
    try:
        data = request.data
        prompt = data.get('prompt', '')
        household_name = data.get('household_name', '')
        damage_status = data.get('damage_status', '')
        ect_amount = data.get('ect_amount', 0)
        
        # Get Gemini API key from settings
        api_key = getattr(settings, 'GEMINI_API_KEY', '')
        
        if not api_key:
            return Response({
                'success': False,
                'error': 'Gemini API key not configured. Please set GEMINI_API_KEY in settings.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Call Gemini API
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}'
        
        payload = {
            'contents': [{
                'parts': [{
                    'text': prompt
                }]
            }]
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract the generated text from Gemini response
            if 'candidates' in result and len(result['candidates']) > 0:
                generated_text = result['candidates'][0]['content']['parts'][0]['text']
                
                return Response({
                    'success': True,
                    'sms_message': generated_text.strip(),
                    'household_name': household_name,
                    'damage_status': damage_status,
                    'ect_amount': ect_amount
                })
            else:
                return Response({
                    'success': False,
                    'error': 'No response from Gemini API'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'success': False,
                'error': f'Gemini API error: {response.status_code} - {response.text}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)