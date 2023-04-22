import streamlit as st
import numpy as np
from  model import model
from SQLcode import DB
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

styles = """
body {
    background-color: #f0f0f0;
}
"""

# Inject your custom CSS styles into the Streamlit app
st.write(f'<style>{styles}</style>', unsafe_allow_html=True)
st.set_option('deprecation.showPyplotGlobalUse', False)


# Add more descriptive names for each option
st.sidebar.title("Choose an Analysis")
user_input = st.sidebar.selectbox("Select an option", ["Predict Price using ML Model", "Average Price by Company and Model", "Price vs Storage Line Plot"])

db=DB()
if user_input=="Predict Price using ML Model":
    st.write("Welcome to Laptop Insights, your source for data-driven analysis of laptop prices and specifications."
             " Our website provides a variety of insightful visualizations and analyses of laptop data, including scatter plots,"
             " line plots, and correlation matrices. By analyzing trends in laptop prices, screen types, operating systems, and other variables,"
             " our website provides valuable insights for consumers and tech enthusiasts alike. Whether you're looking for the perfect laptop for"
             " work or play, or simply interested in the latest trends in laptop technology, our website has everything you need to stay informed"
             " and make informed decisions.")
    model()
elif user_input == "Average Price by Company and Model":
    # Code for generating average price by company and model
    st.title("CHECK AVG PRICE OF COMPANY WITH EACH MODEL AVAILABLE")
    col1, col2 = st.columns(2)
    Company1, TypeName1 = db.avg_price_with_combo()
    with col1:
        Company1 = st.selectbox("Company", sorted(Company1))
    with col2:
        TypeName1 = st.selectbox("TypeName", sorted(TypeName1))
    if st.button("Avg Price"):
        result = db.fetch_avg_price(Company1, TypeName1)
        avg_price = result[0]  # extract the numerical value from the tuple
        st.write(f"Average Price: {avg_price}")

    st.title("Avg Price Bar Chart to Compare the Avg price d/f btw Companies")
    company_name, avg_price = db.pricevar_withcompany()
    data_dict = {company_name: avg_price for company_name, avg_price in zip(company_name, avg_price)}
    data_dict = dict(sorted(data_dict.items(), key=lambda item: item[1], reverse=True))
    fig = go.Figure(data=[go.Bar(x=list(data_dict.keys()), y=list(data_dict.values()))])
    fig.update_layout(title="Average Price by Company", xaxis_title="Company", yaxis_title="Price")
    st.plotly_chart(fig)


elif user_input=="Price vs RAM Scatter Plot":
    st.title("Price vs RAM Scatter Plot")
    fig, ax = plt.subplots(figsize=(10, 6))
    ram, price = db.fetch_ram_and_price()
    sns.scatterplot(x=ram, y=price, ax=ax)
    ax.set_title("Price vs RAM")
    ax.set_xlabel("RAM (GB)")
    ax.set_ylabel("Price (USD)")
    st.pyplot(fig)

    # heatmap
    df=db.correlation()
    corr_matrix = df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap of Laptop Features')
    plt.show()
    st.pyplot()
elif user_input=="Price vs Storage Line Plot":

    st.title("AVG PRICE VS TOUCHSCREEN")
    TouchScreen, price = db.touch_screen()
    fig = go.Figure(data=go.Bar(x=TouchScreen, y=price))
    fig.update_xaxes(title='TouchScreen')
    fig.update_yaxes(title='PRICE')
    st.plotly_chart(fig)
    st.title("OS VS AVG PRICE")
    os, price = db.operating_system()
    fig = go.Figure(data=go.Bar(x=os, y=price))
    fig.update_xaxes(title='Operating System')
    fig.update_yaxes(title='PRICE')
    st.plotly_chart(fig)

    st.title("Line Plot")
    ppi,hdd,sdd,price,Weight=db.line_plot()
    sns.lineplot(x=ppi,y=price)
    plt.title('How price changes with ppi')
    st.pyplot()
    #
    sns.lineplot(x=hdd, y=price,label='HDD')
    sns.lineplot(x=sdd, y=price,label='SSD')
    plt.title('How Price changes with HDD & SSD')
    plt.xlabel('Storage (GB)')
    plt.ylabel('Price ($)')
    plt.legend()
    st.pyplot()
    sns.lineplot(x=Weight, y=price)
    plt.title('How price changes with Weight')
    st.pyplot()




else:
    pass

