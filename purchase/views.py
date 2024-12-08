from django.shortcuts import render
from rest_framework import generics, permissions
from sms.utils import CustomResponse
from .models import *
from .serializers import *
from rest_framework import status
from sms.pagination import CustomPagination
from rest_framework.response import Response
from sms.permission import check_permission
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

# Create your views here.

# For supplier

class SupplierList(generics.ListAPIView):
    serializer_class = SupplierListSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Supplier.objects.filter(status=True).order_by('-id')
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

class SupplierCreateList(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = SupplierViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Supplier.objects.filter(status=True).order_by('-id')
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
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'view')
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

    def create(self, request, *args, **kwargs):
        '''Check user has permission to Create start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'create')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        serializer_class = SupplierCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                name_count = Supplier.objects.filter(name=name, institution=institution, branch=branch,is_active=True,status=True).count()
                if (name_count == 0):
                    instance = serializer.save(institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Supplier created successfully", data=SupplierViewSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Warehouse {name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class SupplierDetail(generics.RetrieveUpdateAPIView):
    queryset = Supplier.objects.filter(status=True)
    serializer_class = SupplierCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=SupplierViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'update')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                name = serializer.validated_data.get('name')
                if (name==instance.name):
                    instance = serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Supplier Update successfully", data=SupplierViewSerializer(instance).data)
                else:
                    # If data is provided, use it; otherwise, use the values from the request user
                    institution = institution_data if institution_data is not None else self.request.user.institution
                    branch = branch_data if branch_data is not None else self.request.user.branch
                    fees_count = Supplier.objects.filter(name__iexact=name,institution=institution,branch=branch,status=True).count()
                    if(fees_count==0):
                        # Perform any custom update logic here if needed
                        instance = serializer.save()
                        # Customize the response data
                        return CustomResponse(code=status.HTTP_200_OK, message="Supplier Update successfully", data=SupplierViewSerializer(instance).data)
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Supplier {name} already exits", data=serializer.errors)
                    # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class SupplierDelete(generics.UpdateAPIView):
    queryset = Supplier.objects.filter(status=True)
    serializer_class = SupplierCreateList
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'delete')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Supplier {instance.name} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Supplier {instance.name} Delete successfully", data=None)

class PurchaseOrderList(generics.ListAPIView):
    serializer_class = PurchaseOrderMasterViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = PurchaseOrderMaster.objects.filter(status=True).order_by('-id')
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

class GoodsReceiveNoteList(generics.ListAPIView):
    serializer_class = GoodSReceiptNoteMasterViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = GoodSReceiptNoteMaster.objects.filter(status=True).order_by('-id')
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

class GoodsReceiveNoteCreate(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = GoodSReceiptNoteMasterViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = GoodSReceiptNoteMaster.objects.filter(status=True).order_by('-id')
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
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'view')
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
    
    def create(self, request, *args, **kwargs):
        '''Check user has permission to Create start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'create')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        serializer_class = GoodSReceiptNoteMasterCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                instance = serializer.save(institution=institution, branch=branch)
                    # Customize the response data
                return CustomResponse(code=status.HTTP_200_OK, message="Goods Receive created successfully", data=GoodSReceiptNoteMasterViewSerializer(instance).data)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class GoodsReceiveNoteDetail(generics.RetrieveUpdateAPIView):
    queryset = GoodSReceiptNoteMaster.objects.filter(status=True)
    serializer_class = GoodSReceiptNoteMasterCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=GoodSReceiptNoteMasterViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'update')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                instance = serializer.save()
                # Customize the response data
                return CustomResponse(code=status.HTTP_200_OK, message="Goods Receive Update successfully", data=GoodSReceiptNoteMasterViewSerializer(instance).data)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class GoodsReceiveNoteDelete(generics.UpdateAPIView):
    queryset = GoodSReceiptNoteMaster.objects.filter(status=True)
    serializer_class = GoodSReceiptNoteMasterDeleteSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'delete')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"GRN No. {instance.code} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        for grn_dtl in GoodsReceiptNotesDetails.objects.filter(status=True,goods_receipt_note=instance):
            grn_dtl.status = False
            grn_dtl.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"GRN No. {instance.code} Delete successfully", data=None)

class GoodsReceiveNoteConfirm(generics.UpdateAPIView):
    queryset = GoodSReceiptNoteMaster.objects.filter(status=True)
    serializer_class = GoodSReceiptNoteMasterConfirmSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):

        instance = self.get_object()

        # Get the data from the request body
        confirm_without_pay = request.data.get("confirm_without_pay")
        confirm_with_pay = request.data.get("confirm_with_pay")

        # Validation logic
        if instance.confirm_without_pay or instance.confirm_with_pay:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Goods Receive Note is already confirmed.", data=None)
        
        if confirm_without_pay and confirm_with_pay:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Cannot set both confirm without pay and confirm with pay.", data=None)
        
        # Prevent setting the value to False once it is True
        if instance.confirm_without_pay and confirm_without_pay is False:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Cannot change confirm without pay to False once set to True.", data=None)
        if instance.confirm_with_pay and confirm_with_pay is False:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Cannot change confirm with pay to False once set to True.", data=None)
        
        # Update the instance
        try:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return CustomResponse(code=status.HTTP_200_OK, message=f"Voucher Confirm successfully", data=None)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class GoodSReceiptNoteMasterSearchAPI(generics.ListAPIView):
    queryset = GoodSReceiptNoteMaster.objects.filter(status=True)
    serializer_class = GoodSReceiptNoteMasterViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_value = self.request.query_params.get('search', None)
        queryset = queryset.order_by('-code')
        if search_value.lower() == 'entered':
            queryset = queryset.filter(confirm_with_pay=False, confirm_without_pay=False)
        elif search_value.lower() == 'confirmed':
            queryset = queryset.filter(Q(confirm_with_pay=True) | Q(confirm_without_pay=True))
            
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id)
            elif branch_id:
                queryset = queryset.filter(branch=branch_id)
            elif institution_id:
                queryset = queryset.filter(institution=institution_id)
            else:
                queryset
        except Exception as e:
            print(f"Error while filtering by institution/branch: {e}")
        
        print("Final Queryset:", queryset) 
        return queryset

    
    # Enable search and filtering
    filter_backends = [SearchFilter, DjangoFilterBackend]

    # Fields to allow searching
    search_fields = ['code', 'supplier__name', 'warehouse__name', 'pay_method__name','grn_details__item_name']

'''For Supplier Payment'''

class SupplierPaymentList(generics.ListAPIView):
    serializer_class = SupplierPaymentMstViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = SupplierPaymentMst.objects.filter(status=True).order_by('-id')
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

class SupplierPaymenCreate(generics.ListCreateAPIView):
    # queryset = Version.objects.filter(status=True).order_by('id')
    serializer_class = SupplierPaymentMstViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = SupplierPaymentMst.objects.filter(status=True).order_by('-id')
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
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'view')
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
    
    def create(self, request, *args, **kwargs):
        '''Check user has permission to Create start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'create')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''
        serializer_class = SupplierPaymentMstCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                instance = serializer.save(institution=institution, branch=branch)
                    # Customize the response data
                return CustomResponse(code=status.HTTP_200_OK, message="Supplier Payment created successfully", data=SupplierPaymentMstViewSerializer(instance).data)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class SupplierPaymenDetail(generics.RetrieveUpdateAPIView):
    queryset = SupplierPaymentMst.objects.filter(status=True)
    serializer_class = SupplierPaymentMstCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=SupplierPaymentMstViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'update')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                instance = serializer.save()
                # Customize the response data
                return CustomResponse(code=status.HTTP_200_OK, message="Supplier Payment Update successfully", data=SupplierPaymentMstViewSerializer(instance).data)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class SupplierPaymenDelete(generics.UpdateAPIView):
    queryset = SupplierPaymentMst.objects.filter(status=True)
    serializer_class = SupplierPaymentMstDeleteSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        # permission_check = check_permission(self.request.user.id, 'Fees Type', 'delete')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''

        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Supplier Payment. {instance.code} already Deleted", data=None)
        if instance.confirm:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Supplier Payment already confirmed!!", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        for sp_dtl in SupplierPaymentDtl.objects.filter(status=True,supplier_payment=instance):
            sp_dtl.status = False
            sp_dtl.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Supplier Payment. {instance.code} Delete successfully", data=None)

class SupplierPaymentConfirm(generics.UpdateAPIView):
    queryset = SupplierPaymentMst.objects.filter(status=True)
    serializer_class = SupplierPaymentMstConfirmSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):

        instance = self.get_object()

        if instance.confirm:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Supplier Payment already Confirmed", data=None)
        else:
            instance.confirm = True
            instance.save()
            return CustomResponse(code=status.HTTP_200_OK, message=f"Supplier Payment Confirm successfully", data=None)



