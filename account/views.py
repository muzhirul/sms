from rest_framework.response import Response
from sms.pagination import CustomPagination
from rest_framework import generics
from django.db.models import F, Window, Sum, Count,Case,When,Value,Subquery, OuterRef, DecimalField
from django.db.models import RowRange, Value as V
from .models import *
from .serializers import *
from rest_framework import generics, permissions
from datetime import datetime
from sms.utils import CustomResponse
from rest_framework import status
from sms.permission import check_permission
from django.db.models import Q
    

class ChartOfAccountCreateList(generics.ListCreateAPIView):
    serializer_class = ChartOfAccountViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ChartofAccounts.objects.filter(status=True).order_by('-id')
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
        # permission_check = check_permission(self.request.user.id, 'Version', 'view')
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
        # permission_check = check_permission(self.request.user.id, 'Version', 'create')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''

        serializer_class = ChartOfAccountCreateSerializer
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
                return CustomResponse(code=status.HTTP_200_OK, message="COA created successfully", data=ChartOfAccountViewSerializer(instance).data)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class ChartOfAccountRetriveUpdate(generics.RetrieveUpdateAPIView):
    queryset = ChartofAccounts.objects.filter(status=True)
    serializer_class = ChartOfAccountCreateSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        # permission_check = check_permission(self.request.user.id, 'Class Routine', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        try:
            instance = self.get_object()
            # Customize the response format for retrieving a single instance
            return CustomResponse(code=status.HTTP_200_OK, message="Success", data=ChartOfAccountViewSerializer(instance).data)
        except:
            return CustomResponse(code=status.HTTP_404_NOT_FOUND, message="Not Found", data=None)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        # permission_check = check_permission(self.request.user.id, 'Class Routine', 'update')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = ChartOfAccountCreateSerializer
        serializer = serializer_class(instance, data=request.data, partial=partial)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                instance = serializer.save()
                return CustomResponse(code=status.HTTP_200_OK, message="COA updated successfully", data=ChartOfAccountViewSerializer(instance).data)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class ChartOfAccountDelete(generics.UpdateAPIView):
    queryset = ChartofAccounts.objects.filter(status=True)
    serializer_class = ChartOfAccountCreateSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        # permission_check = check_permission(self.request.user.id, 'Class Routine', 'delete')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        instance = self.get_object()
        
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"COA already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"COA Delete successfully", data=None)

class ChartofAccountList(generics.ListAPIView):
    serializer_class = CostofAccountSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ChartofAccounts.objects.filter(parent_id__isnull=True,status=True).order_by('id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('id')
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

class ChartOfAccountList(generics.ListAPIView):
    serializer_class = ChartOfAccountSortSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ChartofAccounts.objects.filter(status=True).order_by('id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(
                    institution=institution_id, branch=branch_id, status=True).order_by('id')
            elif branch_id:
                queryset = queryset.filter(
                    branch=branch_id, status=True).order_by('id')
            elif institution_id:
                queryset = queryset.filter(
                    institution=institution_id, status=True).order_by('id')
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

class AccLedgerListView(generics.ListAPIView):
    serializer_class = AccLedgerSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = CustomPagination

    def get_queryset(self):
        acc_coa = self.request.query_params.get('acc_coa')
        if acc_coa:
            queryset = AccountLedger.objects.filter(status=True,acc_coa=acc_coa).annotate(
                    balance=Window(
                        expression=Sum(F('debit_amt') - F('credit_amt')),
                        partition_by=[F('acc_coa')],
                        order_by=F('gl_date').asc(),
                        frame=RowRange(start=None, end=0)
                    )
                )
        else:
            queryset = AccountLedger.objects.filter(status=True).annotate(
                    balance=Window(
                        expression=Sum(F('debit_amt') - F('credit_amt')),
                        partition_by=[F('acc_coa')],
                        order_by=F('gl_date').asc(),
                        frame=RowRange(start=None, end=0)
                    )
                )
        from_date = self.request.query_params.get('from_date')
        if from_date:
            from_date = datetime.strptime(from_date,'%Y-%m-%d').date()
        to_date = self.request.query_params.get('to_date')
        if to_date:
            to_date = datetime.strptime(to_date,'%Y-%m-%d').date()
        if from_date and to_date:
            queryset = queryset.filter(gl_date__range=[from_date, to_date])
        if from_date > to_date:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"From date {from_date} is less than To date {to_date}", data=None)
        
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True)
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True)
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True)
            else:
                queryset
        except:
            pass
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        total_debit_amt = sum([float(item['debit_amt']) for item in serialized_data if item['debit_amt']])
        total_credit_amt = sum([float(item['credit_amt']) for item in serialized_data if item['credit_amt']])

        if not serialized_data:
            last_balance = 0
        else:
            last_item = serialized_data[-1]
            last_balance = last_item['balance']

        
        response_data = {
            "code": 200,
            "message": "Success",
            "data": serializer.data,
            "total": {
                    "gl_date": None,
                    "acc_coa": None,
                    "acc_coa_ref": None,
                    "narration": None,
                    "total": None,
                    "total_debit_amt": total_debit_amt,
                    "total_credit_amt": total_credit_amt,
                    "total_balance": last_balance,

                }
        }

        return Response(response_data)
    
class COAHeadList(generics.ListAPIView):
    serializer_class = ChartOfAccountSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        # queryset = ChartofAccounts.objects.filter(parent_id__isnull=True,status=True).order_by('id')
        queryset = ChartofAccounts.objects.annotate(
            transaction_count=Count('acc_coa')
        ).filter(transaction_count__gt=0)
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('code')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('code')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('code')
            else:
                queryset
        except:
            pass
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "code": 200,
            "message": "Success",
            "data": serializer.data,
        }

        return Response(response_data)
    
class TrialBalanceAPIView(generics.ListAPIView):
    serializer_class = TrialBalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch
        from_date = self.request.query_params.get('from_date')
        if from_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = self.request.query_params.get('to_date')
        if to_date:
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

        # Date validation
        if from_date > to_date:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"From date {from_date} is less than To date {to_date}", data=None)
        
        # Subquery for opening balance (before from_date)
        opening_balance_subquery = AccountLedger.objects.filter(
                        acc_coa=OuterRef('acc_coa'),
                        gl_date__lt=from_date,institution=institution_id, branch=branch_id
                    ).values('acc_coa').annotate(
                        opening_balance=Sum('debit_amt') - Sum('credit_amt')
                    ).values('opening_balance')
        
        # Subquery for closing balance (up to to_date)
        closing_balance_subquery = AccountLedger.objects.filter(
                    acc_coa=OuterRef('acc_coa'),
                    gl_date__lte=to_date,institution=institution_id, branch=branch_id
                ).values('acc_coa').annotate(
                    closing_balance=Sum('debit_amt') - Sum('credit_amt')
                ).values('closing_balance')

        # Calculate amounts
        amounts = (AccountLedger.objects
                   .filter(gl_date__range=[from_date, to_date],institution=institution_id, branch=branch_id)
                   .values('acc_coa')
                   .annotate(
                       title=F('acc_coa__title'),  # Assuming 'title' is a field in the ChartofAccounts model
                       amount=Sum('debit_amt') - Sum('credit_amt'),
                    opening_balance=Subquery(opening_balance_subquery, output_field=DecimalField()),
                    closing_balance=Subquery(closing_balance_subquery, output_field=DecimalField())
                   ))

        # Annotate the queryset with debit, credit, opening/closing balances
        queryset = amounts.annotate(
            debit_amt=Case(
                When(amount__gte=Value(0), then=F('amount')),
                default=Value(0),
                output_field=DecimalField(),
            ),
            credit_amt=Case(
                When(amount__lt=Value(0), then=-F('amount')),
                default=Value(0),
                output_field=DecimalField(),
            ),
            opening_debit_amt=Case(
                When(opening_balance__gte=Value(0), then=F('opening_balance')),
                default=Value(0),
                output_field=DecimalField(),
            ),
            opening_credit_amt=Case(
                When(opening_balance__lt=Value(0), then=-F('opening_balance')),
                default=Value(0),
                output_field=DecimalField(),
            ),
            closing_debit_amt=Case(
                When(closing_balance__gte=Value(0), then=F('closing_balance')),
                default=Value(0),
                output_field=DecimalField(),
            ),
            closing_credit_amt=Case(
                When(closing_balance__lt=Value(0), then=-F('closing_balance')),
                default=Value(0),
                output_field=DecimalField(),
            )
        ).values(
            'acc_coa', 'title', 'debit_amt', 'credit_amt', 
            'opening_debit_amt', 'opening_credit_amt',
            'closing_debit_amt', 'closing_credit_amt'
        )
        

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Calculate totals
        total_debit_amt = sum([item['debit_amt'] for item in queryset])
        total_credit_amt = sum([item['credit_amt'] for item in queryset])
        total_opening_debit_amt = sum([item['opening_debit_amt'] for item in queryset])
        total_opening_credit_amt = sum([item['opening_credit_amt'] for item in queryset])
        total_closing_debit_amt = sum([item['closing_debit_amt'] for item in queryset])
        total_closing_credit_amt = sum([item['closing_credit_amt'] for item in queryset])

        # Prepare the total row
        total_row = {
            "acc_coa": None,
            "title": "Total",
            "debit_amt": total_debit_amt,
            "credit_amt": total_credit_amt,
            "opening_debit_amt": total_opening_debit_amt,
            "opening_credit_amt": total_opening_credit_amt,
            "closing_debit_amt": total_closing_debit_amt,
            "closing_credit_amt": total_closing_credit_amt
        }

        response_data = {
            "code": 200,
            "message": "Success",
            "data": serializer.data,
            "total": total_row
        }

        return Response(response_data)
    
class AccountGenLedgerListView(generics.ListAPIView):
    serializer_class = AccLedgerViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = AccountLedger.objects.filter(status=True).order_by('-gl_date')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('-gl_date')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('-gl_date')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('-gl_date')
            else:
                queryset
        except:
            pass
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "code": 200,
            "message": "Success",
            "data": serializer.data,
        }

        return Response(response_data)

class AccountVoucherCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AccountVoucherMasterViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = AccountVoucherMaster.objects.filter(status=True).order_by('-gl_date','-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('-gl_date','-id')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('-gl_date','-id')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('-gl_date','-id')
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

    def create(self, request, *args, **kwargs):
        serializer_class = AccountVoucherMasterSerializer
        serializer = serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            institution_data = serializer.validated_data.get('institution')
            branch_data = serializer.validated_data.get('branch')
            institution = institution_data if institution_data is not None else self.request.user.institution
            branch = branch_data if branch_data is not None else self.request.user.branch
            instance = serializer.save(institution=institution, branch=branch)

            return CustomResponse(
                code=status.HTTP_200_OK,
                message="Voucher created successfully",
                data=AccountVoucherMasterViewSerializer(instance).data
            )
        except Exception as e:
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class AccountVoucherDetaillupdate(generics.RetrieveUpdateAPIView):
    queryset = AccountVoucherMaster.objects.filter(status=True)
    serializer_class = AccountVoucherMasterSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        # permission_check = check_permission(self.request.user.id, 'Class Routine', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        try:
            instance = self.get_object()
            # Customize the response format for retrieving a single instance
            return CustomResponse(code=status.HTTP_200_OK, message="Success", data=AccountVoucherMasterViewSerializer(instance).data)
        except:
            return CustomResponse(code=status.HTTP_404_NOT_FOUND, message="Not Found", data=None)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        # permission_check = check_permission(self.request.user.id, 'Class Routine', 'update')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = AccountVoucherMasterSerializer
        serializer = serializer_class(instance, data=request.data, partial=partial)
        try:
            if serializer.is_valid():
                if not instance.confirm:
                    institution_data = serializer.validated_data.get('institution')
                    branch_data = serializer.validated_data.get('branch')
                    institution = institution_data if institution_data is not None else self.request.user.institution
                    branch = branch_data if branch_data is not None else self.request.user.branch
                    instance = serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Voucher updated successfully", data=AccountVoucherMasterViewSerializer(instance).data)
                else:
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="You can not update Voucher...", data=serializer.errors)
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))

class AccountVoucherDelete(generics.UpdateAPIView):
    queryset = AccountVoucherMaster.objects.all()
    serializer_class = AccountVoucherMasterSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        # permission_check = check_permission(self.request.user.id, 'Class Routine', 'delete')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        instance = self.get_object()

        if instance.confirm:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Voucher already Confirmed", data=None)
        
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Voucher already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        for voucher_dtl in AccountVoucherDetails.objects.filter(status=True,acc_voucher_mst=instance):
            voucher_dtl.status = False
            voucher_dtl.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Voucher Delete successfully", data=None)

class AccountVoucherConfirm(generics.UpdateAPIView):
    queryset = AccountVoucherMaster.objects.filter(status=True)
    serializer_class = AccountVoucherMasterSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        # permission_check = check_permission(self.request.user.id, 'Class Routine', 'delete')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        instance = self.get_object()

        if instance.confirm:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Voucher already Confirmed", data=None)
        else:
            instance.confirm = True
            instance.save()
            return CustomResponse(code=status.HTTP_200_OK, message=f"Voucher Confirm successfully", data=None)

class AccountVoucherMasterAPIView(generics.ListAPIView):
    serializer_class = ChartOfAccountSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        # queryset = ChartofAccounts.objects.filter(parent_id__isnull=True,status=True).order_by('id')
        queryset = ChartofAccounts.objects.filter(status=True,coa_type='ASSET',parent__title__iexact='Current Asset')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('code')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('code')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('code')
            else:
                queryset
        except:
            pass
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "code": 200,
            "message": "Success",
            "data": serializer.data,
        }

        return Response(response_data)

class AccountVoucherDetailAPIView(generics.ListAPIView):
    serializer_class = ChartOfAccountSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        # queryset = ChartofAccounts.objects.filter(parent_id__isnull=True,status=True).order_by('id')
        queryset = ChartofAccounts.objects.filter(status=True,coa_type='EXPENSE',parent__title__iexact='Expense')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('code')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('code')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('code')
            else:
                queryset
        except:
            pass
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "code": 200,
            "message": "Success",
            "data": serializer.data,
        }

        return Response(response_data)

class AccountVoucherAllAPIView(generics.ListAPIView):
    serializer_class = ChartOfAccountSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        # queryset = ChartofAccounts.objects.filter(parent_id__isnull=True,status=True).order_by('id')
        queryset = ChartofAccounts.objects.filter(
                        Q(coa_type='EXPENSE', parent__title__iexact='Expense') |
                        Q(coa_type='ASSET', parent__title__iexact='Current Asset'),
                        status=True
                    )
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            if institution_id and branch_id:
                queryset = queryset.filter(institution=institution_id, branch=branch_id, status=True).order_by('code')
            elif branch_id:
                queryset = queryset.filter(branch=branch_id, status=True).order_by('code')
            elif institution_id:
                queryset = queryset.filter(institution=institution_id, status=True).order_by('code')
            else:
                queryset
        except:
            pass
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "code": 200,
            "message": "Success",
            "data": serializer.data,
        }

        return Response(response_data)

class AccountBankList(generics.ListCreateAPIView):
    serializer_class = AccountBanksSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = AccountBanks.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
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

class AccountBankCreateList(generics.ListCreateAPIView):
    serializer_class = AccountBanksViewSerializer
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = AccountBanks.objects.filter(status=True).order_by('-id')
        try:
            institution_id = self.request.user.institution
            branch_id = self.request.user.branch
            # users = Authentication.objects.get(id=user_id)
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
        # permission_check = check_permission(self.request.user.id, 'Version', 'view')
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
        # permission_check = check_permission(self.request.user.id, 'Version', 'create')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Create End'''

        serializer_class = AccountBanksCreateSerializer
        serializer = serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                institution_data = serializer.validated_data.get('institution')
                branch_data = serializer.validated_data.get('branch')
                bank_name = serializer.validated_data.get('bank')
                branch_name = serializer.validated_data.get('branch_name')
                account_no = serializer.validated_data.get('account_no')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                bank_count = AccountBanks.objects.filter(bank=bank_name,branch_name=branch_name,account_no=account_no,institution=institution, branch=branch, status=True).count()
                if (bank_count == 0):
                    instance = serializer.save(institution=institution, branch=branch)
                    # Customize the response data
                    return CustomResponse(code=status.HTTP_200_OK, message="Bank Info created successfully", data=AccountBanksViewSerializer(instance).data)
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Bank Information {bank_name} already exits", data=serializer.errors)
            # If the serializer is not valid, return an error response
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the Create", data=str(e))

class AccountBankDetail(generics.RetrieveUpdateAPIView):
    queryset = AccountBanks.objects.all()
    serializer_class = AccountBanksCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def retrieve(self, request, *args, **kwargs):
        '''Check user has permission to retrive start'''
        # permission_check = check_permission(self.request.user.id, 'Holiday', 'view')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to retrive End'''
        print('**************')
        instance = self.get_object()
        # Customize the response format for retrieving a single instance
        return CustomResponse(code=status.HTTP_200_OK, message="Success", data=AccountBanksViewSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        '''Check user has permission to update start'''
        # permission_check = check_permission(self.request.user.id, 'Holiday', 'update')
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
                bank_name = serializer.validated_data.get('bank')
                branch_name = serializer.validated_data.get('branch_name')
                account_no = serializer.validated_data.get('account_no')
                # If data is provided, use it; otherwise, use the values from the request user
                institution = institution_data if institution_data is not None else self.request.user.institution
                branch = branch_data if branch_data is not None else self.request.user.branch
                if (bank_name==instance.bank and branch_name==instance.branch_name and account_no==instance.account_no):
                    instance = serializer.save()
                    return CustomResponse(code=status.HTTP_200_OK, message="Bank Information Update successfully", data=AccountBanksViewSerializer(instance).data)
                else:
                    bank_count = AccountBanks.objects.filter(bank=bank_name,account_no__iexact=account_no,branch_name__iexact=branch_name,
                                                                institution=institution,branch=branch,status=True).count()
                    if(bank_count==0):
                        # Perform any custom update logic here if needed
                        instance = serializer.save()
                        # Customize the response data
                        return CustomResponse(code=status.HTTP_200_OK, message="Bank Information Update successfully", data=AccountBanksViewSerializer(instance).data)
                    return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Bank Information already exits", data=serializer.errors)
                    # Customize the response format for successful update
            else:
                # Handle validation errors
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message="Validation error", data=serializer.errors)
        except Exception as e:
            # Handle other exceptions
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred during the update", data=str(e))
    
class AccountBankDelete(generics.UpdateAPIView):
    queryset = AccountBanks.objects.all()
    serializer_class = AccountBanksCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires a valid JWT token for access
    
    def partial_update(self, request, *args, **kwargs):
        '''Check user has permission to Delete start'''
        # permission_check = check_permission(self.request.user.id, 'Holiday', 'delete')
        # if not permission_check:
        #     return CustomResponse(code=status.HTTP_401_UNAUTHORIZED, message="Permission denied", data=None)
        '''Check user has permission to Delete End'''
        
        instance = self.get_object()
        if not instance.status:
            return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=f"Bank Information {instance.account_no} already Deleted", data=None)
        # Update the "status" field to False
        instance.status = False
        instance.save()
        # Customize the response format for successful update
        return CustomResponse(code=status.HTTP_200_OK, message=f"Bank Information {instance.account_no} Delete successfully", data=None)


