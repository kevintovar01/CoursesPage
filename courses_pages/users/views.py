from django.shortcuts import render

# Create your views here.

#CRUD 
def user_create(request):
    # Logic for creating a user
    return render(request, 'user_create.html')

def user_read(request, user_id):
    # Logic for reading a user
    return render(request, 'user_read.html')

def user_update(request, user_id):
    # Logic for updating a user
    return render(request, 'user_update.html')

def user_delete(request, user_id):
    # Logic for deleting a user
    return render(request, 'user_delete.html')