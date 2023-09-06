from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine, create_engine, insert
from sqlalchemy.ext.declarative import declarative_base
from tables import *

# Usage example
if __name__ == "__main__":
    session = Session()

    # Create sample data
    customer1 = Customer(first_name="Sasha", last_name="Iluku")
    customer2 = Customer(first_name="Joyce", last_name="Wangui")
    restaurant1 = Restaurant(name="Brew Bistro", price=3000)
    restaurant2 = Restaurant(name="CJ's", price=2000)
    review1 = Review(star_rating=4, restaurant=restaurant1, customer=customer1)
    review2 = Review(star_rating=5, restaurant=restaurant1, customer=customer2)
    review3 = Review(star_rating=3, restaurant=restaurant2, customer=customer2)

    # Add data to the session and commit to the database
    session.add_all([customer1, customer2, restaurant1, restaurant2, review1, review2, review3])
    session.commit()

    # Retrieve and print customer's reviews and restaurants
    customer1.get_reviews(session)
    customer1.get_restaurants(session)

    # Retrieve and print restaurant's customers and reviews
    restaurant1.get_customers(session)
    restaurant1.get_reviews(session)

    session.close()
