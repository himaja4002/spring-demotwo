st.markdown("""
    <style>
        body {
            background-color: #1e1e1e;
            color: #FFF;
        }
        .reportview-container .main .block-container {
            padding: 2rem;
            max-width: 1024px;
        }
        h2 {
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .sidebar .sidebar-content {
        background-color: #F7F7F7;
        padding: 10px 20px;
        }
        select[data-baseweb="select"] {
        min-height: 30px;
        font-size: 14px;
        border-radius: 8px;
        outline: none;
        }
        .st-expander > div:after {
        font-size: 16px;
        font-weight: bold;
        }
        .st-expander > header {
        padding: 8px 12px;
        background-color: #E0E0E0;
        }
        .st-expander > header:hover {
        background-color: #C0C0C0;
        }
    </style>
""", unsafe_allow_html=True)

show_relational_analysis = True

if show_relational_analysis:
    st.header("Relational Analysis")
    default_columns = ['month','season']
    sample_cols = st.sidebar.multiselect("Select columns for scatter matrix", columns, default=default_columns, key='rel_select')
    
    # Scatter Matrix for numeric columns
    if len(sample_cols) > 1:
        if df1[sample_cols].select_dtypes(include=['number']).shape[1] > 1:
            fig_matrix = px.scatter_matrix(df1[sample_cols], color=df1[sample_cols[-1]], 
                                           color_continuous_scale=px.colors.sequential.Viridis,
                                           title="Scatter Matrix for Selected Columns")
            st.plotly_chart(fig_matrix, use_container_width=True)
        else:
            st.warning("Selected columns are non-numeric. Choose numeric columns for the scatter matrix.")
    
    # Heatmap for Correlation matrix
    numeric_columns = df1.select_dtypes(include=['number'])
    correlation_matrix = numeric_columns.corr()
    fig_heatmap = ff.create_annotated_heatmap(
        z=correlation_matrix.values, 
        x=list(correlation_matrix.columns), 
        y=list(correlation_matrix.index), 
        annotation_text=correlation_matrix.round(2).values,
        colorscale='Viridis'
    )
    fig_heatmap.update_layout(title="Correlation Heatmap")
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Relationship Analysis
    col1, col2 = st.columns(2)
    column_a = col1.selectbox("Select column A", columns)
    column_b = col2.selectbox("Select column B", columns)
    
    if df1[column_a].dtype == 'object' or df1[column_b].dtype == 'object':
        # Grouped bar chart for two categorical columns
        if df1[column_a].dtype == 'object' and df1[column_b].dtype == 'object':
            cross_tab = pd.crosstab(df1[column_a], df1[column_b])
            fig = px.imshow(cross_tab, title=f"Cross Tabulation between {column_a} and {column_b}")
            st.plotly_chart(fig, use_container_width=True)
        
        # Bar chart for one categorical column
        else:
            col = column_a if df1[column_a].dtype == 'object' else column_b
            fig = px.bar(df1[col].value_counts().reset_index(), x='index', y=col, title=f"Counts of {col}")
            st.plotly_chart(fig, use_container_width=True)

    else:
        # Scatter plot for numeric columns
        fig = px.scatter(df1, x=column_a, y=column_b, title=f"Relationship between {column_a} and {column_b}")
        
        # Calculate correlation coefficient
        correlation = df1[column_a].corr(df1[column_b])
        
        # Display the scatter plot and the correlation
        st.plotly_chart(fig)
        st.write(f"Correlation coefficient between {column_a} and {column_b}: {correlation:.2f}")

# Interpretation of correlation
if correlation > 0.7: # Strong positive correlation
    st.write(f"The attributes {column_a} and {column_b} have a strong positive correlation with a coefficient of {correlation:.2f}. This means they are directly proportional.")
elif correlation > 0: # Weak positive correlation
    st.write(f"The attributes {column_a} and {column_b} have a weak positive correlation with a coefficient of {correlation:.2f}.")
elif correlation < -0.7: # Strong negative correlation
    st.write(f"The attributes {column_a} and {column_b} have a strong negative correlation with a coefficient of {correlation:.2f}. This means they are inversely proportional.")
elif correlation < 0: # Weak negative correlation
    st.write(f"The attributes {column_a} and {column_b} have a weak negative correlation with a coefficient of {correlation:.2f}.")
else: # No correlation
    st.write(f"The attributes {column_a} and {column_b} do not have a linear correlation with a coefficient of {correlation:.2f}.")


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

st.sidebar.markdown("## Navigation", unsafe_allow_html=True)
st.sidebar.markdown("------")

col1, col2, col3 = st.sidebar.columns([1, 2, 1])  # Adjust the middle value to control width
with col2:
    selected_configuration_type = st.selectbox("Choose Configuration Type (Parent)", options=["-"] + CONFIGURATION_TYPES)

st.sidebar.markdown("<br>", unsafe_allow_html=True) 

# Main Screen Content
if selected_configuration_type != "-":

    st.write("### Configuration: ", selected_configuration_type)  # Give a title for clarity

    # Load Template Section
    with st.expander("Load Template"):
        col1, col2, col3 = st.columns([1, 6, 1])  # Adjust the middle value to control width
        with col2:
            templates = st.session_state.configs.get(selected_configuration_type, {})
            selected_template = st.selectbox("Choose Template", options=["-"] + list(templates.keys()))
        
        if selected_template != "-" and st.button("Load Selected Template"):
            st.session_state.filters = templates[selected_template]
            st.session_state.filter_added = True
            
            with st.spinner("Applying filters..."):
                df = data.compute()
                filtered_data = apply_filters(df, st.session_state.filters)
                record_count = len(filtered_data)  
                st.success(f"Number of records: {record_count}")

    # Save New Template Section
    with st.expander("Save New Template"):
        new_template_name = st.text_input("Template Name")
        
        if new_template_name and st.button("Save Template"):
            if selected_configuration_type not in st.session_state.configs:
                st.session_state.configs[selected_configuration_type] = {}
            
            if new_template_name in st.session_state.configs[selected_configuration_type]:
                st.warning(f"Template {new_template_name} already exists under {selected_configuration_type}. If you want to overwrite it, delete the existing one first.")
            else:
                st.session_state.configs[selected_configuration_type][new_template_name] = st.session_state.filters
                save_configs_to_file(st.session_state.configs)
                st.success(f"Saved filters as {new_template_name} under {selected_configuration_type}!")

    # Delete Template Section
    with st.expander("Delete Template"):
        col1, col2, col3 = st.columns([1, 6, 1])  # Adjust the middle value to control width
        with col2:
            delete_template_name = st.selectbox("Choose Template to Delete", options=["-"] + list(templates.keys()))
        
        if delete_template_name != "-" and st.button("Delete Template"):
            del st.session_state.configs[selected_configuration_type][delete_template_name]
            save_configs_to_file(st.session_state.configs)
            st.success(f"Deleted {delete_template_name} template under {selected_configuration_type}!")

# Sidebar Content
st.sidebar.markdown("## Navigation", unsafe_allow_html=True)
st.sidebar.markdown("------")

selected_configuration_type = st.sidebar.selectbox("Choose Configuration Type (Parent)", options=["-"] + CONFIGURATION_TYPES)
st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Adding a bit of space

# Expandable Filter Section
with st.sidebar.expander("Add New Filter", expanded=True):
    # Include filter controls here

st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Adding a bit of space
st.sidebar.markdown("## Visualization Controls", unsafe_allow_html=True)
st.sidebar.markdown("------")




