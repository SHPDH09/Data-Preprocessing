import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error

class DataPreprocessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Preprocessing Automation using Python GUI")
        self.root.geometry("900x550")
        self.root.configure(bg='grey')

        self.label = tk.Label(root, text="Upload an Excel File", font=("Arial", 12), bg='grey', fg='white')
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(root, bg='grey')
        self.button_frame.pack(pady=5)
        
        self.upload_button = tk.Button(self.button_frame, text="Upload File", command=self.upload_file, bg='green', fg='white')
        self.upload_button.grid(row=0, column=0, padx=10)
        
        self.process_button = tk.Button(self.button_frame, text="Process Data", command=self.process_data, state=tk.DISABLED, bg='blue', fg='white')
        self.process_button.grid(row=0, column=1, padx=10)
        
        self.view_button = tk.Button(self.button_frame, text="View Data", command=self.view_data, state=tk.DISABLED, bg='purple', fg='white')
        self.view_button.grid(row=0, column=2, padx=10)

        # Dropdown for target variable selection
        self.target_var_label = tk.Label(root, text="Select Target Variable:", font=("Arial", 10), bg='grey', fg='white')
        self.target_var_label.pack()
        self.target_var_combo = ttk.Combobox(root, state="readonly")
        self.target_var_combo.pack()
        
        self.train_model_button = tk.Button(root, text="Train Model", command=self.train_model, state=tk.DISABLED, bg='orange', fg='white')
        self.train_model_button.pack(pady=5)

        # NEW PREDICT BUTTON
        self.predict_button = tk.Button(root, text="Predict", command=self.predict_data, state=tk.DISABLED, bg='red', fg='white')
        self.predict_button.pack(pady=5)

        self.filepath = ""
        self.processed_data = None
        self.model = None  # Initialize model variable

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.filepath = file_path
            self.label.config(text=f"File Loaded: {file_path.split('/')[-1]}")
            self.process_button.config(state=tk.NORMAL)
            self.view_button.config(state=tk.NORMAL)

    def view_data(self):
        df = pd.read_excel(self.filepath)
        self.processed_data = df
        messagebox.showinfo("Info", "Data loaded successfully!")

    def process_data(self):
        df = pd.read_excel(self.filepath)
        df.drop_duplicates(inplace=True)
        df.fillna(method='ffill', inplace=True)
        
        self.processed_data = df
        self.train_model_button.config(state=tk.NORMAL)
        messagebox.showinfo("Success", "Data processing complete!")

        # Populate the dropdown with column names
        self.target_var_combo['values'] = self.processed_data.columns
        self.target_var_combo.current(0)

    def train_model(self):
        if self.processed_data is not None:
            target_variable = self.target_var_combo.get()
            X = self.processed_data.drop(columns=[target_variable])
            y = self.processed_data[target_variable]
            
            # Encode categorical variables
            X = pd.get_dummies(X, drop_first=True)
            if y.dtype == 'object':
                y = LabelEncoder().fit_transform(y)
                self.model = RandomForestClassifier()
            else:
                self.model = RandomForestRegressor()
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model.fit(X_train, y_train)
            y_pred = self.model.predict(X_test)
            
            if isinstance(self.model, RandomForestClassifier):
                acc = accuracy_score(y_test, y_pred)
                messagebox.showinfo("Model Trained", f"Classification Accuracy: {acc:.2f}")
            else:
                mse = mean_squared_error(y_test, y_pred)
                messagebox.showinfo("Model Trained", f"Regression MSE: {mse:.2f}")

            # Enable predict button
            self.predict_button.config(state=tk.NORMAL)

    def predict_data(self):
        if self.model is not None:
            input_data = simpledialog.askstring("Input", "Enter values separated by commas")
            if input_data:
                try:
                    input_list = [float(x) for x in input_data.split(",")]
                    prediction = self.model.predict([input_list])
                    messagebox.showinfo("Prediction Result", f"Predicted Value: {prediction[0]}")
                except ValueError:
                    messagebox.showerror("Error", "Invalid input format. Please enter numeric values.")
        else:
            messagebox.showerror("Error", "Train the model first!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataPreprocessorApp(root)
    root.mainloop()
