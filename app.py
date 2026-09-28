import pandas as pd

customers = pd.read_csv('data/customers.csv')
orders = pd.read_csv('data/orders.csv')
business_terms = pd.read_csv('data/business_terms.csv')

print("customers shape: ", customers.shape)
print("orders shape: ", orders.shape)
print("business_terms shape: ", business_terms.shape)






