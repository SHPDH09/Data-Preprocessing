# Data Preprocessing Automation

## Overview
Data Preprocessing Automation is a Python-based GUI application designed to streamline the data preprocessing workflow. This tool allows users to upload an Excel file, process the data automatically, remove outliers, visualize data using boxplots and scatter plots, and download the cleaned dataset.

## Features
- **Upload Excel Files**: Load data seamlessly from an Excel file.
- **Automated Data Preprocessing**: Removes duplicates, fills missing values, and cleans data.
- **Outlier Removal**: Identifies and removes outliers using the IQR method.
- **Data Visualization**:
  - **Boxplot**: Displays data distribution and detects anomalies.
  - **Scatter Plot**: Shows relationships between numerical variables.
- **Processed Data Download**: Save the cleaned data in Excel format.
- **Custom Branding**: Includes a custom application logo instead of the default Tkinter icon.

## Technologies Used
- **Python**
- **Tkinter** (GUI framework)
- **Pandas** (Data manipulation)
- **Matplotlib & Seaborn** (Data visualization)

## Installation
### Prerequisites
Ensure you have Python installed on your system. You can install the required dependencies using:
```bash
pip install pandas matplotlib seaborn openpyxl
```

### Running the Application
Clone the repository and run the script:
```bash
python DataPreprocessing.py
```

### Creating an Executable
To create a standalone application:
```bash
pyinstaller --noconsole --onefile --icon=logo.ico --name DataPreprocessing DataPreprocessing.py
```

## License
This software is released under the [MIT License](LICENSE).

## Contact
For inquiries, reach out via [LinkedIn](your-linkedin-profile).

---
Let me know if you need modifications! 🚀

