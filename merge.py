# Set a visually pleasing theme for plotly
import plotly.io as pio
import plotly.figure_factory as ff


pio.templates.default = "plotly_dark"

# Organize the layout using sidebar for controls and main area for visualizations
st.sidebar.title("Visualization Controls")
st.title("Interactive Data Analysis Dashboard")

# Toggle buttons for user to select which visualization to display

show_data_visualization = st.sidebar.checkbox("Data Visualization", value=True)
show_data_quality = st.sidebar.checkbox("Data Quality Analysis", value=True)
show_distribution_analysis = st.sidebar.checkbox("Distribution Analysis", value=True)
show_relational_analysis = st.sidebar.checkbox("Relational Analysis", value=True)

# Visualization - Interactive Plots
if show_data_visualization:
    st.header("Data Visualization")
    columns = df1.columns
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

# Distribution Analysis - Categorical Columns
if show_distribution_analysis:
    st.header("Distribution Analysis")
    categorical_col = st.sidebar.selectbox("Select a Categorical Column for Distribution Analysis", columns, key='cat_select')
    value_counts = df1[categorical_col].value_counts()

    fig_value_counts = px.bar(value_counts, title=f"Distribution of {categorical_col}", 
                              color=value_counts, color_continuous_scale=px.colors.sequential.Agsunset,
                              text=value_counts)
    fig_value_counts.update_traces(texttemplate='%{text}', textposition='outside')
    
    # Showing min and max values
    st.write(f"Min Value of {categorical_col}: {df1[categorical_col].min()}")
    st.write(f"Max Value of {categorical_col}: {df1[categorical_col].max()}")
    
    st.plotly_chart(fig_value_counts, use_container_width=True)
# Relational Analysis
if show_relational_analysis:
    st.header("Relational Analysis")

    # Scatter Matrix (Pair plot) for a subset of columns
    sample_cols = st.sidebar.multiselect("Select columns for scatter matrix", columns, default=columns[:4], key='rel_select')
    if len(sample_cols) > 1:
        fig_matrix = px.scatter_matrix(df1[sample_cols], color=df1[sample_cols[-1]], 
                                       color_continuous_scale=px.colors.sequential.Viridis,
                                       title="Scatter Matrix for Selected Columns")
        st.plotly_chart(fig_matrix, use_container_width=True)
    else:
        st.warning("Please select more than one column for the scatter matrix.")

    # Heatmap for Correlation matrix
    correlation_matrix = df1.corr()
    fig_heatmap = ff.create_annotated_heatmap(
        z=correlation_matrix.values, 
        x=list(correlation_matrix.columns), 
        y=list(correlation_matrix.index), 
        annotation_text=correlation_matrix.round(2).values,
        colorscale='Viridis'
    )
    fig_heatmap.update_layout(title="Correlation Heatmap")
    st.plotly_chart(fig_heatmap, use_container_width=True)
