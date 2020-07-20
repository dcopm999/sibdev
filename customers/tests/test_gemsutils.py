from django.test import TestCase

from customers.gems_utils import Gems


class GemUtilsCase(TestCase):
    def setUp(self):
        self.gems = Gems()
        pass
