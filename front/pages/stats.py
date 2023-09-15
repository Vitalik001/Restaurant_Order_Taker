import streamlit as st
import requests
import matplotlib.pyplot as plt
BACKEND_URL = "http://app:80/admin"



st.set_page_config(page_title="Stats", page_icon="📊")

# Make a request to the admin/orders endpoint
orders_response = requests.get(f"{BACKEND_URL}/stats")
orders_data = orders_response.json()
upsell_stats = orders_data["upsell_stats"]
st.title("Upsell Statistics")

# Create a Matplotlib figure with subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Plot 1: Bar chart for accepted and rejected upsells
labels = ['Accepted', 'Rejected']
values = [upsell_stats['accepted'], upsell_stats['rejected']]
axes[0].bar(labels, values)
axes[0].set_title('Accepted vs Rejected')

# Plot 2: Pie chart for questions asked and accepted
labels2 = ['Questions Asked', 'Accepted']
sizes2 = [upsell_stats['questions_asked'], upsell_stats['accepted']]
axes[1].pie(sizes2, labels=labels2, autopct='%1.1f%%', startangle=90)
axes[1].set_title('Questions Asked vs Accepted')
axes[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

total_revenue = upsell_stats['total_upsell_revenue']
total_revenue_text = f"Total Upsell Revenue: ${total_revenue:.2f}"
fig.text(0.5, 0.05, total_revenue_text, ha='center', fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.7))

# Display the Matplotlib figure in Streamlit

st.pyplot(fig)
