from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from appmsw.models import DbConnection, SysOption
