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

# Relationship Analysis
if show_relational_analysis:
    st.header("Relational Analysis")
    default_columns = ['month', 'season']
    sample_cols = st.sidebar.multiselect("Select columns for scatter matrix or categorical analysis", columns, default=default_columns, key='rel_select')
    
    # Check if selected columns are of type string
    if all(df1[col].dtype == 'object' for col in sample_cols):
        # If yes, perform categorical analysis
        for col in sample_cols:
            st.subheader(f"Category Counts for {col}")
            category_counts = df1[col].value_counts()
            fig_bar = px.bar(category_counts, x=category_counts.index, y=category_counts.values, title=f"Category Counts for {col}")
            st.plotly_chart(fig_bar, use_container_width=True)
    elif len(sample_cols) > 1:
        fig_matrix = px.scatter_matrix(df1[sample_cols], color=df1[sample_cols[-1]], 
                                       color_continuous_scale=px.colors.sequential.Viridis,
                                       title="Scatter Matrix for Selected Columns")
        st.plotly_chart(fig_matrix, use_container_width=True)
    else:
        st.warning("Please select more than one column for the scatter matrix or ensure both selected columns are categorical for categorical analysis.")
    
    # ... (rest of the code remains unchanged)
