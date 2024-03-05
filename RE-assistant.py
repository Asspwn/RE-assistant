import PySimpleGUI as sg
import pandas as pd
# Define custom colors
sg.theme('LightBlue1')  # You can choose any built-in theme or create your own

# Define fonts
font_title = ('Helvetica', 16, 'bold')
font_label = ('Helvetica', 12)
font_input = ('Helvetica', 12)

state_data = ['черновая отделка', 'cвежий ремонт',
       'требуется косметический ремонт']
position_data = ['в жилом доме или ЖК', 'отдельностоящее здание',
       'в бизнес-центре', 'в торговом центре']
comm_data = ['вентиляция', 'вода', 'газ', 'канализация', 'отопление', 'свет']
count_data = ['10', '20', '30', '40', '50']

layout = [
    [sg.Text('Город', font=font_label), sg.InputText(key='-CITY-', font=font_input)],
    [sg.Text('Адрес', font=font_label), sg.InputText(key='-ADDRESS-', font=font_input)],
    [sg.Text('Год постройки', font=font_label), sg.InputText(key='-YEAR-', font=font_input)],
    [sg.Text('Высота потолков', font=font_label), sg.InputText(key='-HEIGHT-', font=font_input)],
    [sg.Text('Площадь объекта, м²', font=font_label), sg.InputText(key='-AREA-', font=font_input)],
    [sg.Text('Состояние', font=font_label), sg.OptionMenu(state_data, default_value=state_data[0], key='-CONDITION-')],
    [sg.Text('Размещение объекта', font=font_label), sg.OptionMenu(position_data, default_value=position_data[0], key='-POSITION-')],
    [sg.Text('Коммуникации', font=font_label), sg.Checkbox('вентиляция', key=('-ITEM1-', 'вентиляция')), sg.Checkbox('вода', key=('-ITEM2-', 'вода')), sg.Checkbox('газ', key=('-ITEM3-', 'газ')), sg.Checkbox('канализация', key=('-ITEM4-', 'канализация')),  sg.Checkbox('отопление', key=('-ITEM5-', 'отопление')),  sg.Checkbox('свет', key=('-ITEM6-', 'свет'))],
    [sg.Text('Кол-во обьявлении', font=font_label), sg.OptionMenu(count_data, default_value=count_data[0], key='-COUNT-')],

    [sg.Button('Поиск', font=font_input)]
]

window = sg.Window('Параметры', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == "Поиск":

        city = values['-CITY-'] if values['-CITY-'] else ""
        address = values['-ADDRESS-'] if values['-ADDRESS-'] else ""
        year = values['-YEAR-'] if values['-YEAR-'] else ""
        height = values['-HEIGHT-'] if values['-HEIGHT-'] else ""
        area = values['-AREA-'] if values['-AREA-'] else ""
        condition = values['-CONDITION-'] if values['-CONDITION-'] else ""
        position = values['-POSITION-'] if values['-POSITION-'] else ""
        count = values['-COUNT-'] if values['-COUNT-'] else ""

        comms = [element[1] for element in values if values[element]==True
                       and 'ITEM' in element[0] ]
        comm = ",".join(str(x) for x in comms)
        print(comm)


        output = {}
        output['Город'] = [city]
        output['Адрес'] = [address]
        output['Год постройки'] = [year]
        output['Высота потолков'] = [height]
        output['Площадь объекта, м²'] = [area]
        output['Состояние'] = [condition]
        output['Размещение объекта'] = [position]
        output['Коммуникации'] = [comm]
        output['Кол-во обьявлении'] = [count]

        new_output = pd.DataFrame.from_dict(output)
        

window.close()
data_input = new_output[['Город', 'Адрес', 'Год постройки', 'Высота потолков', 'Площадь объекта, м²', 'Состояние',
                        'Размещение объекта', 'Коммуникации']]

#nq = output['Кол-во обьявлении']

import requests
import pandas as pd

# Assuming your data_inputset is loaded into a data_inputFrame called 'data_input'

# Define the geocoding function
def geocode_address(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = {"address": address, "key": api_key}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        geo_data_input = response.json()
        if geo_data_input["results"]:
            location = geo_data_input["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            return None, None
    else:
        return None, None

# Replace 'YOUR_API_KEY' with your actual Google Maps Geocoding API key
api_key = ''

# Create empty lists to hold the latitude and longitude values
latitudes = []
longitudes = []

# Iterate over each address in the data_inputFrame
for address in data_input["Адрес"]:
    lat, lng = geocode_address(address, api_key)
    latitudes.append(lat)
    longitudes.append(lng)
    print(address)

# Add the latitude and longitude as new columns in the data_inputFrame
data_input["Latitude"] = latitudes
data_input["Longitude"] = longitudes


import pandas as pd

# Load the dataset
file_path = 'data-2.xlsx'
data = pd.read_excel(file_path)

# Display the first few rows of the dataset to understand its structure
#data.head()


import pandas as pd

# Assuming 'data' is your DataFrame
data['Коммуникации'] = data['Коммуникации'].apply(lambda x: ', '.join(sorted(x.split(', '))))

# Sorting the column based on alphabetic order
data['Коммуникации'] = data['Коммуникации'].apply(lambda x: ', '.join(sorted(x.split(', '))))

# Displaying the sorted column
#print(data[['Коммуникации']])


import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the dataset

# Specifying the columns based on the request
specified_columns = [
    "Город", "Адрес", "Состояние", "Год постройки", "Размещение объекта",
    "Высота потолков", "Площадь объекта, м²", "Коммуникации", "Latitude", "Longitude"
]

# Identifying numerical and categorical columns based on the specified list
numerical_cols_specified = ["Год постройки", "Площадь объекта, м²", "Высота потолков", "Latitude", "Longitude"]
categorical_cols_specified = ["Город", "Адрес", "Состояние", "Размещение объекта", "Коммуникации"]

# Defining preprocessing for numerical columns (scale them)
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

# Defining preprocessing for categorical columns (encode them)
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols_specified),
        ('cat', categorical_transformer, categorical_cols_specified)])

# Filtering the dataset to include only the specified columns
data_specified = data[specified_columns]

# Apply preprocessing to the dataset
data_prepared = preprocessor.fit_transform(data_specified)

# Check the shape of the processed data to confirm transformation
print(data_prepared.shape)

# Note: This code prepares the dataset for further analysis or model training. 
# If you intend to use a specific model (e.g., Nearest Neighbors for finding similar cases),
# you would need to initialize and train your model with the `data_prepared` dataset.


from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Initialize the Nearest Neighbors model
nearest_neighbors_model = NearestNeighbors(n_neighbors=int(count), algorithm='auto')

# Fit the model to the prepared data
nearest_neighbors_model.fit(data_prepared)

# Since we need a specific case to query, let's arbitrarily choose one from the dataset for demonstration.
# Normally, you would input the features of a real case you're interested in.
example_case_index = 0  # Using the first case in the dataset as an example
example_case = data_prepared[example_case_index].reshape(1, -1)

# Find the 10 most similar cases
distances, indices = nearest_neighbors_model.kneighbors(example_case)

data_prepared.shape, distances, indices

# Note: This is a high-level overview and may require adjustments to fit into your existing code

# Step 1 & 3: Preprocess the example data (assuming 'data_input' is your example DataFrame)
data_input_prepared = preprocessor.transform(data_input)

# Step 4: Find similar cases using the Nearest Neighbors model
# Assuming 'nearest_neighbors_model' is your fitted model
distances, indices = nearest_neighbors_model.kneighbors(data_input_prepared)

# Step 5: Retrieve similar cases from the broader dataset
# Assuming 'data' is your broader dataset that has been used to fit the model
similar_cases = data.iloc[indices[0]]

# Now, 'similar_cases' contains the rows from your dataset that are most similar to the example case
# You can perform further analysis or operations on 'similar_cases'

from geopy.distance import geodesic

# Assuming 'similar_cases' contains the similar cases found
# and 'data_input' is your example data with latitude and longitude included

# Get the latitude and longitude for the example case
# Assuming the first row of 'data_input' is the example case
example_lat_lng = (data_input.iloc[0]['Latitude'], data_input.iloc[0]['Longitude'])

# Initialize a list to store distances
distances_km = []

# Iterate over similar cases to calculate distances
for index, row in similar_cases.iterrows():
    # Get the latitude and longitude for the current similar case
    case_lat_lng = (row['Latitude'], row['Longitude'])
    
    # Calculate the distance in kilometers and append it to the list
    distance = geodesic(example_lat_lng, case_lat_lng).kilometers
    distances_km.append(distance)

# Add the distances as a new column to the 'similar_cases' DataFrame
similar_cases['Distance from Example (km)'] = distances_km

# Now 'similar_cases' includes distances from the example case



import pandas as pd
from datetime import datetime

# Assuming similar_cases is your DataFrame
# similar_cases = pd.DataFrame(data)

# Generate a timestamp
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

# Create a unique file path
file_path = rf"\output_{timestamp}.xlsx"

# Save the DataFrame to an Excel file with the unique file path
similar_cases.to_excel(file_path)


print(f"RE-assitant found {count} number of similar cases")