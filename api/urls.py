from django.urls import path
from . import views

urlpatterns = [
    path('tabs/', views.PostTabView.as_view()),
    path('tabs/<int:tab_id>/', views.TabDetailView.as_view()),
    path('tabs/<int:tab_id>/items/', views.AddTabItemView.as_view()),
    path('tabs/<int:tab_id>/payment_intent/', views.CreatePaymentIntentView.as_view()),
    path('tabs/<int:tab_id>/take_payment/', views.TakePaymentView.as_view()),
]