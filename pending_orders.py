import streamlit as st

st.title("Pending Smoothie Orders")

cnx = st.connection("snowflake")
session = cnx.session()

# Read orders
orders_df = session.sql("""
    SELECT *
    FROM smoothies.public.orders
""").to_pandas()

st.write("All Orders:")
st.dataframe(orders_df)

# Show only pending orders
pending_df = orders_df[orders_df["order_filled"] == False]

st.subheader("Pending Orders")

for index, row in pending_df.iterrows():
    st.write(f"Order ID: {row['order_id']} | Name: {row['name_on_order']}")

    if st.button(f"Mark Filled {row['order_id']}"):
        session.sql(f"""
            UPDATE smoothies.public.orders
            SET order_filled = TRUE
            WHERE order_id = {row['order_id']}
        """).collect()

        st.success(f"Order {row['order_id']} marked as filled!")
