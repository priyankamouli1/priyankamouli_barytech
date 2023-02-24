# views.py

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee, Vacation
from .serializers import EmployeeSerializer, VacationSerializer

# Create, Read, Update and Delete APIs for Employee
@api_view(['GET', 'POST'])
def employee_list(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EmployeeSerializer(employee, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=204)

# Request a vacation for a specific employee
@api_view(['POST'])
def request_vacation(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        data['employee'] = pk
        serializer = VacationSerializer(data=data)
        if serializer.is_valid():
            # Check if employee has already taken 4 vacations
            if employee.vacations.count() < 4:
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response({'error': 'Employee has already taken 4 vacations.'}, status=400)
        return Response(serializer.errors, status=400)

# Get all vacations for an employee (Either approved, pending, rejected or all)
@api_view(['GET'])
def get_vacations(request, pk, status=None):
    employee = get_object_or_404(Employee, pk=pk)

    if status:
        vacations = Vacation.objects.filter(employee=employee, status=status)
    else:
        vacations = Vacation.objects.filter(employee=employee)

    serializer = VacationSerializer(vacations, many=True)
    return Response(serializer.data)

# Design an API to search employees
@api_view(['GET'])
def search_employees(request):
    name = request.query_params.get('name', '')
    employees = Employee.objects.filter(name__icontains=name)
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

# Design an API to upload different types of files related to a vacation
@api_view(['POST'])
def upload_file(request, pk):
    vacation = get_object_or_404(Vacation, pk=pk)

    if request.method == 'POST':
        attachment = request.FILES.get('attachment')
        vacation.attachment_file_name = attachment.name
        vacation.save()
        return JsonResponse({'success': 'File uploaded successfully.'})
    return JsonResponse({'error': 'Unable to upload file.'})
