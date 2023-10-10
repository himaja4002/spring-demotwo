import plotly.express as px

with st.expander("Data Preview"):
    st.write(filtered_data.head())

st.header("Data Visualization")
columns = df1.columns
x_axis = st.selectbox("Select X Axis", columns)
y_axis = st.selectbox("Select Y Axis", columns)

# Now, using plotly, you can visualize this
fig = px.scatter(df1, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
st.plotly_chart(fig)

# Data Quality - Missing Values
st.header("Data Quality Analysis")

missing_values = df1.isnull().sum()
fig_missing = px.bar(missing_values, title="Missing Values in Each Column")
st.plotly_chart(fig_missing)
# Assuming a categorical column for demonstration
categorical_col = st.selectbox("Select a Categorical Column for Distribution Analysis", columns)
value_counts = df1[categorical_col].value_counts()
fig_value_counts = px.bar(value_counts, title=f"Distribution of {categorical_col}")
st.plotly_chart(fig_value_counts)
