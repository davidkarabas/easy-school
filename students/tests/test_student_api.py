from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
import datetime
from unittest import mock
from course.models import Course
from ..models import Student


class StudentApiTest(APITestCase):
    API_ENDPOINT = '/api/students/'

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test@gmail.com', password='Pas$w0rd')
        self.course = Course.objects.create(course_name='test', course_description='test_desc')

    def test_success_list_get(self):
        r = self.client.get('{}'.format(self.API_ENDPOINT))

        self.assertEqual(r.status_code, 200)

    @mock.patch('rest_framework.authentication.BasicAuthentication.authenticate')
    def test_success_create(self, auth):
        auth.return_value = (mock.Mock(), None)
        r = self.client.post('{}create/'.format(self.API_ENDPOINT),
                             {
                                 'admission_no': 1,
                                 'date_of_admission': datetime.date.today(),
                                 'first_name': 'first_name',
                                 'last_name': 'last_name',
                                 'gender': 'M',
                                 'date_of_birth': datetime.date.today(),
                                 'is_studying': True,
                                 'current_class': self.course.id
                             }
                             )
        self.assertEqual(r.status_code, 201)
        student = Student.objects.get(id=r.data['id'])
        self.assertEqual(student.admission_no, 1)
        self.assertEqual(student.first_name, 'first_name')
        self.assertEqual(student.last_name, 'last_name')
        self.assertEqual(student.gender, 'M')
        self.assertEqual(student.is_studying, True)

    def test_unauthorized_create(self):
        r = self.client.post('{}create/'.format(self.API_ENDPOINT),
                             {
                                 'admission_no': 1,
                                 'date_of_admission': datetime.date.today(),
                                 'first_name': 'first_name',
                                 'last_name': 'last_name',
                                 'gender': 'M',
                                 'date_of_birth': datetime.date.today(),
                                 'is_studying': True,
                                 'current_class': self.course.id
                             }
                             )
        self.assertEqual(r.status_code, 401)

    @mock.patch('rest_framework.authentication.BasicAuthentication.authenticate')
    def test_success_get_detail(self, auth):
        auth.return_value = (mock.Mock(), None)
        student = Student.objects.create(**{
                                 'admission_no': 1,
                                 'date_of_admission': datetime.date.today(),
                                 'first_name': 'first_name',
                                 'last_name': 'last_name',
                                 'gender': 'M',
                                 'date_of_birth': datetime.date.today(),
                                 'is_studying': True,
                                 'current_class': self.course
                             })
        r = self.client.get('{}{}/'.format(self.API_ENDPOINT, student.id),)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['admission_no'], 1)
        self.assertEqual(r.data['first_name'], 'first_name')
        self.assertEqual(r.data['last_name'], 'last_name')
        self.assertEqual(r.data['gender'], 'M')
        self.assertEqual(r.data['is_studying'], True)

    def test_unauthorized_patch_detail(self):
        student = Student.objects.create(**{
                                 'admission_no': 1,
                                 'date_of_admission': datetime.date.today(),
                                 'first_name': 'first_name',
                                 'last_name': 'last_name',
                                 'gender': 'M',
                                 'date_of_birth': datetime.date.today(),
                                 'is_studying': True,
                                 'current_class': self.course
                             })
        r = self.client.patch('{}{}/'.format(self.API_ENDPOINT, student.id), {'last_name': 'last_name_un'})
        self.assertEqual(r.status_code, 401)

    @mock.patch('rest_framework.authentication.BasicAuthentication.authenticate')
    def test_success_patch_detail(self, auth):
        auth.return_value = (mock.Mock(), None)
        student = Student.objects.create(**{
                                 'admission_no': 1,
                                 'date_of_admission': datetime.date.today(),
                                 'first_name': 'first_name',
                                 'last_name': 'last_name',
                                 'gender': 'M',
                                 'date_of_birth': datetime.date.today(),
                                 'is_studying': True,
                                 'current_class': self.course
                             })
        r = self.client.patch('{}{}/'.format(self.API_ENDPOINT, student.id), {'last_name': 'last_name_un'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['admission_no'], 1)
        self.assertEqual(r.data['first_name'], 'first_name')
        self.assertEqual(r.data['last_name'], 'last_name_un')
        self.assertEqual(r.data['gender'], 'M')
        self.assertEqual(r.data['is_studying'], True)

    @mock.patch('rest_framework.authentication.BasicAuthentication.authenticate')
    def test_success_delete_detail(self, auth):
        auth.return_value = (mock.Mock(), None)
        student = Student.objects.create(**{
                                 'admission_no': 1,
                                 'date_of_admission': datetime.date.today(),
                                 'first_name': 'first_name',
                                 'last_name': 'last_name',
                                 'gender': 'M',
                                 'date_of_birth': datetime.date.today(),
                                 'is_studying': True,
                                 'current_class': self.course
                             })
        r = self.client.delete('{}{}/'.format(self.API_ENDPOINT, student.id),)
        self.assertEqual(r.status_code, 204)
        self.assertEqual(Student.objects.filter(id=student.id).count(), 0)

    def test_unauthorized_delete_detail(self):
        student = Student.objects.create(**{
                                 'admission_no': 1,
                                 'date_of_admission': datetime.date.today(),
                                 'first_name': 'first_name',
                                 'last_name': 'last_name',
                                 'gender': 'M',
                                 'date_of_birth': datetime.date.today(),
                                 'is_studying': True,
                                 'current_class': self.course
                             })
        r = self.client.delete('{}{}/'.format(self.API_ENDPOINT, student.id),)
        self.assertEqual(r.status_code, 401)
        self.assertEqual(Student.objects.filter(id=student.id).count(), 1)
