import pandas as pd

customers = pd.read_csv('data/customers.csv')
orders = pd.read_csv('data/orders.csv')
business_terms = pd.read_csv('data/business_terms.csv')

print("customers shape: ", customers.shape)
print("orders shape: ", orders.shape)
print("business_terms shape: ", business_terms.shape)

customers.columns = customers.columns.str.strip().str.lower()
orders.columns = orders.columns.str.strip().str.lower()
business_terms.columns = business_terms.columns.str.strip().str.lower()

customers = customers.apply(
    lambda col: col.str.strip() if col.dtype == "object" else col
)

orders = orders.apply(
    lambda col: col.str.strip() if col.dtype == "object" else col
)

business_terms = business_terms.apply(
    lambda col: col.str.strip() if col.dtype == "object" else col
)

print("customers columns: ", customers.columns)
print("orders columns: ", orders.columns)
print("business_terms columns: ", business_terms.columns)
print()
print(customers.dtypes)
print()
print(orders.dtypes)
print()
print(business_terms.dtypes)
print("UNIQUE:")
print("cities: ", customers["city"].unique())
print("customer_types: ", customers["customer_type"].unique())
print("products: ", orders['product'].unique())
print("statuses: ", orders['status'].unique())



