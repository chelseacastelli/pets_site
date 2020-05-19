from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

from pets.models import Pet, Appointment


# Create your tests here.
class PetTests(TestCase):
    def test_list_page(self):
        # Instance of user to test the pages
        user = User.objects.create()

        # Create a test pet
        pet = Pet.objects.create(pet_name="Nicky",
                                 species="Dog",
                                 breed='Pomchi',
                                 weight_in_pounds=9,
                                 owner=user)
        pet.save()  # save our pet

        # Making a GET request to check if the pet is in the results (list page)
        res = self.client.get(f'/pets/{pet.id}/')
        # Very a 200 response
        self.assertEqual(res.status_code, 200)
        # Check if the page contains Captain America (our title)
        self.assertContains(res, 'Nicky')
        # Get pet object to check if the user's pet exists
        pet_object = Pet.objects.get(owner=user)
        self.assertEqual(pet_object.owner, user)


