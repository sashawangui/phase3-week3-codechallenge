from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'sqlite:///database.db'

engine = create_engine(DATABASE_URI, echo=True)
with engine.connect()as connection:
    alter_statement = text(
        "ALTER TABLE restaurants ADD COLUMN new_column INTEGER")
    connection.execute(alter_statement)


Base = declarative_base()
Session = sessionmaker(bind=engine)


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer)

    def get_customers(self, session):
        customers = session.query(Customer).join(Review).filter(
            Review.restaurant_id == self.id).all()
        for customer in customers:
            print(f"Customer Name: {customer.first_name}")

    def get_reviews(self, session):
        reviews = session.query(Review).filter(
            Review.restaurant_id == self.id).all()
        for review in reviews:
            print(f"Star Rating for the restaurant: {review.star_rating}")

    reviews = relationship("Review", back_populates="restaurant")


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    def get_reviews(self, session):
        reviews = session.query(Review).filter(
            Review.customer_id == self.id).all()
        for review in reviews:
            print(f"Star Rating: {review.star_rating}")

    def get_restaurants(self, session):
        restaurants = session.query(Restaurant).join(
            Review).filter(Review.customer_id == self.id).all()
        for restaurant in restaurants:
            print(f"Restaurant Name: {restaurant.name}")

    reviews = relationship("Review", back_populates="customer")


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer, nullable=False)
    restaurant_id = Column(Integer, ForeignKey(
        'restaurants.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)

    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")


# Create a SQLite database
Base.metadata.create_all(bind=engine)
