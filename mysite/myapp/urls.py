from django.urls import path
from .views import save_pics, train_model, face_recognition, user_signup, payment, add_money
urlpatterns = [
    path('save-pics', save_pics, name='save-pics'), 
    path('train-model', train_model, name='train-model'), 
    path('face-recognition', face_recognition, name='face-recognition'), 
    path('user-signup', user_signup, name='user-signup'),
    path('payment', payment, name='payment'), 
    path('recharge', add_money,name='add_money')
]