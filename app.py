import pandas as pd

# from openai import OpenAI
from google import genai
from dotenv import load_dotenv
import os
import json



customers = pd.read_csv('data/customers.csv')
orders = pd.read_csv('data/orders.csv')
business_terms = pd.read_csv('data/business_terms.csv')

# print("customers shape: ", customers.shape)
# print("orders shape: ", orders.shape)
# print("business_terms shape: ", business_terms.shape)

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

# print("customers columns: ", customers.columns)
# print("orders columns: ", orders.columns)
# print("business_terms columns: ", business_terms.columns)
# print()
# print(customers.dtypes)
# print()
# print(orders.dtypes)
# print()
# print(business_terms.dtypes)
# print("UNIQUE:")
# print("cities: ", customers["city"].unique())
# print("customer_types: ", customers["customer_type"].unique())
# print("products: ", orders['product'].unique())
# print("statuses: ", orders['status'].unique())

business_dict = {}

for _, row in business_terms.iterrows():
    business_dict[row["business_term"]] = row["meaning"]

# print(business_dict)

## checking if terms are beign found from the question
# question = input("Ask a question: ")

# found_terms = []

# for term in business_dict:
#     if term.lower() in question.lower():
#         found_terms.append(term)

# # print("Found terms: ", found_terms)

# for term in found_terms:
#     print(term, "->", business_dict[term])
#------


load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# response = client.chat.completions.create(
#     model="gpt-5-mini",
#     messages=[
#         {
#             "role": "user",
#             "content": "Say only: OpenAI connection successful"
#         }
#     ]
# )

# print(response.choices[0].message.content)

def get_query_intent(question):

    prompt = f"""
    You are working with business data.

    CUSTOMERS COLUMNS:
    customer_id
    customer_name
    city
    customer_type

    ORDERS COLUMNS:
    order_id
    customer_id
    order_date
    product
    quantity
    sales_value
    status

    Business Terms Dictionary
    Key = Business Term
    Value = Meaning

    {business_dict}

    Available Cities:
    Mumbai
    Pune
    Delhi
    Bengaluru
    Chennai
    Hyderabad

    Available Customer Types:
    Enterprise
    SME
    Distributor

    Available Products:
    Industrial Sensor
    Control Unit
    Automation Panel

    Available Statuses:
    Open
    Closed
    Cancelled

    Allowed Operations:
    sum
    avg
    count
    top_customers
    top_city
    top_products
    list_orders
    

    Rules:
    1. Use ONLY the allowed operations above.
    2. Do NOT invent operation names.
    3. When a business term maps to a dataset field, return the dataset field name.
    Example:
    Revenue -> sales_value
    4. When the user asks for value, revenue, sales, turnover, or order value,
    use (metric = sales_value) and (operation = sum) unless another operation is explicitly requested.
    5. Do NOT invent filters, statuses, date ranges, or business rules that are not supported by:
    - User question
    - Business Terms Dictionary
    - Available columns
    - Available values
    6. If the question is ambiguous but a reasonable interpretation can be made from:
    - User question
    - Business Terms Dictionary
    - Available columns
    - Available values
    then make the assumption and explain it briefly in the assumption field.
    7. Keep assumption under 10 words.
    8. Set clarification_needed = true only when no reasonable interpretation exists.
    9. If a value is not present, return null.
    10. Return ONLY valid JSON.

    JSON Schema:

    {{
        "operation": null,
        "metric": null,
        "city": null,
        "customer_type": null,
        "product": null,
        "status": null,
        "limit": null,
        "assumption": null,
        "clarification_needed": false
    }}

    Question:
    {question}
    """

    # response = client.chat.completions.create(
    #     model="gpt-5-mini",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # )

    # return json.loads(response.choices[0].message.content)
    try:
        response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
        )
        cleaned_response = response.text.replace("```json", "").replace("```", "").strip()

        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Error: {e}")
        # print("Gemini temporarily busy. Try again.")
        return None

# result = get_query_intent("What is revenue from strategic customers?")
# result = get_query_intent("What is the revenue from distributors?")
# result = get_query_intent("What is the revenue from Industrial Sensor?")
# result = get_query_intent("What is the revenue from Mumbai distributors?")
# result = get_query_intent("What is the average sales?")
# result = get_query_intent("How many open orders are there?")
# result = get_query_intent("Who are our top 5 customers?")
# result = get_query_intent("What are our total sales?")
# result = get_query_intent("How much revenue came from Mumbai?")
# result = get_query_intent("Which market performed best?")
# result = get_query_intent("What is the value of Open Orders?")



result = {
    "operation": "sum",
    "metric": "sales_value",
    "city": None,
    "customer_type": None,
    "product": None,
    "status": "Open",
    "limit": None,
    "assumption": None,
    "clarification_needed": False
}
print(result)
print(type(result))
print(execute_query(result))