from rest_framework.response import Response
from sms.pagination import CustomPagination
from rest_framework import generics
from django.db.models import F, Window, Sum, Count
from .models import *
from .serializers import *
from rest_framework import generics, permissions
from datetime import datetime
from sms.utils import CustomResponse
from rest_framework import status
    

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
                        order_by=F('gl_date').asc()
                    )
                )
        else:
            queryset = AccountLedger.objects.filter(status=True).annotate(
                    balance=Window(
                        expression=Sum(F('debit_amt') - F('credit_amt')),
                        partition_by=[F('acc_coa')],
                        order_by=F('gl_date').asc()
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
        response_data = {
            "code": 200,
            "message": "Success",
            "data": serializer.data,
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
    

    