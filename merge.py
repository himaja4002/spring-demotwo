import plotly.io as pio
import plotly.figure_factory as ff


pio.templates.default = "plotly_dark"

st.sidebar.title("Visualization Controls")
st.title("Interactive Data Analysis Dashboard")

# Toggle buttons for user to select which visualization to display

show_data_visualization = st.sidebar.checkbox("Data Visualization", value=True)
show_data_quality = st.sidebar.checkbox("Data Quality Analysis", value=True)
show_distribution_analysis = st.sidebar.checkbox("Distribution Analysis", value=True)
show_relational_analysis = st.sidebar.checkbox("Relational Analysis", value=True)

columns = df1.columns

# Visualization - Interactive Plots
if show_data_visualization:
    st.header("Data Visualization")
    x_axis = st.sidebar.selectbox("Select X Axis for Data Visualization", columns, key='x_select')
    y_axis = st.sidebar.selectbox("Select Y Axis for Data Visualization", columns, key='y_select')

    fig = px.scatter(df1, x=x_axis, y=y_axis, color=y_axis, title=f"{y_axis} vs {x_axis}", 
                     color_continuous_scale=px.colors.sequential.Plasma, size_max=15, opacity=0.7)
    st.plotly_chart(fig, use_container_width=True)
    
# Data Quality - Descriptive Statistics
if show_data_quality:
    st.header("Data Quality & Descriptive Analysis")
    
    # Calculating statistics
    mean = df1.mean()
    median = df1.median()
    std_dev = df1.std()
    missing_values = df1.isnull().sum()

    data_quality_df = pd.DataFrame({
        'Mean': mean,
        'Median': median,
        'Standard Deviation': std_dev,
        'Missing Values': missing_values
    })

    fig_quality = px.bar(data_quality_df, title="Data Quality & Descriptive Analysis",
                         color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_quality, use_container_width=True)


# Relationship Analysis
if show_relational_analysis:
    st.header("Relational Analysis")
    default_columns = ['month','season']
    sample_cols = st.sidebar.multiselect("Select columns for scatter matrix", columns, default=default_columns, key='rel_select')
    if len(sample_cols) > 1:
        fig_matrix = px.scatter_matrix(df1[sample_cols], color=df1[sample_cols[-1]], 
                                       color_continuous_scale=px.colors.sequential.Viridis,
                                       title="Scatter Matrix for Selected Columns")
        st.plotly_chart(fig_matrix, use_container_width=True)
    else:
        st.warning("Please select more than one column for the scatter matrix.")

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

    # Add the Relationship Analysis here:
    col1, col2 = st.columns(2)
    column_a = col1.selectbox("Select column A", columns)
    column_b = col2.selectbox("Select column B", columns)

    # Scatter plot
    fig = px.scatter(df1, x=column_a, y=column_b, title=f"Relationship between {column_a} and {column_b}")
    
    # Calculate correlation coefficient
    correlation = df1[column_a].corr(df1[column_b])
    
    # Display the scatter plot and the correlation
    st.plotly_chart(fig)
    st.write(f"Correlation coefficient between {column_a} and {column_b}: {correlation:.2f}")

# Distribution Analysis
if show_distribution_analysis:  # Assuming you want distribution analysis here
    st.header("Distribution Analysis")
    column = st.sidebar.selectbox("Select column for distribution analysis", columns)
    fig = px.histogram(df1, x=column, title=f"Distribution of {column}")
    
    # Customize hovertemplate
    fig.update_traces(hoverinfo='x+y')
    
    st.plotly_chart(fig)
