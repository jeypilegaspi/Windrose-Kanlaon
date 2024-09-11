# Windrose-Kanlaon

This repository contains the python script for windrose generator created specifically for Kanlaon wind data along wind the json files that contains the wind data.
The executable (EXE) file is downloadable on https://drive.google.com/file/d/1JUwU2cA8iPE1G_01fiEg4VJzdbaDBxyL/view?usp=drive_link

Please send a message to 09302455701 upon discovery of a bug or if you have any suggestions.

When running the python scripts, some prerequisites must be installed on the system first:
 - Python 3.12
 - Jupyter Notebook (download through Anaconda Installer) or Google Colab(https://colab.research.google.com/)
 - matplotlib(download via command prompt/anaconda prompt by running ```pip install matplotlib```)
 - numpy(download via command prompt/anaconda prompt by running ```pip install numpy```)

Tutorials on how to setup Jupyter Notebook on Anaconda virtual environment and installing packages is widely available online.

When using the GUI, just run the executable file provided by the link above. When a windows defender prompted a warning, click `more info` and select `run anyway`.

## **Windrose Plot Generator - Instruction Guide**

### **Input Data Format**
The data for the windrose plot comes from a **JSON file**. This file must adhere to a specific structure to ensure correct parsing and plotting. The JSON structure should look like this:

```json
{
  "windrose": [
    {
      "date": "Month DD, YYYY",
      "time": "HH:MM AM/PM (PST)",
      "data": [
        {
          "z_hPa": value,
          "speed_kph": value,
          "direction": "N/E/S/W/etc"
        },
        {
          "z_hPa": value,
          "speed_kph": value,
          "direction": "N/E/S/W/etc"
        },
        // ... repeat for up to 5 wind speed measurements
      ]
    },
    //... repeat for multiple date and time entries
  ]
}
```
- **`date`**: The date when the measurements were taken.
- **`time`**: The time of the day when the measurements were taken.
- **`speed_kph`**: The wind speed in kilometers per hour (kph).
- **`direction`**: The compass direction of the wind, e.g., `"N"`, `"NE"`, `"E"`, etc.

The json file can be created through any text editor by setting its file extension as '.json'.

### **Plotting Process**

#### **1. Data Parsing**
The program first reads the JSON file and extracts the following data for each entry:
- **Date and Time**: The date and time of the wind measurement.
- **Wind Speed and Direction**: A list of wind speeds (in kilometers per hour) and corresponding directions (e.g., N, NE, E, etc.).

#### **2. Polar Coordinate System**
The windrose plot uses a **polar coordinate system**, where:
- **Angle (Theta)**: Represents the wind direction (North, East, South, West, and intermediate directions). The angle is computed in radians. 
  - For example: 
    - North (N) corresponds to 90 degrees or π/2 radians.
    - East (E) corresponds to 0 degrees or 0 radians.
    - South (S) corresponds to 270 degrees or 3π/2 radians.
- **Radius (R)**: Represents the wind speed, measured radially outward from the center of the plot. Higher speeds extend further from the center, while lower speeds stay close to the center.

#### **3. Wind Direction Mapping**
The code maps the wind directions into corresponding angles on the polar plot:
- The main directions (e.g., N, E, S, W) and intermediate directions (e.g., NE, NW) are converted into angles based on their position on the compass. For instance:
  - East (E): `0` radians
  - North (N): `π/2` radians
  - West (W): `π` radians
  - South (S): `3π/2` radians
  - Intermediate directions like `NE` are calculated as fractional angles (e.g., NE = `π/4` radians).

This mapping allows the wind direction to be properly placed around the circular plot.

#### **4. Wind Speed as Radial Distance**
Each wind speed value is placed on the corresponding radial axis, with higher wind speeds placed farther from the center and lower speeds placed closer.

#### **5. Plotting the Windrose**
The core of the windrose plot is created using **Matplotlib**:
- **Bars**: The wind speeds are represented by **colored bars** extending radially. Each bar corresponds to a wind direction and its length corresponds to the wind speed.
- **Colors**: Different colors are used to distinguish between the different wind speed measurements.
- **Width of Bars**: Each bar has a constant angular width, dividing the polar plot into equal sections for each direction.

#### **6. Adding a Legend**
A legend is created to indicate which bar corresponds to which height or radial label, such as:
- `~1.5km`
- `~3km`
- `~5-6km`
- `~9km`
- `~12km`

This gives an understanding of the altitude or vertical level at which the wind data was collected.

#### **7. Displaying the Plot**
After plotting, the windrose is displayed with:
- **Directional Labels**: Labels around the circular plot, such as N, NE, E, SE, S, etc., showing the wind direction.
- **Title**: The date and time of the wind measurement, displayed at the top of the plot.

### **Example Windrose Plot**
- **Data Example**: Suppose the wind data is recorded at 5 altitudes (~1.5km, ~3km, ~5-6km, ~9km, ~12km) with wind speeds recorded at 5 directions (N, NE, E, SE, S).
- **Visual Output**: The windrose will show a circular plot with bars extending at angles corresponding to the directions. Bars will be colored and proportional to wind speeds.

### **Use Cases**
- **Tephra Deposite Analysis**: Understanding the impact of wind in distribution of volcanic ash and other volcanic materials ejected during an eruption..
