
def download_csv(dataframe: pd.DataFrame) -> str:
    # The rest of your code for this function...
    csv_string = dataframe.to_csv(index=False, sep=',')
    b64 = base64.b64encode(csv_string.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="download.csv" target="_blank">Download CSV</a>'
    return href

filtered_df = filtered_data.compute() if isinstance(filtered_data, dd.DataFrame) else filtered_data

# Place the download link in the sidebar
st.sidebar.markdown(download_csv(filtered_df), unsafe_allow_html=True)

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
            counts_df = df1[col].value_counts().reset_index()
            counts_df.columns = ['category', 'count']
            fig = px.bar(counts_df, x='category', y='count', title=f"Counts of {col}")
            st.plotly_chart(fig, use_container_width=True)

    else:
        # Scatter plot for numeric columns
        fig = px.scatter(df1, x=column_a, y=column_b, title=f"Relationship between {column_a} and {column_b}")
        
        # Calculate correlation coefficient
        correlation = df1[column_a].corr(df1[column_b])
        
        # Display the scatter plot and the correlation
        st.plotly_chart(fig)
        st.write(f"Correlation coefficient between {column_a} and {column_b}: {correlation:.2f}")
        # Calculate correlation coefficient
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




