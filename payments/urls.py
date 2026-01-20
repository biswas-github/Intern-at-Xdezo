from django.urls import path,include
from payments.views import ViewPayment,AddPayment,UpdatePayment,DeletePayment,DuesAndOverDues
# url pattrns
urlpatterns = [
    
# -------Finance---------#
    path('ViewPayment',ViewPayment,name="ViewPayment"),
    # AddPayment
    path('AddPayment',AddPayment,name="AddPayment"),
    # UpdatePayment
    path('UpdatePayment/<int:id>',UpdatePayment,name="UpdatePayment"),
    path('DeletePayment/<int:id>',DeletePayment,name="DeletePayment"),
    # Dues and overdues
    path('DuesAndOverDues',DuesAndOverDues,name="DuesAndOverDues"),

]
