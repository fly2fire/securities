from money import Money
from stocks import Base, Security, Name

__author__ = 'mihaildoronin'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()
security = Security.create(
    name=Name('sber', 'sb', 'sb'),
    isin='234',
    reg_number='234',
    issue_size=234,
    face_value=Money(234, 'USD')
)

session.add(security)
session.commit()
