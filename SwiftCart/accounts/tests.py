# accounts/tests.py
import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User, Group

@pytest.mark.django_db
def test_register_user():
    # Register a new user with role "Customer"
    url = reverse('register')
    data = {
        'username': 'testuser',
        'password': 'testpassword123',
        'role': 'Customer',
    }
    response = pytest.client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == "User created successfully!"
    
    # Check if the user is assigned to the correct group
    user = User.objects.get(username='testuser')
    customer_group = Group.objects.get(name='Customer')
    assert customer_group in user.groups.all()

@pytest.mark.django_db
def test_login_user():
    # First register the user
    user = User.objects.create_user(username='testuser', password='testpassword123')
    group = Group.objects.create(name='Customer')
    user.groups.add(group)
    
    # Login and obtain JWT tokens
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'testpassword123',
    }
    response = pytest.client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_product_list_authenticated():
    # Register a user and log them in to get an access token
    user = User.objects.create_user(username='testuser', password='testpassword123')
    group = Group.objects.create(name='Customer')
    user.groups.add(group)
    
    # Login to get token
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'testpassword123',
    }
    response = pytest.client.post(url, data)
    token = response.data['access']
    
    # List products (using the token)
    product_url = reverse('product_list')
    response = pytest.client.get(product_url, HTTP_AUTHORIZATION=f'Bearer {token}')
    
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)  # Should return a list of products

@pytest.mark.django_db
def test_product_manage_sales_manager():
    # First, create a Sales Manager user
    user = User.objects.create_user(username='salesmanager', password='salespassword123')
    group = Group.objects.create(name='Sales Manager')
    user.groups.add(group)
    
    # Login to get token
    url = reverse('login')
    data = {
        'username': 'salesmanager',
        'password': 'salespassword123',
    }
    response = pytest.client.post(url, data)
    token = response.data['access']
    
    # Add a product (using the token)
    product_url = reverse('product_manage')
    data = {
        'name': 'Product1',
        'price': 99.99,
        'stock': 100,
        'description': 'A test product'
    }
    response = pytest.client.post(product_url, data, HTTP_AUTHORIZATION=f'Bearer {token}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Product created successfully!'

@pytest.mark.django_db
def test_product_manage_forbidden_for_customer():
    # First, create a Customer user
    user = User.objects.create_user(username='customer', password='customerpassword123')
    group = Group.objects.create(name='Customer')
    user.groups.add(group)
    
    # Login to get token
    url = reverse('login')
    data = {
        'username': 'customer',
        'password': 'customerpassword123',
    }
    response = pytest.client.post(url, data)
    token = response.data['access']
    
    # Try to add a product (should be forbidden for Customer)
    product_url = reverse('product_manage')
    data = {
        'name': 'Product1',
        'price': 99.99,
        'stock': 100,
        'description': 'A test product'
    }
    response = pytest.client.post(product_url, data, HTTP_AUTHORIZATION=f'Bearer {token}')
    assert response.status_code == status.HTTP_403_FORBIDDEN
