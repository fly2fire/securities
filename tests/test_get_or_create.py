# coding=utf-8
from unittest import TestCase
from money import Money
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stocks.securities import Base, get_or_create, Security, Name

__author__ = 'mihaildoronin'


class TestGet_or_create(TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)

        self.session = Session()

    def test_get_or_create(self):
        correct_name = Name('foo', 'bar', 'foobar')
        correct_isin = '123'
        correct_reg_number = '123b'
        correct_issue_size = 43
        correct_face_value = Money(100, 'USD')
        correct_id = 1
        security, created = get_or_create(
            self.session,
            Security,
            id=correct_id,
            full=correct_name.full,
            short=correct_name.short,
            latin=correct_name.latin,
            isin=correct_isin,
            reg_number=correct_reg_number,
            issue_size=correct_issue_size,
            face_value_amount=correct_face_value.amount,
            face_value_unit=correct_face_value.currency
        )
        self.assertTrue(created)
        self.assertEquals(security.name, correct_name)
        self.assertEquals(security.isin, correct_isin)
        self.assertEquals(security.reg_number, correct_reg_number)
        self.assertEquals(security.issue_size, correct_issue_size)
        self.assertEquals(security.face_value, correct_face_value)
        self.assertEquals(security.id, correct_id)
        security_2, created = get_or_create(
            self.session,
            Security,
            id=correct_id,
            full=correct_name.full,
            short=correct_name.short,
            latin=correct_name.latin,
            isin=correct_isin,
            reg_number=correct_reg_number,
            issue_size=correct_issue_size,
            face_value_amount=correct_face_value.amount,
            face_value_unit=correct_face_value.currency
        )
        self.assertFalse(created)
        self.assertEquals(security_2, security)

