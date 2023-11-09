import snowflake.connector
import pandas as pd
import vizro.plotly.express as px
from vizro import Vizro
import vizro.models as vm

# Connect to Snowflake
conn = snowflake.connector.connect(
    user='YOUR_SNOWFLAKE_USERNAME',
    password='YOUR_SNOWFLAKE_PASSWORD',
    account='YOUR_SNOWFLAKE_ACCOUNT',
    warehouse='YOUR_WAREHOUSE',
    database='YOUR_DATABASE',
    schema='YOUR_SCHEMA'
)

# Execute a query
query = "SELECT * FROM YOUR_TABLE"
cur = conn.cursor()
cur.execute(query)
rows = cur.fetchall()

# Load query results into a pandas DataFrame
df = pd.DataFrame(rows, columns=[x[0] for x in cur.description])

# Close the cursor and connection
cur.close()
conn.close()

# Now you can use df with Vizro as before
page = vm.Page(
    title="My first dashboard",
    components=[
        vm.Graph(id="scatter_chart", figure=px.scatter(df, x="COLUMN_NAME_X", y="COLUMN_NAME_Y", color="COLUMN_NAME_COLOR")),
        vm.Graph(id="hist_chart", figure=px.histogram(df, x="COLUMN_NAME_X", color="COLUMN_NAME_COLOR")),
    ],
    controls=[
        vm.Filter(column="COLUMN_NAME_FILTER"),
    ],
)

dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run()
