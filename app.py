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
    6A. If you infer a value for a field, you MUST populate that field.
    Example:
   If "Strategic Customer" is interpreted as an Enterprise customer:

    {{
    "customer_type": "Enterprise",
    "assumption": "Strategic customer interpreted as Enterprise"
    }}
    Do not leave customer_type as null when an inferred value exists.
    6B. Do NOT populate the assumption field when the result is directly derived from:
    - Business Terms Dictionary
    - Available columns
    - Available values
    - Explicit prompt rules
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



def execute_query(intent):
    
    df = orders.merge(customers, on="customer_id")
    # print(df.columns)
    # print(df.shape)
    if intent["status"]:
        df = df[df["status"] == intent["status"]]

    if intent["product"]:
        df = df[df["product"] == intent["product"]]

    if intent["city"]:
        df = df[df["city"] == intent["city"]]

    if intent["customer_type"]:
        df = df[df["customer_type"] == intent["customer_type"]]
    # print(df.shape)
    if intent["operation"] == "sum":
        return df[intent["metric"]].sum()
    elif intent["operation"] == "avg":
        return df[intent["metric"]].mean()
    elif intent["operation"] == "count":
        return len(df)
    elif intent["operation"] == "top_customers":
        return (
            df.groupby("customer_name")[intent["metric"]]
            .sum()
            .sort_values(ascending=False)
            .head(intent["limit"])
        )
    elif intent["operation"] == "top_city":
        return (
            df.groupby("city")[intent["metric"]]
            .sum()
            .sort_values(ascending=False)
            .head(intent["limit"])
        )
    elif intent["operation"] == "top_products":
        return (
            df.groupby("product")[intent["metric"]]
            .sum()
            .sort_values(ascending=False)
            .head(intent["limit"])
        )
    elif intent["operation"] == "list_orders":
        return df
    # print(df.shape)
    return df

def response_format(question, query_result):

    prompt = f"""
    You are a business assistant.

    User Question:
    {question}

    Query Result:
    {query_result}

    Generate a concise business answer.

    The query result may contain:
    - a single value
    - multiple rows
    - rankings
    - grouped summaries

    Use the query result to answer naturally.

    Do not invent information.

    Rules:
    1. Answer using only the query result.
    2. Do not invent numbers.
    3. Do not mention technical terms like JSON, intent, dataframe, query, pandas.
    4. Keep the answer concise.
    5. If the result contains a ranked list, present it naturally.
    6. Return only the answer.
    7. Display sales_value values using ₹ currency format.
    """

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:

        print(f"Error: {e}")

        return "Unable to generate response."

# result = get_query_intent("What are our total sales?")  #q1
# result = get_query_intent("Who are our top 5 customers?")  #q2
# result = get_query_intent("How much revenue came from Mumbai?")  #q3
# result = get_query_intent("What is the value of Open Orders?")  #q4
# result = get_query_intent("Which market performed best?")  #q5

# result = get_query_intent("How many open orders are there?")  #extra 1
# result = get_query_intent("What is the average sales?")   #extra 2

# result = get_query_intent("What is revenue from strategic customers?")  #extra 3
# result = get_query_intent("What is the revenue from distributors?")  #extra 4
# result = get_query_intent("What is the revenue from Industrial Sensor?")  #extra 5    
# result = get_query_intent("What is the revenue from Mumbai distributors?")  #extra 6


# result = {
#     "operation": "top_city",
#     "metric": "sales_value",
#     "city": None,
#     "customer_type": None,
#     "product": None,
#     "status": None,
#     "limit": 1,
#     "assumption": "Market interpreted as city",
#     "clarification_needed": False
# }

# question = "What are our total sales?"    #q1
# question = "Who are our top 5 customers?"     #q2
# question = "How much revenue came from Mumbai?"   #q3
# question = "What is the value of Open Orders?"    #q4
# question = "Which market performed best?"     #q5

# question = "How many open orders are there?"      #extra 1
# question = "What is the average sales?"       #extra 2
# question = "What is revenue from strategic customers?"    #extra 3
# question = "What is the revenue from distributors?"       #extra 4
# question = "What is the revenue from Industrial Sensor?"  #extra 5
# question = "What is the revenue from Mumbai distributors?"     #extra 6

# result = get_query_intent(question)
# print(result)

# print(type(result))

# query_result = execute_query(result)
# print(response_format(question, query_result))

#---------------------------------------------------------

import streamlit as st
st.set_page_config(
    page_title="Business Data Assistant",
    page_icon="📊",
    layout="centered"
)
st.title("Business Data Assistant")



st.markdown(
    """
    Ask questions about sales, customers, products and orders using natural English language.
    """
)

st.subheader("Example Questions")

examples = [
    "What are our total sales?",
    "Who are our top 5 customers?",
    "How much revenue came from Mumbai?",
    "What is the value of Open Orders?",
    "Which market performed best?"
]

for q in examples:
    if st.button(q):
        st.session_state.question = q

question = st.text_input(
    "Ask a business question",
    value=st.session_state.get("question", "")
)

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
            
        
        with st.spinner("Analyzing your question..."):

            intent = get_query_intent(question)

            if intent["clarification_needed"]:
                st.warning("Please clarify your question.")

            else:
                # Challenge C - Show Interpretation
                st.subheader("How I Interpreted Your Question")

                for key, value in intent.items():
                    if value is not None and key not in ["clarification_needed", "assumption"]:
                        st.write(f"• {key.replace('_', ' ').title()}: {value}")
                query_result = execute_query(intent)

                answer = response_format(
                    question,
                    query_result
                )

                st.success(answer)

                if intent["assumption"]:
                    st.info(
                        f"Assumption: {intent['assumption']}"
                    )

