import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.decomposition import PCA
from tkinter import ttk


class DataPreprocessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Preprocessing Automation using Python GUI")
        self.root.geometry("900x550")
        self.root.configure(bg='grey')
        self.root.iconbitmap(r"C:\Users\rauna\Downloads\download.ico")
        self.label = tk.Label(root, text="Upload an Excel File", font=("Arial", 12), bg='grey', fg='white')
        self.label.pack(pady=10)
        
        self.button_frame = tk.Frame(root, bg='grey')
        self.button_frame.pack(pady=5)
        
        self.upload_button = tk.Button(self.button_frame, text="Upload File", command=self.upload_file, bg='green', fg='white')
        self.upload_button.grid(row=0, column=0, padx=10)
        
        self.process_button = tk.Button(self.button_frame, text="Process Data", command=self.process_data, state=tk.DISABLED, bg='blue', fg='white')
        self.process_button.grid(row=0, column=1, padx=10)
        
        self.transform_button = tk.Button(self.button_frame, text="Transform Data", command=self.transform_data, state=tk.DISABLED, bg='orange', fg='white')
        self.transform_button.grid(row=0, column=2, padx=10)
        
        self.reduce_button = tk.Button(self.button_frame, text="Reduce Data", command=self.reduce_data, state=tk.DISABLED, bg='brown', fg='white')
        self.reduce_button.grid(row=0, column=3, padx=10)
        
        self.download_button = tk.Button(self.button_frame, text="Download Processed File", command=self.download_processed_file, state=tk.DISABLED, bg='green', fg='white')
        self.download_button.grid(row=0, column=4, padx=10)
        
        self.outlier_button = tk.Button(self.button_frame, text="Remove Outliers", command=self.remove_outliers, state=tk.DISABLED, bg='red', fg='white')
        self.outlier_button.grid(row=0, column=5, padx=10)
        
        self.scatter_button = tk.Button(self.button_frame, text="Scatter Plot", command=self.scatter_plot, state=tk.DISABLED, bg='purple', fg='white')
        self.scatter_button.grid(row=0, column=6, padx=10)
        
        
        #View Data

        self.view_button = tk.Button(self.button_frame, text="View Data", command=self.view_data, state=tk.DISABLED, bg='purple', fg='white')
        self.view_button.grid(row=0, column=7, padx=10)
        
        
        self.filepath = ""
        self.processed_data = None

        # Developer and Software Info
        self.dev_info = tk.Label(root, text="Developed by: Raunak Kumar", font=("Arial", 10, "bold"), bg='grey', fg='white')
        self.dev_info.pack(pady=5)
        
        self.institute_info = tk.Label(root, text="LNCTU, DEPARTMENT BCA(AIDA)", font=("Arial", 10, "bold"), bg='grey', fg='white')
        self.institute_info.pack(pady=5)
        
        self.email_info = tk.Label(root, text="Contact: rk331159@gmail.com", font=("Arial", 10, "bold"), bg='grey', fg='white')
        self.email_info.pack(pady=5)
        
        self.usage_info = tk.Label(root, text="This software automates data preprocessing, including handling missing values, removing duplicates, outlier detection, transformation, reduction, and visualization.", wraplength=700, font=("Arial", 9), bg='grey', fg='white')
        self.usage_info.pack(pady=5)
        self.email_info = tk.Label(root, text="Note : Reduce Data Service is Not Working ", font=("Arial", 12, "bold"), bg='Black', fg='Red')
        self.email_info.pack(pady=5)
        
        self.tree_frame = ttk.Frame(root)  # Remove bg='grey'
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)



    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.filepath = file_path
            self.label.config(text=f"File Loaded: {file_path.split('/')[-1]}")
            self.process_button.config(state=tk.NORMAL)
    def view_data(self):
        if self.processed_data is not None:
            for widget in self.tree_frame.winfo_children():
                widget.destroy()
            
            self.tree = ttk.Treeview(self.tree_frame)
            self.tree.pack(fill=tk.BOTH, expand=True)
            
            self.tree['columns'] = list(self.processed_data.columns)
            self.tree.column("#0", width=0, stretch=tk.NO)
            
            for col in self.processed_data.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor=tk.CENTER, width=100)
            
            for _, row in self.processed_data.iterrows():
                self.tree.insert("", tk.END, values=list(row))
        else:
            messagebox.showwarning("Warning", "No data to display.") 
    def process_data(self):
        try:
            df = pd.read_excel(self.filepath)
            
            # Automatic data preprocessing
            df.drop_duplicates(inplace=True)
            df.fillna(method='ffill', inplace=True)
            
            self.processed_data = df
            self.download_button.config(state=tk.NORMAL)
            self.outlier_button.config(state=tk.NORMAL)
            self.scatter_button.config(state=tk.NORMAL)
            self.transform_button.config(state=tk.NORMAL)
            
            self.view_button.config(state=tk.NORMAL)
            messagebox.showinfo("Success", "Data processing complete!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def transform_data(self):
        if self.processed_data is not None:
            df = self.processed_data.copy()
            
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                scaler = StandardScaler()
                df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
                
            self.processed_data = df
            messagebox.showinfo("Success", "Data transformation complete!")
    
    def reduce_data(self):
        if self.processed_data is not None:
            df = self.processed_data.copy()
            
            numeric_cols = df.select_dtypes(include=['number']).columns
            df = df.loc[:, df.var() > 0.01]  
            
            if len(numeric_cols) > 2:
                pca = PCA(n_components=2)
                reduced_data = pca.fit_transform(df[numeric_cols])
                df_pca = pd.DataFrame(reduced_data, columns=['PC1', 'PC2'])
                df = pd.concat([df_pca, df.drop(columns=numeric_cols, errors='ignore')], axis=1)
            
            self.processed_data = df
            messagebox.showinfo("Success", "Data reduction complete!")
    
    def remove_outliers(self):
        if self.processed_data is not None:
            df = self.processed_data.copy()
            numeric_cols = df.select_dtypes(include=['number']).columns
            
            for col in numeric_cols:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
            
            self.processed_data = df
            messagebox.showinfo("Success", "Outliers removed!")
        if len(numeric_cols) > 0:
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=df[numeric_cols])
            plt.title("Box Plot after Outlier Removal")
            plt.xticks(rotation=45)
            plt.show()
    
    def scatter_plot(self):
        if self.processed_data is not None:
            df = self.processed_data.copy()
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) >= 2:
                plt.figure(figsize=(8, 6))
                sns.scatterplot(x=df[numeric_cols[0]], y=df[numeric_cols[1]])
                plt.title("Scatter Plot")
                plt.xlabel(numeric_cols[0])
                plt.ylabel(numeric_cols[1])
                plt.show()
            else:
                messagebox.showwarning("Warning", "Not enough numeric columns for scatter plot.")
    
    def download_processed_file(self):
        if self.processed_data is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if save_path:
                self.processed_data.to_excel(save_path, index=False)
                messagebox.showinfo("Success", "File downloaded successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataPreprocessorApp(root)
    root.mainloop()
