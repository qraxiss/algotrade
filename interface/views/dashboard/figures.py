from dash import dash_table

def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        # sort_action="native",
        # sort_mode="native",
        # page_size=300,
    )
    return table