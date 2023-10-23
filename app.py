import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import os

def get_db_connection():
    connection = mysql.connector.connect(
        host="kuskuam-data-1.cmsqpdu6xv2x.us-east-1.rds.amazonaws.com",
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME')
    )
    return connection


def main():
    st.title("Kuaskuam Mariam Church Fundraising Event")
    st.image("https://github.com/0xtibs/kuskuam/raw/main/CdL2dybUAAAmjh9.png", use_column_width=True)



    donor_name = st.text_input("Donor Name")
    kiristina_name = st.text_input("Kiristina Name")
    amount = st.number_input("Given Amount", min_value=0.0, step= 0.01)


    if st.button("Add Donation"):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO donations (donor_name, kiristina_name, amount) VALUES (%s,%s,%s)"
        cursor.execute(query, (donor_name, kiristina_name, amount))
        conn.commit()
        cursor.close()
        conn.close()

    conn = get_db_connection()
    total_amount = pd.read_sql("SELECT SUM(amount) as total FROM donations", conn).iloc[0]['total']
    st.write(f"Total Amount Raised: ${total_amount:.2f}")
    target_amount = 10000  # set this to your fundraising goal

    fig, ax = plt.subplots()

    ax.bar(['Target', 'Raised'], [target_amount, total_amount], color=['gray', 'blue'])

    ax.set_ylabel('Amount ($)')
    ax.set_title('Fundraising Progress')
    ax.set_ylim(0, target_amount * 1.2)  # set y-axis limit to 120% of the target for better visualization

    st.pyplot(fig)
    conn.close()


main()

