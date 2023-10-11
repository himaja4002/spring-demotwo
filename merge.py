# Set a visually pleasing theme for plotly
import plotly.io as pio

pio.templates.default = "plotly_dark"

# Organize the layout using sidebar for controls and main area for visualizations
st.sidebar.title("Visualization Controls")
st.title("Interactive Data Analysis Dashboard")

# Toggle buttons for user to select which visualization to display
show_data_visualization = st.sidebar.checkbox("Data Visualization", value=True)
show_data_quality = st.sidebar.checkbox("Data Quality Analysis", value=True)
show_distribution_analysis = st.sidebar.checkbox("Distribution Analysis", value=True)

# Visualization - Interactive Plots
if show_data_visualization:
    st.header("Data Visualization")
    columns = df1.columns
    x_axis = st.sidebar.selectbox("Select X Axis for Data Visualization", columns, key='x_select')
    y_axis = st.sidebar.selectbox("Select Y Axis for Data Visualization", columns, key='y_select')
    
    # Enhanced scatter plot with color scale based on Y values, size adjustments, and opacity for better visualization
    fig = px.scatter(df1, x=x_axis, y=y_axis, color=y_axis, title=f"{y_axis} vs {x_axis}", 
                     color_continuous_scale=px.colors.sequential.Plasma, size_max=15, opacity=0.7)
    st.plotly_chart(fig, use_container_width=True)

# Data Quality - Missing Values
if show_data_quality:
    st.header("Data Quality Analysis")
    missing_values = df1.isnull().sum()
    
    # Enhancing the bar chart for missing values with customized colors
    fig_missing = px.bar(missing_values, title="Missing Values in Each Column", color=missing_values,
                         color_continuous_scale=px.colors.sequential.Reds)
    st.plotly_chart(fig_missing, use_container_width=True)

# Distribution Analysis - Categorical Columns
if show_distribution_analysis:
    st.header("Distribution Analysis")
    categorical_col = st.sidebar.selectbox("Select a Categorical Column for Distribution Analysis", columns, key='cat_select')
    value_counts = df1[categorical_col].value_counts()
    
    # Enhancing the bar chart for distribution with customized colors
    fig_value_counts = px.bar(value_counts, title=f"Distribution of {categorical_col}", 
                              color=value_counts, color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig_value_counts, use_container_width=True)
