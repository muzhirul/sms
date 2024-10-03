from rest_framework.response import Response
from sms.pagination import CustomPagination
from rest_framework import generics
from django.db.models import F, Window, Sum
from .models import *
from .serializers import *
from rest_framework import generics, permissions
    

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
        queryset = AccountLedger.objects.filter(status=True, acc_coa=8).annotate(
                balance=Window(
                    expression=Sum(F('debit_amt') - F('credit_amt')),
                    partition_by=[F('acc_coa')],
                    order_by=F('gl_date').asc()
                )
            )
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
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     response_data = self.get_paginated_response(serializer.data).data
        # else:
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "code": 200,
            "message": "Success",
            "data": serializer.data,
        }

        return Response(response_data)