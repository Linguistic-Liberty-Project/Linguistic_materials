from unittest import TestCase

from scratch import get_comments_text


class Test(TestCase):
    def test_get_comments_text(self):
        text = get_comments_text(None)

        self.fail()
