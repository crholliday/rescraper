from django.test import TestCase

from .models import Property
...

class PropertyTests(TestCase):
    """Property model tests."""

    def test_str(self):

        property = Property(address='123 Main Street, Somewhere, OK', is_commercial=False)

        self.assertEquals(
            str(property),
            '123 Main Street, Somewhere, OK',
        )
