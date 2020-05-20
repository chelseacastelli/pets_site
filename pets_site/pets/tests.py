from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

from pets.models import Pet, Appointment


# Create your tests here.
class PetTests(TestCase):
    def test_list_page(self):

        user = User.objects.create()

        pet = Pet.objects.create(pet_name="Nicky",
                                 species="Dog",
                                 breed='Pomchi',
                                 weight_in_pounds=9,
                                 owner=user)
        pet.save()

        res = self.client.get(f'/pets/{pet.id}/')

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Nicky')

        pet_object = Pet.objects.get(owner=user)
        self.assertEqual(pet_object.owner, user)

        def test_detail_page(self):
            user = User.objects.create_user(username='admin', password='djangopony')
            self.client.login(username='admin', password='djangopony')

            pet = Pet.objects.create(pet_name='Bruce',
                                     species='Cat',
                                     breed='British Shorthair',
                                     weight_in_pounds=9.8,
                                     owner=user)
            pet.save()

            appointment = Appointment.objects.create(date_of_appointment=timezone.now(),
                                                     duration_minutes=30,
                                                     special_instructions='She isn\'t playful',
                                                     pet=pet)
            appointment.save()
            res = self.client.get(f'/pets/{pet.id}/')
            self.assertEqual(res.status_code, 200)

            pet_object = Pet.objects.get(pet_name='Bruce')
            self.assertEqual(pet_object.pet_name, 'Bruce')

        def test_pet_create_page(self):
            user = User.objects.create()
            post_data = {
                'pet_name': 'Spot',
                'species': 'Dog',
                'breed': 'Hound',
                'weight_in_pounds': 68,
                'owner': user.id
            }

            res = self.client.post('/pet/create/', data=post_data)
            self.assertEqual(res.status_code, 302)

            pet_object = Pet.objects.get(pet_name='Spot')
            self.assertEqual(pet_object.pet_name, 'Spot')

        def test_create_appointment_page(self):
            user = User.objects.create()

            pet = Pet.objects.create(pet_name='Holly',
                                     species='Dog',
                                     breed='Mix',
                                     weight_in_pounds=50,
                                     owner=user)
            pet.save()

            post_data = {
                'date_of_appointment': '2020-2-2',
                'duration_minutes': 90,
                'special_instructions': 'Scoop and a half of her food, twice',
                'pet': pet
            }

            res = self.client.post('/appointment/create/', data=post_data)
            self.assertEqual(res.status_code, 200)

            app_object = Appointment.objects.get(date_of_appointment='2020-2-2')
            self.assertEqual(app_object.date_of_appointment,
                             datetime.date(2020, 2, 2))
