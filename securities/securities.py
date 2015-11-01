from money import Money
from sqlalchemy.orm import composite
from sqlalchemy.sql import ClauseElement

__author__ = 'mihaildoronin'

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Issuer(object):
    def __init__(self, full_name, short_name, latin_name):
        self.latin_name = latin_name
        self.short_name = short_name
        self.full_name = full_name

    def __composite_values__(self):
        return self.full_name, self.short_name, self.latin_name

    def __repr__(self):
        return u"full name - {}, \n short name - {} \n latin name - {}".\
            format(self.full_name, self.short_name, self.latin_name)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


def get_or_create(session, model, defaults=None, **kwargs):
    entity = session.query(model).filter_by(**kwargs).first()
    if entity:
        return entity, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        entity = model(**params)
        session.add(entity)
        return entity, True


class Security(Base):
    __tablename__ = 'securities'

    id = Column(Integer, primary_key=True, name='SECID')
    full = Column(String, name='NAME')
    short = Column(String, name='SHORTNAME')
    latin = Column(String, name='LATNAME')
    issuer = composite(Issuer, full, short, latin)
    isin = Column(String, name='ISIN')
    reg_number = Column(String, name='REGNUMBER')
    issue_size = Column(Integer, name='ISSUESIZE')
    face_value_amount = Column(Float, name='FACEVALUE')
    face_value_unit = Column(String, name='FACEUNIT')

    def update(self, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

    def remove_attributes(self, *args):
        for attr_name in args:
            if hasattr(self, attr_name):
                setattr(self, attr_name, None)

    @property
    def face_value(self):
        if self.face_value_amount and self.face_value_unit:
            return Money(amount=self.face_value_amount, currency=self.face_value_unit)
        else:
            return None

    @face_value.setter
    def face_value(self, face_value):
        if face_value:
            self.face_value_amount = face_value.amount
            self.face_value_unit = face_value.currency
        else:
            self.face_value_amount = None
            self.face_value_unit = None

    @staticmethod
    def create(_id, issuer, isin, reg_number, issue_size, face_value):
        return Security(
            id=_id,
            issuer=issuer,
            isin=isin,
            reg_number=reg_number,
            issue_size=issue_size,
            face_value=face_value
        )

    def __repr__(self):
        return 'Security {} of issuer {},' \
               'registration_number {},' \
               'ISIN {},' \
               'issue size {},' \
               'face value {}'.format(self.id, self.issuer, self.reg_number, self.isin, self.issue_size, self.face_value)
