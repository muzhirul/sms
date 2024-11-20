from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
from staff.models import *
from .serializers import *
from rest_framework import status
from sms.permission import check_permission
from sms.pagination import CustomPagination
from rest_framework.response import Response
from django.db.models import Q

# Create your views here.
'''
For Account Bank
'''
class BankList(generics.ListAPIView):
    serializer_class = AccountBankViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = AccountBank.objects.filter(status=True).order_by('-id')
        return queryset

    def list(self, request, *args, **kwargs):
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

class BankCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = AccountBankSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = AccountBank.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Bank', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        
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
    
    def create(self, request, *args, **kwargs):
        '''Check user has permission to Create start'''
        permission_check = check_permission(self.request.user.id, 'Bank', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                bank_name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                bank_count = AccountBank.objects.filter(name__iexact=bank_name,institution=institution,branch=branch,status=True).count()
                if(bank_count==0):
                    instance = serializer.save(institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Bank create successfully", data=AccountBankSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Bank {bank_name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class BankDetail(generics.RetrieveUpdateAPIView):
    queryset = AccountBank.objects.all()
    serializer_class = AccountBankSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Bank', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=AccountBankSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Bank', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                bank_name = serializer.validated_data.get('bank')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                bank_count = AccountBank.objects.filter(name__iexact=bank_name,institution=institution,branch=branch,status=True).count()
                if(bank_count==0):
                    # Perform any custom update logic here if needed
                    instance = serializer.save()
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Bank Update successfully", data=AccountBankSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Bank {bank_name} already exits", data=serializer.errors)
                # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))
    
class BankDelete(generics.UpdateAPIView):
    queryset = AccountBank.objects.all()
    serializer_class = AccountBankSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Bank', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Bank {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Bank {instance.name} Delete successfully", data=None)

'''
For Holiday
'''
class HolidayListView(generics.ListAPIView):
    serializer_class = HolidayViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        if month or year:
            queryset = Holiday.objects.filter(Q(end_date__month=month) | Q(start_date__month=month),Q(start_date__year=year),status=True).order_by('start_date','-id')
        else:
            queryset = Holiday.objects.filter(status=True).order_by('start_date','-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('start_date','-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('start_date','-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('start_date','-id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):        
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

class HolidayCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = HolidayViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Holiday.objects.filter(status=True).order_by('start_date','-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('start_date','-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('start_date','-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('start_date','-id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Holiday', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        
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
    
    def create(self, request, *args, **kwargs):
        '''Check user has permission to Create start'''
        permission_check = check_permission(self.request.user.id, 'Holiday', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        serializer_class = HolidaySerializer
        serializer = serializer_class(data=request.data)
        # serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                start_date = serializer.validated_data.get('start_date')
                end_date = serializer.validated_data.get('end_date')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                holiday_count = Holiday.objects.filter(name__iexact=name,start_date=start_date,end_date=end_date,institution=institution,branch=branch,status=True).count()
                if(holiday_count==0):
                    instance = serializer.save(institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Holiday create successfully", data=HolidayViewSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Holiday {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class HolidayDetail(generics.RetrieveUpdateAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Holiday', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=HolidayViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Holiday', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                start_date = serializer.validated_data.get('start_date')
                end_date = serializer.validated_data.get('end_date')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                if (start_date==instance.start_date and end_date==instance.end_date):
                    instance = serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Holiday Update successfully", data=HolidayViewSerializer(instance).data)
                else:
                    holiday_count = Holiday.objects.filter(name__iexact=name,start_date=start_date,end_date=end_date,institution=institution,branch=branch,status=True).count()
                    if(holiday_count==0):
                        # Perform any custom update logic here if needed
                        instance = serializer.save()
                        # Customize the response data
                        return CustomResponse(code=status.HTTP_200_OK, message="Holiday Update successfully", data=HolidayViewSerializer(instance).data)
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Holiday {name} already exits", data=serializer.errors)
                    # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))
    
class HolidayDelete(generics.UpdateAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Holiday', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Holiday {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Holiday {instance.name} Delete successfully", data=None)

'''
For Leave Type
'''
class LeaveTypeList(generics.ListAPIView):
    serializer_class = LeaveTypeListSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = LeaveType.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
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

class LeaveTypeCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = LeaveTypeViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = LeaveType.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Leave Type', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        
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
    
    def create(self, request, *args, **kwargs):
        '''Check user has permission to Create start'''
        permission_check = check_permission(self.request.user.id, 'Leave Type', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                type_count = LeaveType.objects.filter(name__iexact=name,institution=institution,branch=branch,status=True).count()
                if(type_count==0):
                    instance = serializer.save(institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Leave Type create successfully", data=LeaveTypeViewSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Leave Type {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class LeaveTypeDetail(generics.RetrieveUpdateAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Leave Type', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=LeaveTypeViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Leave Type', 'update')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                leave_type_code = serializer.validated_data.get('leave_type_code')
                if (leave_type_code==instance.leave_type_code and name==instance.name):
                    instance = serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Leave Type Update successfully", data=LeaveTypeViewSerializer(instance).data)
                else:
                    # If data is provided, use it; otherwise, use the values from the request user
                    institution = institution_data if institution_data is not None else self.request.user.institution
                    branch = branch_data if branch_data is not None else self.request.user.branch
                    type_count = LeaveType.objects.filter(name__iexact=name,institution=institution,branch=branch,status=True).count()
                    if(type_count==0):
                        # Perform any custom update logic here if needed
                        instance = serializer.save()
                        # Customize the response data
                        return CustomResponse(code=status.HTTP_200_OK, message="Leave Type Update successfully", data=LeaveTypeViewSerializer(instance).data)
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Leave Type {name} already exits", data=serializer.errors)
                    # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))
    
class LeaveTypeDelete(generics.UpdateAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Leave Type', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Leave Type {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Leave Type {instance.name} Delete successfully", data=None)


'''
For Salary Setup
'''
class SalaryElementList(generics.ListAPIView):
    serializer_class = PayrollElementListSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = PayrollElement.objects.filter(is_active=True,status=True).order_by('-id')
        return queryset

    def list(self, request, *args, **kwargs):
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

class SalarySpecificElementList(generics.ListAPIView):
    serializer_class = PayrollElementViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = PayrollElement.objects.filter(is_active=True,status=True).order_by('-id')
        return queryset

    def list(self, request, *args, **kwargs):
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

class SalarySetupCreate(generics.CreateAPIView):
    serializer_class = SalarySetupMstViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

   
    def create(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(self.request.user.id, 'Salary Setup', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        serializer_class = SalarySetupMstCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                salary_mst_count = SalarySetupMst.objects.filter(name=name,status=True).count()
                if (salary_mst_count==0):
                    instance = serializer.save(institution=institution, branch=branch)
                        # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Salary Setup created successfully", data=SalarySetupMstViewSerializer(instance).data)
                else:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Salary Setup already exists for this class", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class SalarySetupList(generics.ListAPIView):
    serializer_class = SalarySetupMstViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        # month = self.request.query_params.get('month')
        # year = self.request.query_params.get('year')
        # if month or year:
        #     queryset = Holiday.objects.filter(Q(end_date__month=month) | Q(start_date__month=month),Q(start_date__year=year),status=True).order_by('start_date','-id')
        # else:
        queryset = SalarySetupMst.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('-id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):        
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

# class StaffSalaryCalculation(generics.ListAPIView):
        
#     def list(self,request,*args, **kwargs):    
           
#         for staff_list in Staff.objects.filter(status=True,pk=96):
#             salary_info = {}
#             staff_sal = StaffPayroll.objects.filter(status=True,is_active=True,staff=staff_list).order_by('start_date').last()
#             staff_gross = staff_sal.gross
#             sal_for_ele = SalarySetupMst.objects.filter(status=True,is_active=True,pk=1).order_by('id').last()
#             for sal_dtl_ele in SalarySetupDtl.objects.filter(status=True,salary_setup_mst=sal_for_ele).order_by('seq_order'):
#                 context = {
#                     'gross_pay': staff_gross,
#                 }
#                 import ast
#                 if sal_dtl_ele.payroll_ele.name =='Gross Salary':
#                     formatted_formula = sal_dtl_ele.formula.format(**context)
#                     gross_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
#                     print('Gross Pay:',gross_pay)
#                 elif sal_dtl_ele.payroll_ele.name =='Basic Pay':
#                     formatted_formula = sal_dtl_ele.formula.format(**context)
#                     basic_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
#                     print('Basic Pay',basic_pay)
#                 elif sal_dtl_ele.payroll_ele.name =='House Rent':
#                     context = {
#                         'gross_pay': gross_pay,
#                         'basic_pay':basic_pay,
#                     }
#                     formatted_formula = sal_dtl_ele.formula.format(**context)
#                     house_rent = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
#                     if sal_dtl_ele.max_amt:
#                         if house_rent > sal_dtl_ele.max_amt:
#                             house_rent = sal_dtl_ele.max_amt
#                     print('House Rent',house_rent)
#                 elif sal_dtl_ele.payroll_ele.name =='Medical':
#                     context = {
#                         'gross_pay': gross_pay,
#                         'basic_pay':basic_pay,
#                         'house_rent': house_rent,
#                         # 'medical': 10,
#                         # 'convence': 5,
#                         # 'others': 5,
#                     }
#                     formatted_formula = sal_dtl_ele.formula.format(**context)
#                     medical_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
#                     if sal_dtl_ele.max_amt:
#                         if medical_pay > sal_dtl_ele.max_amt:
#                             medical_pay = sal_dtl_ele.max_amt
#                     print('Medical Pay:',medical_pay)
#                 elif sal_dtl_ele.payroll_ele.name =='Conveyance':
#                     context = {
#                         'gross_pay': gross_pay,
#                         'basic_pay':basic_pay,
#                         'house_rent': house_rent,
#                         'medical': medical_pay,
#                         # 'convence': 5,
#                         # 'others': 5,
#                     }
#                     formatted_formula = sal_dtl_ele.formula.format(**context)
#                     conveyance_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
#                     if sal_dtl_ele.max_amt:
#                         if conveyance_pay > sal_dtl_ele.max_amt:
#                             conveyance_pay = sal_dtl_ele.max_amt
#                     print('Conveyance Pay:',conveyance_pay)
#                 elif sal_dtl_ele.payroll_ele.name == 'Other':
#                     context = {
#                         'gross_pay': gross_pay,
#                         'basic_pay':basic_pay,
#                         'house_rent': house_rent,
#                         'medical': medical_pay,
#                         'convence': conveyance_pay,
#                         # 'others': 5,
#                     }
#                     formatted_formula = sal_dtl_ele.formula.format(**context)
#                     others_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
#                     print('Others Pay:',others_pay)



#         response_data = {
#             "code": 200,
#             "message": "Success",
#             "data": salary_info
#         }

#         return Response(response_data)

class StaffSalaryCalculation(generics.ListAPIView):
    
    def list(self, request, *args, **kwargs):
        salary_info = {}
        
        for staff_list in Staff.objects.filter(status=True, pk=96):
            staff_sal = StaffPayroll.objects.filter(status=True, is_active=True, staff=staff_list).order_by('start_date').last()
            staff_gross = staff_sal.gross
            sal_for_ele = SalarySetupMst.objects.filter(status=True, is_active=True, pk=1).order_by('id').last()

            context = {
                'gross_pay': staff_gross,
            }

            for sal_dtl_ele in SalarySetupDtl.objects.filter(status=True, salary_setup_mst=sal_for_ele).order_by('seq_order'):
                import ast
                if sal_dtl_ele.payroll_ele.name == 'Gross Salary':
                    formatted_formula = sal_dtl_ele.formula.format(**context)
                    gross_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                    salary_info['Gross Pay'] = gross_pay
                    context['gross_pay'] = gross_pay  # Update context with the calculated gross pay

                elif sal_dtl_ele.payroll_ele.name == 'Basic Pay':
                    formatted_formula = sal_dtl_ele.formula.format(**context)
                    basic_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                    salary_info['Basic Pay'] = basic_pay
                    context['basic_pay'] = basic_pay  # Update context with the calculated basic pay

                elif sal_dtl_ele.payroll_ele.name == 'House Rent':
                    context.update({
                        'basic_pay': salary_info.get('Basic Pay', 0),  # Ensure basic_pay is added to the context
                    })
                    formatted_formula = sal_dtl_ele.formula.format(**context)
                    house_rent = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                    if sal_dtl_ele.max_amt and house_rent > sal_dtl_ele.max_amt:
                        house_rent = sal_dtl_ele.max_amt
                    salary_info['House Rent'] = house_rent
                    context['house_rent'] = house_rent  # Update context with the calculated house rent

                elif sal_dtl_ele.payroll_ele.name == 'Medical':
                    context.update({
                        'house_rent': salary_info.get('House Rent', 0),  # Ensure house_rent is added to the context
                    })
                    formatted_formula = sal_dtl_ele.formula.format(**context)
                    medical_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                    if sal_dtl_ele.max_amt and medical_pay > sal_dtl_ele.max_amt:
                        medical_pay = sal_dtl_ele.max_amt
                    salary_info['Medical Pay'] = medical_pay
                    context['medical'] = medical_pay  # Update context with the calculated medical pay

                elif sal_dtl_ele.payroll_ele.name == 'Conveyance':
                    context.update({
                        'medical': salary_info.get('Medical Pay', 0),  # Ensure medical is added to the context
                    })
                    formatted_formula = sal_dtl_ele.formula.format(**context)
                    conveyance_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                    if sal_dtl_ele.max_amt and conveyance_pay > sal_dtl_ele.max_amt:
                        conveyance_pay = sal_dtl_ele.max_amt
                    salary_info['Conveyance Pay'] = conveyance_pay
                    context['convence'] = conveyance_pay  # Update context with the calculated conveyance pay

                elif sal_dtl_ele.payroll_ele.name == 'Other':
                    context.update({
                        'convence': salary_info.get('Conveyance Pay', 0),  # Ensure conveyance is added to the context
                    })
                    formatted_formula = sal_dtl_ele.formula.format(**context)
                    others_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                    salary_info['Others Pay'] = others_pay

        response_data = {
            "code": 200,
            "message": "Success",
            "data": salary_info
        }

        return Response(response_data)

class SalarySetupListView(generics.ListAPIView):
    serializer_class = SalarySetupMstListSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = SalarySetupMst.objects.filter(status=True).order_by('id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id,status=True).order_by('id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id,status=True).order_by('id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id,status=True).order_by('id')
            else:
                queryset            
        except:
            pass
        return queryset
        
    def list(self,request,*args, **kwargs):        
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
