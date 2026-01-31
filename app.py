#create the streamlit app
# importing the needed libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
# set default template
st.set_page_config(page_title="Logistics Dashboard", layout="wide")
# load the cleaned data
df = pd.read_csv('final_cleaned_data.csv')
# initialize session state
if 'view' not in st.session_state:
    st.session_state.view = "home"
# create the bar for navigation
st.title("🚚 Olist Logistics Analysis")
st.info("Developed by Arwa Wesam Elsayed")

st.markdown("Select a category to view the insights:")

col1, col2, col3, col4, col5 = st.columns(5)
# add images to the buttons
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830305.png", width=80) 
    if st.button("Delivery Performance"):
        st.session_state.view = "delivery"

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/9422/9422831.png", width=80) 
    if st.button("Sales Categories"):
        st.session_state.view = "sales"

with col3:
    st.image("https://cdn-icons-png.flaticon.com/512/854/854878.png", width=80) 
    if st.button("Geographic Impact"):
        st.session_state.view = "geographic"

with col4:
    st.image("https://cdn-icons-png.flaticon.com/512/1698/1698535.png", width=80) 
    if st.button("Customer satisfaction"):
        st.session_state.view = "customer"

with col5:
    st.image("https://cdn-icons-png.flaticon.com/512/411/411712.png", width=80) 
    if st.button("Logistics Segments"):
        st.session_state.view = "logistics"

st.divider()
#actions based on the selected view
if st.session_state.view == "delivery":
    st.subheader("📉 Delivery Delay Analysis")
    df = df.sort_values(by='order_approved_at')
    df['cumulative_delay_rate'] = (df['delay'].expanding().mean() * 100).round(2)
    
    fig1 = px.line(df, x='order_approved_at', y='cumulative_delay_rate', template='plotly_dark')
    fig2 = px.histogram(df, x='delivery_time', nbins=30, template='plotly_dark')
    
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

elif st.session_state.view == "sales":
    st.subheader("😎 Top Categories by Sales")
    sales_by_category = df.groupby('product_category_name_english')['price'].sum().nlargest(10).reset_index()
    pull_values = [0.2, 0.1, 0.05] + [0] * 7
    
    figPie = px.pie(sales_by_category, names='product_category_name_english', values='price', hole=0.3, template='plotly_dark')
    figPie.update_traces(pull=pull_values, textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))
    
    st.plotly_chart(figPie, use_container_width=True)

elif st.session_state.view == "geographic":
    st.subheader("🌍 Map of Delays")
    state_delay = df.groupby('seller_state')['delay'].mean().reset_index().nlargest(10, 'delay')
    state_delay_fig = px.bar(state_delay, x='seller_state', y='delay', color='delay', color_continuous_scale='Viridis_r', template='plotly_dark')
    
    city_delay = df.groupby('seller_city')['delay'].mean().reset_index().nlargest(10, 'delay')
    city_delay_fig = px.bar(city_delay, x='delay', y='seller_city', orientation='h', color='delay', color_continuous_scale='Magma_r', template='plotly_dark')
    
    st.plotly_chart(state_delay_fig, use_container_width=True)
    st.plotly_chart(city_delay_fig, use_container_width=True)

elif st.session_state.view == "logistics":
    st.subheader("📦 Logistics Segments Analysis")
    corr_df = df[['approval_time_hrs', 'shipping_prep_hrs', 'carrier_delivery_hrs', 'delay']].corr()
    figCorr = px.imshow(corr_df, text_auto=True, color_continuous_scale='RdBu_r', template='plotly_dark')
    st.plotly_chart(figCorr, use_container_width=True)

elif st.session_state.view == "customer":
    st.subheader("⭐ Customer Satisfaction Analysis")
    customerFig = px.box(df, x="price_segment", y="review_score", color='price_segment', template='plotly_dark')
    delayFig = px.scatter(df, x="delay", y="review_score", color='review_score', color_continuous_scale='Purp_r', template='plotly_dark')
    
    st.plotly_chart(customerFig, use_container_width=True)
    st.plotly_chart(delayFig, use_container_width=True)
