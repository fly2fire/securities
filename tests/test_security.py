from unittest import TestCase

from money import Money

from securities.securities import Security, Issuer

__author__ = 'mihaildoronin'


class TestSecurity(TestCase):

    def setUp(self):
        self.security = Security.create(1, Issuer('foo', 'bar', 'foobar'), 'isin', '123b', 24, Money(20, 'USD'))

    def test_update(self):
        new_issuer = Issuer('bar', 'foo', 'barfoo')
        new_isin = 'nisi'
        new_reg_number = '321b'
        new_issue_size = 42
        new_face_value = Money(30, 'RUB')
        self.security.update(
            issuer=new_issuer,
            isin=new_isin,
            reg_number=new_reg_number,
            issue_size=new_issue_size,
            face_value=new_face_value
        )
        self.assertEquals(self.security.issuer, new_issuer)
        self.assertEquals(self.security.isin, new_isin)
        self.assertEquals(self.security.reg_number, new_reg_number)
        self.assertEquals(self.security.issue_size, new_issue_size)
        self.assertEquals(self.security.face_value, new_face_value)
        self.security.update(abc='abc')
        self.assertRaises(AttributeError, self._print, self.security)

    def _print(self, obj):
        print(obj.abc)


    def test_remove_attributes(self):
        self.security.remove_attributes('issuer', 'isin', 'face_value')
        self.assertIsNone(self.security.issuer)
        self.assertIsNone(self.security.isin)
        self.assertIsNone(self.security.face_value_unit)
        self.assertIsNone(self.security.face_value_amount)

    def test_face_value(self):
        self.assertEquals(self.security.face_value, Money(20, 'USD'))
        self.security.face_value = Money(30, 'RUB')
        self.assertEquals(self.security.face_value_unit, 'RUB')
        self.assertEquals(self.security.face_value_amount, 30)
        self.security.face_value = None
        self.assertIsNone(self.security.face_value)


