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