st.sidebar.title("Visualization Controls")
st.title("Interactive Data Analysis Dashboard")

# Dropdown for user to first select 'Interactive Data Visualization'
visualization_options = ["Select an Option", "Interactive Data Visualization"]
selected_option = st.sidebar.selectbox("Choose a Visualization Type:", visualization_options)

# If the user selects 'Interactive Data Visualization' from the dropdown, display other 4 checkboxes
if selected_option == "Interactive Data Visualization":
    show_data_visualization = st.sidebar.checkbox("Data Visualization", value=True)
    show_data_quality = st.sidebar.checkbox("Data Quality Analysis", value=True)
    show_distribution_analysis = st.sidebar.checkbox("Distribution Analysis", value=True)
    show_relational_analysis = st.sidebar.checkbox("Relational Analysis", value=True)
else:
    show_data_visualization = False
    show_data_quality = False
    show_distribution_analysis = False
    show_relational_analysis = False

columns = df1.columns
