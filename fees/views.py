from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
from .serializers import *
from rest_framework import status
from sms.pagination import CustomPagination
from rest_framework.response import Response
from authentication.models import Authentication
from setup_app.models import *
from sms.permission import check_permission,generate_random_payment_id
from django.utils import timezone
# Create your views here.

'''
For Fees Type
'''
class FeesTypeList(generics.ListAPIView):
    serializer_class = FeesTypeListSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = FeesType.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('-id')
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

class FeesTypeCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = FeesTypeViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = FeesType.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Fees Type', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Fees Type', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        serializer_class = FeesTypeCreateSerializer
        serializer = serializer_class(data=request.data)
        print(request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                name_count = FeesType.objects.filter(name=name, institution=institution, branch=branch,is_active=True,status=True).count()
                if (name_count == 0):
                    instance = serializer.save(institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Fees Type created successfully", data=FeesTypeViewSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Fees Type {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class FeesTypeDetail(generics.RetrieveUpdateAPIView):
    queryset = FeesType.objects.all()
    serializer_class = FeesTypeCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Fees Type', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=FeesTypeViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Fees Type', 'update')
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
                code = serializer.validated_data.get('code')
                if (code==instance.code and name==instance.name):
                    instance = serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Fees Type Update successfully", data=FeesTypeViewSerializer(instance).data)
                else:
                    # If data is provided, use it; otherwise, use the values from the request user
                    institution = institution_data if institution_data is not None else self.request.user.institution
                    branch = branch_data if branch_data is not None else self.request.user.branch
                    fees_count = FeesType.objects.filter(name__iexact=name,institution=institution,branch=branch,status=True).count()
                    if(fees_count==0):
                        # Perform any custom update logic here if needed
                        instance = serializer.save()
                        # Customize the response data
                        return CustomResponse(code=status.HTTP_200_OK, message="Fees Type Update successfully", data=FeesTypeViewSerializer(instance).data)
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Fees Type {name} already exits", data=serializer.errors)
                    # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class FeesTypeDelete(generics.UpdateAPIView):
    queryset = FeesType.objects.all()
    serializer_class = FeesTypeCreateSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Fees Type', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Fees Type {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Fees Type {instance.name} Delete successfully", data=None)

'''
For Fees Discount
'''
class FeesDiscountList(generics.ListAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = FeesDiscountViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = FeesDiscount.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Fees Discount', 'view')
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


class FeesDiscountCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = FeesDiscountViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = FeesDiscount.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('-id')
            else:
                queryset
        except:
            pass
        return queryset

    def list(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Fees Discount', 'view')
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
        permission_check = check_permission(
            self.request.user.id, 'Fees Discount', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        serializer_class = FeesDiscountCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                name_count = FeesDiscount.objects.filter(name=name, institution=institution, branch=branch,status=True).count()
                if (name_count == 0):
                    instance = serializer.save(institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Fees Discount created successfully", data=FeesDiscountViewSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Fees Discount {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class FeesDiscountDetail(generics.RetrieveUpdateAPIView):
    queryset = FeesDiscount.objects.all()
    serializer_class = FeesDiscountCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        permission_check = check_permission(self.request.user.id, 'Fees Discount', 'view')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=FeesDiscountViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        permission_check = check_permission(self.request.user.id, 'Fees Discount', 'update')
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
                code = serializer.validated_data.get('code')
                if (code==instance.code and name==instance.name):
                    instance = serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Fees Discount Update successfully", data=FeesDiscountViewSerializer(instance).data)
                else:
                    # If data is provided, use it; otherwise, use the values from the request user
                    institution = institution_data if institution_data is not None else self.request.user.institution
                    branch = branch_data if branch_data is not None else self.request.user.branch
                    fees_count = FeesDiscount.objects.filter(name__iexact=name,institution=institution,branch=branch,status=True).count()
                    if(fees_count==0):
                        # Perform any custom update logic here if needed
                        instance = serializer.save()
                        # Customize the response data
                        return CustomResponse(code=status.HTTP_200_OK, message="Fees Discount Update successfully", data=FeesDiscountViewSerializer(instance).data)
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Fees Discount {name} already exits", data=serializer.errors)
                    # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class FeesDiscountDelete(generics.UpdateAPIView):
    queryset = FeesDiscount.objects.all()
    serializer_class = FeesDiscountCreateSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        permission_check = check_permission(self.request.user.id, 'Fees Discount', 'delete')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Fees Discount {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Fees Discount {instance.name} Delete successfully", data=None)

'''
For Fees
'''
class FeesCreateList(generics.ListCreateAPIView):
    serializer_class = FeesMasterViewSerializer
    # serializer_class = FeesMasterCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = FeesMaster.objects.filter(status=True).order_by('-id')
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
        # permission_check = check_permission(
        #     self.request.user.id, 'Fees Entry', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
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
        '''Check user has permission to View start'''
        permission_check = check_permission(
            self.request.user.id, 'Fees Entry', 'create')
        if not permission_check:
            return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        data = request.data
        fees_data = data.copy()
        fees_details = fees_data.pop('fees_detail',[])
        serializer_class = FeesMasterCreateSerializer
        fees_serializer = serializer_class(data=fees_data)

        if fees_serializer.is_valid():
            fees_serializer.is_valid(raise_exception=True)
            institution_data = fees_serializer.validated_data.get('institution')
            branch_data = fees_serializer.validated_data.get('branch')
            # If data is provided, use it; otherwise, use the values from the request user
            institution = institution_data if institution_data is not None else self.request.user.institution
            branch = branch_data if branch_data is not None else self.request.user.branch
            fees_master = fees_serializer.save(institution=institution, branch=branch)

            details = []
            for fees_detail in fees_details:
                fees_detail['fees_master'] = fees_master.id 
                detail_serializer = FeesDetailsCreateSerializer(data=fees_detail)
                detail_serializer.is_valid(raise_exception=True)
                detail = detail_serializer.save(institution=institution, branch=branch)
                details.append(detail)
            response_data = fees_serializer.data
            response_data['fees_detail'] = FeesDetailsViewSerializer(details,many=True).data
        
        return Response(response_data, status=status.HTTP_201_CREATED)

class FeesDetailUpdate(generics.RetrieveUpdateAPIView):
    queryset = FeesMaster.objects.filter(status=True)
    serializer_class = FeesMasterCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        # permission_check = check_permission(
        #     self.request.user.id, 'Fees Entry', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object() 
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=FeesMasterViewSerializer(instance).data)
    
    def update(self, request, *args, **kwargs):
        fees = self.get_object()
        institution = self.request.user.institution
        branch = self.request.user.branch
        fees_serializer = self.get_serializer(fees, data=request.data, partial=True)
        fees_serializer.is_valid(raise_exception=True)
        instance = fees_serializer.save()
        return CustomResponse(code=status.HTTP_200_OK, message="Staff information updated successfully", data=FeesMasterViewSerializer(instance).data)

class FeesEntryList(generics.ListAPIView):
    serializer_class = FeesMasterListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = FeesMaster.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
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

'''
For Fees detail breakdown
'''
class FeesDetailsBreakDownList(generics.ListCreateAPIView):
    serializer_class = FeeDetailsBreakDownViewSerializer
    # serializer_class = FeesMasterCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    

    def get_queryset(self):
        fees_dtl = self.request.query_params.get('fees_dtl')
        if fees_dtl:
            queryset = FeeDetailsBreakDown.objects.filter(status=True,fees_detail=fees_dtl ).order_by('id')
        else:
            queryset = FeeDetailsBreakDown.objects.filter(status=True).order_by('id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
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
        '''Check user has permission to View start'''
        # permission_check = check_permission(
        #     self.request.user.id, 'Fees Entry', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
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
    
    # def create(self, request, *args, **kwargs):
    #     '''Check user has permission to Create start'''
    #     # permission_check = check_permission(self.request.user.id, 'Fees Discount', 'create')
    #     # if not permission_check:
    #     #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
    #     '''Check user has permission to Create End'''
    #     serializer_class = FeeDetailsBreakDownCreateSerializer
    #     serializer = serializer_class(data=request.data)
    #     try:
    #         if serializer.is_valid():
    #             institution_data = serializer.validated_data.get('institution')
    #             branch_data = serializer.validated_data.get('branch')
    #             # If data is provided, use it; otherwise, use the values from the request user
    #             institution = institution_data if institution_data is not None else self.request.user.institution
    #             branch = branch_data if branch_data is not None else self.request.user.branch
    #             instance = serializer.save(institution=institution, branch=branch)
    #                 # Customize the response data
    #             return CustomResponse(code=status.HTTP_200_OK, message="Fees Details Break Down created successfully", data=FeeDetailsBreakDownViewSerializer(instance).data)
    #         # If the serializer is not valid, return an error response
    #         return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
    #     except Exception as e:
    #         # Handle other exceptions
    #         return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

# class FeesDetailsBreakDownCreate(generics.ListCreateAPIView):
#     serializer_class = FeeDetailsBreakDownCreateSerializer
#     # serializer_class = FeesMasterCreateSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     pagination_class = CustomPagination

#     def create(self, request, *args, **kwargs):
#         try:
#             institution_id = self.request.user.institution.id
#             branch_id = self.request.user.branch.id
#             fees_break_down_data = request.data.get("fees_break_down", [])
#             for item in fees_break_down_data:
#                 item["institution"] = institution_id
#                 item["branch"] = branch_id
#             serializer = self.get_serializer(data=fees_break_down_data, many=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             return CustomResponse(code=status.HTTP_200_OK, message="Fees Details Break Down created successfully", data=serializer.data)
#         except Exception as e:
#             # Handle other exceptions
#             return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

# class FeesDetailsBreakDownCreate(generics.ListCreateAPIView):
#     serializer_class = FeeDetailsBreakDownCreateSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     pagination_class = CustomPagination

#     def create(self, request, *args, **kwargs):
#         try:
#             institution_id = self.request.user.institution.id
#             branch_id = self.request.user.branch.id
#             fees_break_down_data = request.data.get("fees_break_down", [])
#             created_data = []
#             updated_data = []

#             for item in fees_break_down_data:
#                 item["institution"] = institution_id
#                 item["branch"] = branch_id
#                 if "id" in item:
#                     # If ID is present, update the existing entry
#                     try:
#                         instance = FeeDetailsBreakDown.objects.get(id=item["id"])
#                         serializer = self.get_serializer(instance, data=item, partial=True)
#                         serializer.is_valid(raise_exception=True)
#                         serializer.save()
#                         updated_data.append(serializer.data)
#                     except FeeDetailsBreakDown.DoesNotExist:
#                         return CustomResponse(
#                             code=status.HTTP_400_BAD_REQUEST,
#                             message=f"FeeDetailsBreakDown with ID {item['id']} does not exist.",
#                             data=None
#                         )
#                 else:
#                     # If ID is not present, create a new entry
#                     created_data.append(item)

#             if created_data:
#                 create_serializer = self.get_serializer(data=created_data, many=True)
#                 create_serializer.is_valid(raise_exception=True)
#                 self.perform_create(create_serializer)
#                 created_data = create_serializer.data

#             return CustomResponse(
#                 code=status.HTTP_200_OK,
#                 message="Fees Details Break Down processed successfully",
#                 data={"created": created_data, "updated": updated_data}
#             )
#         except Exception as e:
#             return CustomResponse(
#                 code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 message="An error occurred during the Create/Update process",
#                 data=str(e)
#             )

class FeesDetailsBreakDownCreate(generics.ListCreateAPIView):
    serializer_class = FeeDetailsBreakDownCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        try:
            institution_id = self.request.user.institution.id
            branch_id = self.request.user.branch.id
            fees_break_down_data = request.data.get("fees_break_down", [])
            provided_ids = [item.get("id") for item in fees_break_down_data if "id" in item]

            # Get all existing records for the provided fees_detail, institution, and branch
            fees_detail_id = fees_break_down_data[0]['fees_detail'] if fees_break_down_data else None
            existing_records = FeeDetailsBreakDown.objects.filter(
                fees_detail=fees_detail_id,
                institution=institution_id,
                branch=branch_id
            )

            # Update the status to False for records that exist in DB but are not in the request
            records_to_update = existing_records.exclude(id__in=provided_ids)
            records_to_update.update(status=False)

            created_data = []
            updated_data = []

            for item in fees_break_down_data:
                item["institution"] = institution_id
                item["branch"] = branch_id
                if "id" in item:
                    # If ID is present, update the existing entry
                    try:
                        instance = FeeDetailsBreakDown.objects.get(id=item["id"])
                        serializer = self.get_serializer(instance, data=item, partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        updated_data.append(serializer.data)
                    except FeeDetailsBreakDown.DoesNotExist:
                        return CustomResponse(
                            code=status.HTTP_400_BAD_REQUEST,
                            message=f"FeeDetailsBreakDown with ID {item['id']} does not exist.",
                            data=None
                        )
                else:
                    # If ID is not present, create a new entry
                    created_data.append(item)

            if created_data:
                create_serializer = self.get_serializer(data=created_data, many=True)
                create_serializer.is_valid(raise_exception=True)
                self.perform_create(create_serializer)
                created_data = create_serializer.data

            return CustomResponse(
                code=status.HTTP_200_OK,
                message="Fees Details Break Down processed successfully",
                data={"created": created_data, "updated": updated_data}
            )
        except Exception as e:
            return CustomResponse(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred during the Create/Update process",
                data=str(e)
            )

class FeesDetailUpdate(generics.RetrieveUpdateAPIView):
    queryset = FeesMaster.objects.filter(status=True)
    serializer_class = FeesMasterCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        # permission_check = check_permission(
        #     self.request.user.id, 'Fees Entry', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object() 
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=FeesMasterViewSerializer(instance).data)
    
    def update(self, request, *args, **kwargs):
        fees = self.get_object()
        institution = self.request.user.institution
        branch = self.request.user.branch
        fees_serializer = self.get_serializer(fees, data=request.data, partial=True)
        fees_serializer.is_valid(raise_exception=True)
        instance = fees_serializer.save()
        return CustomResponse(code=status.HTTP_200_OK, message="Staff information updated successfully", data=FeesMasterViewSerializer(instance).data)

'''
For Fees Transaction
'''
class StudentWiseFeesTransaction(generics.ListAPIView):
    serializer_class = FeesTransactionViewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    pagination_class = CustomPagination

    def get_queryset(self):
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch
        student_id = self.request.query_params.get('student_id')
        if student_id is None:
            student_id = Student.objects.get(status=True,user=self.request.user.id)
        queryset = FeesTransaction.objects.filter(status=True,institution=institution_id,branch=branch_id,student=student_id).order_by('id')
        
        try:
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
        '''Check user has permission to View start'''
        # permission_check = check_permission(self.request.user.id, 'Staff Shift', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
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

class FeesTrnsManualEntry(generics.ListAPIView):
    def list(self,request,*args, **kwargs):
        std_fees_trns = {}
        student_enrolls = StudentEnroll.objects.filter(status=True,is_active=True).order_by('id')
        for enroll in student_enrolls:
            # print(enroll.student.id,enroll.class_name,enroll.section,enroll.session,enroll.version,enroll.group)
            fees_lists = FeesDetails.objects.filter(status=True,is_active=True,fees_master__version=enroll.version,fees_master__class_name=enroll.class_name,fees_master__section=enroll.section,fees_master__session=enroll.session,institution=enroll.institution,branch=enroll.branch)
            for fees_list in fees_lists:
                std_fees_trns['student'] = enroll.student
                std_fees_trns['fees_detail'] = fees_list
                std_fees_trns['institution'] = enroll.institution
                std_fees_trns['branch'] = enroll.branch
                # print(fees_list)
                trns_count = FeesTransaction.objects.filter(status=True,student=enroll.student,fees_detail=fees_list,institution=enroll.institution,branch=enroll.branch).count()
                if (trns_count==0):
                    t = FeesTransaction.objects.create(**std_fees_trns)
                else:
                    print('Nothing to insert')

        return Response(f"std_fees_trns")

class StudentWiseFeesTrnsDetails(generics.RetrieveAPIView):
    queryset = FeesTransaction.objects.filter(pay_status=False)
    serializer_class = FeesTransactionListSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to View start'''
        # permission_check = check_permission(
        #     self.request.user.id, 'Fees Entry', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to View end'''
        instance = self.get_object() 
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=FeesTransactionListSerializer(instance).data)
        
class StudentWiseFeesDiscountAdd(generics.UpdateAPIView):
    queryset = FeesTransaction.objects.filter(pay_status=False)
    serializer_class = FeesTransactionAddDiscountSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access

    def partial_update(self, request, *args, **kwargs):
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch
        queryset = self.queryset.filter(institution=institution_id, branch=branch_id,status=True)
        instance = self.get_object()
        # Get discount_type value from user request data
        discount_type = request.data.get('discount_type')
        discount = FeesDiscount.objects.get(pk=discount_type,institution=institution_id,branch=branch_id)
        if discount:
            try:
                instance.discount_type = discount
                instance.save()
                # Customize the response format for successful update
                return CustomResponse(code=status.HTTP_200_OK, message=f"Fees Discount added successfully", data=FeesTransactionListSerializer(instance).data)
            except FeesDiscount.DoesNotExist:
                return CustomResponse(
                    code=status.HTTP_400_BAD_REQUEST, 
                    message=f"Fees Discount with ID {discount_type} does not exist", 
                    data=FeesTransactionListSerializer(instance).data
                )
        else:
            return CustomResponse(
                code=status.HTTP_400_BAD_REQUEST, 
                message="Discount type value is missing", 
                data=FeesTransactionListSerializer(instance).data
            )

class StudentWiseFeesCollection(generics.UpdateAPIView):
    queryset = FeesTransaction.objects.filter(status=True,pay_status=False)
    serializer_class = FessTransactionCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        fees = self.get_object()
        institution = self.request.user.institution
        branch = self.request.user.branch
        request_date = request.data
        student_no = request_date['student_no']
        pay_method = request_date['pay_method']
        if not pay_method:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Please provide pay method", data=None)
        pay_method_name = PaymentMethod.objects.get(pk=pay_method)
        if pay_method_name.name.lower() == 'cash':
            std_id = Student.objects.filter(student_no=student_no,institution=institution,branch=branch,status=True).last()
            if std_id:
                fees_amt = self.queryset.filter(institution=institution,branch=branch,student=std_id,pk=fees.id).last()
                if fees_amt:
                    paid_amt = fees_amt.net_fess_amt()
                    update_date ={
                        'paid_amt' : paid_amt,
                        'pay_status': True,
                        'pay_method': pay_method,
                        "payment_id":generate_random_payment_id(),
                        'pay_date': timezone.now()

                    }
                    fees_serializer = self.get_serializer(fees, data=update_date, partial=True)
                    fees_serializer.is_valid(raise_exception=True)
                    instance = fees_serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Student Payment successfully", data=FessTransactionCollectionSerializer(instance).data)
                else:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Fees Data not Match", data=None)
            else:
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Employees Not Match", data=None)
        else:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Only Cash Allowed", data=None)





