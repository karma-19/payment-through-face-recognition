from django.urls import path
from .views import save_pics, train_model, face_recognition
urlpatterns = [
    path('save-pics', save_pics, name='save-pics'), 
    path('train-model', train_model, name='train-model'), 
    path('face-recognition', face_recognition, name='face-recognition')
]