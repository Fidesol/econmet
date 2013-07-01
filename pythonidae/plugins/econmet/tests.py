# -*- coding: utf-8 -*-
__autor__ = "Maria del Mar Jiménez Torres, Fundación I+D del Software Libre"
__email__ = "mjimenez@fidesol.org"
__date__ = "10/05/2012"

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
