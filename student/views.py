from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
from .serializers import *
from sms.pagination import CustomPagination
from rest_framework import status
from authentication.models import Authentication
from rest_framework.response import Response

# Create your views here.
class StudentList(generics.ListCreateAPIView):
    serializer_class = StudentViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Student.objects.filter(status=True).order_by('id')
        try:
            user_id = self.request.query_params.get('user')
            users = Authentication.objects.get(id=user_id)
            if users.institution and users.branch:
                queryset = queryset.filter(institution=users.institution, branch=users.branch)
        except:
            pass
        return queryset
    def list(self,request,*args, **kwargs):
        # serializer_class = TokenObtainPairView  # Create this serializer
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data).data
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                "code": 200,
                "message": "Success",
                "data": serializer.data,
                "pagination": {
                    "next": None,
                    "previous": None,
                    "count": queryset.count(),
                },
            }

        return Response(response_data)
    
    def create(self,request,*args, **kwargs):
        data = request.data
        student_data = data.copy()
        first_name = student_data.get('first_name')
        last_name = student_data.get('last_name')
        is_active = student_data.get('is_active', True) 
        user_type = student_data.get('user_type', 'STUDENT') 
        guardians_data = student_data.pop('guardians', [])
        # Create the student
        serializer_class = StudentSerializer
        student_serializer = serializer_class(data=student_data)
        # student_serializer = self.get_serializer(data=student_data)
        try:
            if student_serializer.is_valid():
                student_serializer.is_valid(raise_exception=True)
                institution_data = student_serializer.validated_data.get('institution')
                branch_data = student_serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                student = student_serializer.save(institution=institution, branch=branch)
                try:
                    std_user_data = Student.objects.values('student_no').get(id=student.id)
                    std_username = std_user_data['student_no']
                    default_password = '12345678'
                    user_count = Authentication.objects.filter(username=std_username).count()
                    if(user_count==0):
                        user = Authentication(username=std_username,first_name=first_name,last_name=last_name,user_type=user_type,is_active=is_active,institution=institution, branch=branch)
                        # Set a default password (you can change this as needed)
                        user.set_password(default_password)
                        user.save()
                        # Update the student's user_id field
                        student.user_id = user.id
                        student.save()
                    else:
                        last_username = Authentication.objects.filter(username__startswith='77').order_by('username').last()
                        # int_last_username = int(last_username)
                        int_last_username = int(last_username.username)
                        new_username = (int_last_username+1)
                        user = Authentication(username=new_username,first_name=first_name,last_name=last_name,user_type=user_type,is_active=is_active,institution=institution,branch=branch)
                        # Set a default password (you can change this as needed)
                        user.set_password(default_password)
                        user.save()
                        # Update the student's user_id field
                        student.user_id = user.id
                        student.student_no = new_username
                        student.save()
                except:
                    pass
                # Create the guardian and associate with the student
                guardians = []
                for guardian_data in guardians_data:
                    ga_first_name = guardian_data.get('first_name')
                    ga_last_name = guardian_data.get('last_name')
                    ga_is_active = guardian_data.get('is_active', True) 
                    ga_user_type = guardian_data.get('user_type', 'GUARDIAN') 
                    ga_is_guardian = guardian_data.get('is_guardian') 
                    guardian_data['student'] = student.id
                    guardian_serializer = GuardianSerializer(data=guardian_data)
                    guardian_serializer.is_valid(raise_exception=True)
                    guardian = guardian_serializer.save()
                    if ga_is_guardian:
                        try:
                            default_password = '12345678'
                            ga_user_data = Guardian.objects.values('guardian_no').get(id=guardian.id)
                            ga_username = ga_user_data['guardian_no']
                            ga_count = Authentication.objects.filter(username=ga_username).count()
                            if(ga_count==0):
                                ga_user = Authentication(username=ga_username,first_name=ga_first_name,last_name=ga_last_name,user_type=ga_user_type,is_active=ga_is_active,institution=institution, branch=branch)
                                # Set a default password (you can change this as needed)
                                ga_user.set_password(default_password)
                                ga_user.save()
                                # Update the Guardian's user_id field
                                guardian.user_id = ga_user.id
                                guardian.save()
                            else:
                                last_ga_username = Authentication.objects.filter(username__startswith='11').order_by('username').last()
                                int_last_ga_username = int(last_ga_username.username)
                                new_ga_username = (int_last_ga_username+1)
                                user = Authentication(username=new_ga_username,first_name=first_name,last_name=last_name,user_type=user_type,is_active=is_active,institution=institution,branch=branch)
                                # Set a default password (you can change this as needed)
                                user.set_password(default_password)
                                user.save()
                                # Update the student's user_id field
                                guardian.user_id = user.id
                                guardian.guardian_no = new_ga_username
                                guardian.save()
                        except:
                            pass
                    guardians.append(guardian)
                response_data = student_serializer.data
                response_data['guardians'] = GuardianSerializer(guardians, many=True).data
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))
            
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    
class StudentDetail(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=StudentViewSerializer(instance).data)
    
    def update(self, request, *args, **kwargs):
        # Get the student instance
        student = self.get_object()
        # Deserialize the updated student data
        student_serializer = self.get_serializer(student, data=request.data, partial=True)
        student_serializer.is_valid(raise_exception=True)
        instance = student_serializer.save()
        # Deserialize the updated guardian data
        guardian_data = request.data.get('guardians')
        enroll_data = request.data.get('enroll')
        if enroll_data:
            for enroll_item in enroll_data:
                enroll_id = enroll_item.get('id')
                if enroll_id:
                    enroll = StudentEnroll.objects.get(id=enroll_id, student=student)
                    enroll_serializer = StudentEnrollSerialize(enroll, data=enroll_item, partial=True)
                    enroll_serializer.is_valid(raise_exception=True)
                    enroll_serializer.save()
                else:
                    enroll_serializer = StudentEnrollSerialize(data=enroll_item)
                    enroll_serializer.is_valid(raise_exception=True)
                    enroll_serializer.save()

        if guardian_data:
            for guardian_item in guardian_data:
                guardian_id = guardian_item.get('id')
                if guardian_id:
                    try:
                        guardian = Guardian.objects.get(id=guardian_id, student=student)
                        guardian_serializer = GuardianSerializer(guardian, data=guardian_item, partial=True)
                        guardian_serializer.is_valid(raise_exception=True)
                        guardian_serializer.save()
                    except Guardian.DoesNotExist:
                        pass
                else:
                    ga_first_name = guardian_item.get('first_name')
                    ga_last_name = guardian_item.get('last_name')
                    ga_is_active = guardian_item.get('is_active', True) 
                    ga_user_type = guardian_item.get('user_type', 'GUARDIAN') 
                    ga_is_guardian = guardian_item.get('is_guardian')
                    # If no guardian ID provided, create a new guardian for the student
                    guardian_item['student'] = student.id
                    guardian_serializer = GuardianSerializer(data=guardian_item)
                    guardian_serializer.is_valid(raise_exception=True)
                    guardian = guardian_serializer.save()
                    if ga_is_guardian:
                        try:
                            ga_user_data = Guardian.objects.values('guardian_no').get(id=guardian.id)
                            ga_username = ga_user_data['guardian_no']
                            ga_user = Authentication(username=ga_username,first_name=ga_first_name,last_name=ga_last_name,user_type=ga_user_type,is_active=ga_is_active)
                            # Set a default password (you can change this as needed)
                            default_password = '12345678'
                            ga_user.set_password(default_password)
                            ga_user.save()
                            # Update the Guardian's user_id field
                            guardian.user_id = ga_user.id
                            guardian.save()
                        except:
                            pass
        return CustomResponse(code=status.HTTP_200_OK, message="Student updated successfully", data=StudentViewSerializer(instance).data)