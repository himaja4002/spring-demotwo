import streamlit as st
import dask.dataframe as dd
import pandas as pd
import json
import base64
from io import StringIO
from streamlit_option_menu import option_menu
import plotly.express as px

# Streamlit Configuration for Dark Theme
st.set_page_config(
    page_title="Audience Builder",
    layout="wide",
    # initial_sidebar_state="expanded"
)

CUSTOM_STYLE = """
<style>
    body {
        color: #2C3E50;
        background-color: #ECF0F1;
    }
    .reportview-container .main .block-container {
        padding: 2rem;
        max-width: 1200px;
    }
    h1, h2, h3 {
        font-weight: bold;
    }
    h1 {
        text-align: center;
        font-size: 2em;
        margin-bottom: 1em;
        color: #AB3E2E;
    }
    .sidebar .sidebar-content {
        background-color: #F7F7F7;
        padding: 10px 20px;
    }
    button {
        background-color: #2980B9;
        color: white;
    }
    button:hover {
        background-color: #247BA0;
    }
</style>
"""

st.markdown(CUSTOM_STYLE, unsafe_allow_html=True)

# Title
st.markdown("<h1>Audience Builder</h1>", unsafe_allow_html=True)

# Title

# Load Data
@st.cache_data(persist=True)
def load_data():
    try:
        data = dd.read_csv('bike_sharing_dc.csv')
        return data
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return dd.from_pandas(pd.DataFrame(), npartitions=1)

# Initializations
data = load_data()
record_count = len(data)

# Function to load configurations from a file
def load_configs_from_file() -> dict:
    try:
        with open('configs.json', 'r') as f:
            content = f.read()
            if not content.strip():  # Check if the file is empty or contains only whitespace
                return {}
            return json.loads(content)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}


st.session_state.configs = load_configs_from_file()

if 'filter_action' not in st.session_state:
    st.session_state.filter_action = False

if 'filters' not in st.session_state:
    st.session_state.filters = []

if 'filter_added' not in st.session_state:
    st.session_state.filter_added = False


filtered_data = data
record_count = len(filtered_data)

def detect_column_type(column: str) -> str:
    dtype_str = str(data[column].dtype)
    if dtype_str in ["float64", "int64"]:
        return 'numeric'
    elif dtype_str == 'datetime64[ns]':
        return 'date'
    elif dtype_str == "object" or "string" in dtype_str:   # check for both pandas and pyarrow string types
        return 'text'
    return 'other'

def apply_filters(df, filters):
    for logic, col, op, val in filters:
        condition = None

        if isinstance(df, dd.DataFrame):
            df = df.compute()


        # Define the conditions based on operation
        if op == 'equals':
            if isinstance(val, list):  # for multi-selection
                condition = df[col].isin(val)
            else:
                condition = df[col] == val
        elif op == 'contains':
            if isinstance(val, list):
                condition = df[col].str.contains('|'.join(val), na=False)  # match any of the values
            else:
                condition = df[col].str.contains(val, na=False)
        elif op == 'greater than':
            if isinstance(val, tuple):  # Check if it's a range
                condition = (df[col] > val[0]) & (df[col] < val[1])  # In this case, apply both limits
            else:
                condition = df[col] > val
        elif op == 'less than':
            condition = df[col] < val
        elif op == 'between':
            condition = (df[col] >= val[0]) & (df[col] <= val[1])
        else:
            continue

        # Apply the conditions based on logic
        if logic == "AND":
            df = df[condition]
        elif logic == "OR":
            df = pd.concat([df, df[condition]]).drop_duplicates()
        elif logic == "NOT":
            df = df[~condition]

    return df

import json

def filters_to_json(filters: list) -> str:
    """Convert the filters list to the desired JSON representation."""
    structured_filters = []
    for filter in filters:
        logic, col, op, val = filter

        # Translate the operators to the desired rule type
        if op == 'equals' or op == 'contains':
            rule_type = "one of"
            rule_value = val if isinstance(val, list) else [val]
        elif op == 'greater than':
            rule_type = "greater than"
            rule_value = val
        elif op == 'less than':
            rule_type = "less than"
            rule_value = val
        elif op == 'between':
            rule_type = "between"
            rule_value = val
        else:
            continue

        structured_filters.append({
            "name": col,
            "rule": {
                "type": rule_type,
                "value": rule_value
            }
        })

    return json.dumps(structured_filters, indent=4)

def save_filters_to_file(filters: list):
    json_content = filters_to_json(filters)
    with open('filters.json', 'w') as f:
        f.write(json_content)

def get_value_input(col: str, col_type: str, default_val=None, op=None):
    if col_type == "text":
        unique_vals = list(data[col].dropna().unique())
        return st.multiselect("Value", options=unique_vals, default=default_val if default_val else [])
        # unique_vals = list(data[col].dropna().unique())
        # # unique_vals = data[col].dropna().unique().to_list()
        # return st.selectbox("Value", options=unique_vals, index=unique_vals.index(default_val) if default_val else 0)
    
    elif col_type == "numeric":
        min_val, max_val = data[col].min().compute(), data[col].max().compute()  # Compute the min and max values here
        if op == "between":  # Only use the slider for the between operator
        
            if default_val and isinstance(default_val, (tuple, list)) and len(default_val) == 2:
                start, end = default_val
            else:
                start, end = (min_val, max_val)

            val = st.slider("Value Range", min_value=min_val, max_value=max_val, value=(start, end))
            return val
        else:
            # For other numeric operations, return a number input
            return st.number_input("Value", value=default_val if default_val else min_val, min_value=min_val, max_value=max_val)
    
    elif col_type == "date":
        min_date, max_date = data[col].min(), data[col].max()
        start, end = default_val if default_val else (min_date, max_date)
        return st.date_input("Date Range", (start, end))
    
    else:
        return st.text_input("Value", value=default_val if default_val else '')

column_types = {col: detect_column_type(col) for col in data.columns}
CONFIGURATION_TYPES = ["Checking", "Saving", "Config3", "Config4", "Common"]

# Session state initialization
session_keys = ['filter_action', 'filters', 'filter_added', 'configs']
for key in session_keys:
    if key not in st.session_state:
        if key == "filters":
            st.session_state[key] = []
        elif key == "configs":
            st.session_state[key] = {}
        else:
            st.session_state[key] = {}
# Session state initialization
if 'configs' not in st.session_state:
    st.session_state.configs = load_configs_from_file()

# Function to save configurations to a file
def save_configs_to_file(configs: dict):
    json_content = json.dumps(configs, indent=4)
    with open('configs.json', 'w') as f:
        f.write(json_content)


def save_template(template_name, rules):
    """Save the template to a json file."""
    configs = load_configs_from_file()
    configs[template_name] = rules
    with open('configs.json', 'w') as f:
        json.dump(configs, f)

def delete_template(template_name):
    """Delete the template from the json file."""
    configs = load_configs_from_file()
    if template_name in configs:
        del configs[template_name]
        with open('configs.json', 'w') as f:
            json.dump(configs, f)


# with st.sidebar:
selected = option_menu(
    menu_title=" ",  # required
    options=["Template Management", "Audience Generation", "Interactive Modern Visualizations"],
    default_index=0,  # optional
    menu_icon="cast",  # optional
    orientation="horizontal", 
    styles={
        'container': {'padding': '0!important', 'background-color': '#fafafa'},
        'icon': {'color': 'orange', 'font-size': '20px'},
        'nav-link': {
            'font-size': '16px',
            'text-align': 'left',
            'margin': '0px',
            'hover-color': '#eee',
            'nav-link-selected': {'background-color': '#123958'},
        },
    }
)

if selected == "Template Management":
    st.markdown("<h2>Template Management</h2>", unsafe_allow_html=True)
    tm = option_menu(
        menu_title=" ",  
        options=["Create Template", "Load Template", "Delete Template"],
        default_index=0, 
        menu_icon="cast", 
        orientation="horizontal", 
        styles={
            'container': {
                'padding': '0!important',
                'background-color': '#fafafa',
                'width': '50%',  # setting width to 50%
                'margin-left': 'auto',  # centering the container
                'margin-right': 'auto',
                'padding-left': '20px'  # indenting child options
            },
            'icon': {'color': 'orange', 'font-size': '18px'},  # slightly reduced font size
            'nav-link': {
                'font-size': '14px',  # reduced font size
                'text-align': 'left',
                'margin': '0px',
                'hover-color': '#eee',
                'nav-link-selected': {'background-color': '#123958'},
            },
        }
    )
    if tm == "Create Template":
        col1, col2 = st.columns((1,2))
        with col1:
            selected_configuration_type = st.selectbox("Choose Configuration Type (Parent)", options=["-"] + CONFIGURATION_TYPES)

            with st.expander("Add New Filter"):
                col = st.selectbox("Column", options=list(data.columns))
                col_type = column_types[col]

    # Find if a filter for this column already exists
                existing_filter_for_column = next((item for item in st.session_state.filters if item[1] == col), None)
                default_value = existing_filter_for_column[3] if existing_filter_for_column else None

                ops = {
                    'numeric': ['equals', 'less than', 'greater than', 'between'],
                    'date': ['equals','between'],
                    'text': ['equals', 'contains'],
                    'other': ['equals']
                }

                op = st.selectbox("Operator", options=ops.get(col_type, ['equals']))
                val = get_value_input(col, col_type, default_value, op=op)
                logic = "AND"
                if len(st.session_state.filters) > 0:
                    logic = st.selectbox("Logic", ["AND", "OR", "NOT"])
    
            if st.button('Add Filter'):
                st.session_state.filters.append((logic, col, op, val))
                df = data.compute()
                filtered_data = apply_filters(df, st.session_state.filters)
                record_count = len(filtered_data)  
                st.success(f"Number of records: {record_count}")
                st.experimental_rerun()

        with col2:
            if selected_configuration_type != "-":

                st.write("### Configuration: ", selected_configuration_type)  # Give a title for clarity

                rules = {}
  
                initial_count = len(data)
                for i, (logic, col, op, val) in enumerate(st.session_state.filters):
                    if i == 0:
                        filter_str = f"{col} {op} {val}"  # The first filter shouldn't have a logic operator at the beginning
                    else:
                        filter_str = f"{logic} {col} {op} {val}"  # Subsequent filters should start with the logic operator

                # Break the display into columns
                    col1, col2, col3, col4 = st.columns(4)
        
                # Control buttons for moving filters up and down
                    if i != 0:  # The first filter shouldn't have the move up button
                        if col1.button(f"⬆️", key=f"move_up_{i}"):
                            st.session_state.filters[i], st.session_state.filters[i-1] = st.session_state.filters[i-1], st.session_state.filters[i]
                            st.experimental_rerun()
                    if i != len(st.session_state.filters) - 1:  # The last filter shouldn't have the move down button
                        if col2.button(f"⬇️", key=f"move_down_{i}"):
                            st.session_state.filters[i], st.session_state.filters[i+1] = st.session_state.filters[i+1], st.session_state.filters[i]
                            st.experimental_rerun()
     
                    df_temp = apply_filters(data.compute(), [st.session_state.filters[i]])
                    filtered_count = len(df_temp)
                    records_dropped = initial_count - filtered_count

                    col3.write(f"{filter_str} ⬇️ {records_dropped}")

                    initial_count = filtered_count  # Update the count for the next filter


                    # Display the filter
                    # col3.write(filter_str)

            # Delete button for removing the filter
                    if col4.button(f"❌", key=f"delete_{i}"):
                        st.session_state.filters.pop(i)
                        st.experimental_rerun()

            new_template_name = st.text_input("Enter template name:")
        # save_template(template_name, rules)
            if st.button("Save Template") and new_template_name:
                if selected_configuration_type not in st.session_state.configs:
                    st.session_state.configs[selected_configuration_type] = {}
            
                if new_template_name in st.session_state.configs[selected_configuration_type]:
                    st.warning(f"Template {new_template_name} already exists under {selected_configuration_type}. If you want to overwrite it, delete the existing one first.")
                else:
                    st.session_state.configs[selected_configuration_type][new_template_name] = st.session_state.filters
                    save_configs_to_file(st.session_state.configs)
                    st.success(f"Saved filters as {new_template_name} under {selected_configuration_type}!")

            elif tm == "Load Template":
                template_names = list(load_configs_from_file().keys())
                selected_template = st.selectbox("Choose a template to load:", template_names)
                rules = load_configs_from_file().get(selected_template, {})
                for key, value in rules.items():
                    st.write(f"{key}: {value}")
            elif tm == "Delete Template":
                template_names = list(load_configs_from_file().keys())
                selected_template = st.selectbox("Choose a template to delete:", template_names)
                if st.button("Delete"):
                    delete_template(selected_template)
                    st.success(f"Template {selected_template} deleted successfully!")

    
CONFIGURATION_TYPES = ["Checking", "Saving", "Config3", "Config4", "Common"]

# Load configurations when the application starts
# st.session.state.configs = load_configs_from_file()
