from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from .models import Companies_db, People_db
import ast

# Django app views
# View for the initial main page
class IndexView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['intro_text'] = 'REST API testing to get information about Paranuara'
        return context

# View for getting information about company employees of given company
class GetCompanyEmployees(APIView):
    # Link the serializer
    serializer_class = serializers.Q1_serializer

    def get(self, request, format=None):
        place_holder_text = 'Query for information by filling in the field(s) below, and click Post.'
        return Response(place_holder_text)

    def post(self, request):
        # Get the model data
        companies_data = Companies_db.objects.all()
        people_data = People_db.objects.all()
        
        serializer = serializers.Q1_serializer(data=request.data)
  
        if serializer.is_valid():
            company_data = serializer.data.get('company_name')
            company_name = '{0}'.format(company_data).upper()
            company_name = company_name.replace(' ', '')
            employees_names = get_company_employees(company_name, companies_data, people_data)
            return Response({
                'company' : company_name,
                'employees' : employees_names
            })
        else:
            Response(serializer_q1.errors, status=status.HTTP_400_BAD_REQUEST)

# View for getting information about common friends of two given people sharing specific criteria
class GetCommonFriends(APIView):
    # Link the serializer
    serializer_class = serializers.Q2_serializer

    def get(self, request, format=None):
        place_holder_text = 'Query for information by filling in the field(s) below, and click Post.'
        return Response(place_holder_text)

    def post(self, request):
        # Get the model data
        people_data = People_db.objects.all()

        serializer = serializers.Q2_serializer(data=request.data)

        if serializer.is_valid():
            person_1_data = serializer.data.get('person_1_name')
            person_2_data = serializer.data.get('person_2_name')
            person_1_name = '{0}'.format(person_1_data)
            person_2_name = '{0}'.format(person_2_data)

            # Retrieve person information
            person_1_details, _ = get_person_details(person_1_name.title(), people_data)
            person_2_details, _ = get_person_details(person_2_name.title(), people_data)

            # Get common friends index as a list
            common_friends_index = get_common_friends(person_1_name.title(), person_2_name.title(), people_data)          

            # Filter on common friends as being alive and having brown eye colour
            if common_friends_index[0] != 'none':
                common_group = people_data.filter(
                    index__in=common_friends_index,
                    has_died=False,
                    eye_color__in=['brown']
                )

                # Get common friends between person 1 and person 2 that satisfies specified criteria
                common_group_friends = list(common_group.values_list('name', flat=True))
            else:
                common_group_friends = ['not found']

            return Response({
                'person 1' : person_1_details,
                'person 2' : person_2_details,
                'common friends (alive & with brown eyes)' : common_group_friends
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for getting information about favourite fruits and vegetables of given person
class GetFavFruitsVegetables(APIView):
    # Link the serializer
    serializer_class = serializers.Q3_serializer

    def get(self, request, format=None):
        place_holder_text = 'Query for information by filling in the field(s) below, and click Post.'
        return Response(place_holder_text)

    def post(self, request):
        # Get the model data
        people_data = People_db.objects.all()

        serializer = serializers.Q3_serializer(data=request.data)

        if serializer.is_valid():
            person_data = serializer.data.get('person_name')
            person_name = '{0}'.format(person_data)

            # Retrieve person information (with food information)
            _, person_details_food = get_person_details(person_name.title(), people_data)

            return Response(person_details_food)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Function to get common friends as list
def get_common_friends(person_1, person_2, people_data):
    common_group = people_data.filter(name__in=[person_1, person_2])

    if len(common_group) > 1:
        person_1_friends = common_group.values()[0]['friends']
        person_1_friends = ast.literal_eval(person_1_friends)
        person_2_friends = common_group.values()[1]['friends']
        person_2_friends = ast.literal_eval(person_2_friends)
        if len(person_1_friends) > 0 and len(person_2_friends) > 0:
            common_friends_index = [ friend['index'] for friend in person_1_friends if friend in person_2_friends ]
        else:
            common_friends_index = ['none']
    else:
        common_friends_index = ['none']
    return common_friends_index

# Function to get information about an individual person
def get_person_details(person_name, people_data):
    common_fruits = [
        'apple',
        'banana',
        'orange',
        'strawberry',
        'avocado',
        'apricot',
        'blackberry',
        'coconut',
        'cranberry',
        'cucumber',
        'dragonfruit',
        'grape',
        'lemon',
        'peach',
        'pear',
        'pineapple'
    ]
    common_vegetables = [
        'asparagus',
        'beetroot',
        'broccoli',
        'cabbage',
        'cauliflower',
        'celery',
        'garlic',
        'ginger',
        'lettuce',
        'onion',
        'shallot',
        'peas',
        'potato',
        'pumpkin',
        'zucchini'
    ]
    
    person_info = people_data.filter(name__in=[person_name])
    
    if len(person_info) > 0:
        person_age = person_info.values()[0]['age']
        person_address = person_info.values()[0]['address']
        person_phone = person_info.values()[0]['phone']
        person_favfood = ast.literal_eval(person_info.values()[0]['favourite_food'])
        person_fruits = [ food for food in person_favfood if food.lower() in common_fruits ]
        person_vegetables = [ food for food in person_favfood if food.lower() in common_vegetables ]
        person_details = {
            'name' : person_name,
            'age' : person_age,
            'address' : person_address,
            'phone' : person_phone
        }
        person_details_food = {
            'username' : person_name,
            'age' : person_age,
            'fruits' : person_fruits,
            'vegetables' : person_vegetables
        }
    else:
        person_details = {
            'name' : person_name,
            'age' : 'not found',
            'address' : 'not found',
            'phone' : 'not found'
        }
        person_details_food = {
            'username' : person_name,
            'age' : 'not found',
            'fruits' : 'not found',
            'vegetables' : 'not found'
        }
    return person_details, person_details_food

# Function to get the company employees
def get_company_employees(company_name, companies_data, people_data):
    company_match = companies_data.filter(company_name=company_name)

    if len(company_match) > 0:
        company_index = company_match.values()[0]['index']
        employees_match = people_data.filter(company_id=company_index)
        if len(employees_match) > 0:
            employees_names = list(employees_match.values_list('name', flat=True))
        else:
            employees_names = ['no employees found']
    else:
        employees_names = ['no company found, no employees found']

    return employees_names