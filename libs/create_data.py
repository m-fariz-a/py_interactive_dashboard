import random
import pandas as pd

def create_data():
    # Define lists for generating random data
    names = ['John', 'Alice', 'Bob', 'Emma', 'Michael', 'Sophia', 'James', 'Olivia', 'William', 'Ava']
    genders = ['Male', 'Female']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']

    # Generate 100 rows of data
    data = {
        'Name': random.choices(names, k=100),
        'Age': [random.randint(20, 60) for _ in range(100)],
        'Gender': random.choices(genders, k=100),
        'City': random.choices(cities, k=100),
        'Salary': [random.randint(30000, 100000) for _ in range(100)],
        'Married': random.choices(['Yes', 'No'], k=100)
    }
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    return df