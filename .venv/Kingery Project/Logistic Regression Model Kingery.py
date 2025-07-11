import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib
matplotlib.use('TkAgg')  # Ensure matplotlib works with tkinter
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import joblib
from imblearn.over_sampling import SMOTE

# Function to load and process data
def load_data(file_path):
    """
    Load data from a CSV file.
    Expected format: 3 quantitative + 7 one-hot encoded features, target (win/loss)
    """
    try:
        data = pd.read_csv(file_path)
        data = data.dropna()  # Remove rows with missing values
        X = data.iloc[:, :-1]  # All columns except the last one
        y = data.iloc[:, -1]   # Last column (1 for win, 0 for loss)
        print("Class Distribution (before SMOTE):")
        print(y.value_counts())
        return X, y
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Please check the path.")
        exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        exit(1)

# Function to train the model
def train_model(X, y):
    """
    Train a Random Forest model with SMOTE and class balancing
    """
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale quantitative features (first 3 columns)
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled.iloc[:, :3] = scaler.fit_transform(X_train.iloc[:, :3])
    X_test_scaled.iloc[:, :3] = scaler.transform(X_test.iloc[:, :3])
    
    # Apply SMOTE to balance classes
    try:
        smote = SMOTE(random_state=42, k_neighbors=3)
        X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)
        print("Class Distribution (after SMOTE):")
        print(pd.Series(y_train_smote).value_counts())
    except ValueError as e:
        print(f"SMOTE failed: {e}. Proceeding without SMOTE.")
        X_train_smote, y_train_smote = X_train_scaled, y_train
    
    # Train Random Forest
    model = RandomForestClassifier(random_state=42, n_estimators=100, class_weight='balanced', max_depth=5)
    model.fit(X_train_smote, y_train_smote)
    
    # Evaluate on test set
    y_pred = model.predict(X_test_scaled)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Feature importance
    print("\nFeature Importances:")
    feature_names = X.columns if hasattr(X, 'columns') else [f"Feature_{i+1}" for i in range(X.shape[1])]
    for name, importance in zip(feature_names, model.feature_importances_):
        print(f"{name}: {importance:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_smote, y_train_smote, cv=5, scoring='f1_macro')
    print("\nCross-Validation F1 Scores:", cv_scores)
    print("Mean F1 Score:", cv_scores.mean())
    
    # Save model and scaler
    joblib.dump(model, 'random_forest_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    
    return model, scaler, X_test_scaled, y_test

# Function to make predictions
def predict_probability(model, scaler, features):
    """
    Predict win probability for given features
    features: list of 3 quantitative + 7 one-hot encoded values
    """
    features_array = np.array(features).reshape(1, -1)
    features_array[:, :3] = scaler.transform(features_array[:, :3])
    win_probability = model.predict_proba(features_array)[0, 1] * 100
    return win_probability

# Function to create GUI for predictions
def create_prediction_gui(model, scaler):
    """
    Create GUI for entering features and displaying predictions
    """
    root = tk.Tk()
    root.title("Win Probability Predictor")
    root.geometry("600x500")
    
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(pady=20)
    
    # Feature names (update to match your dataset)
    feature_names = ["Feature1", "Feature2", "Feature3", "Cat1", "Cat2", "Cat3", "Cat4", "Cat5", "Cat6", "Cat7"]
    
    # Quantitative features
    tk.Label(frame, text="Quantitative Features:", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
    quant_entries = []
    for i in range(3):
        tk.Label(frame, text=f"{feature_names[i]}:").grid(row=i+1, column=0, sticky='w', pady=2)
        entry = tk.Entry(frame, width=10)
        entry.grid(row=i+1, column=1, pady=2)
        quant_entries.append(entry)
    
    # Categorical features
    tk.Label(frame, text="One-Hot Encoded Features (0 or 1):", font=('Arial', 12, 'bold')).grid(row=4, column=0, sticky='w', pady=5)
    cat_entries = []
    for i in range(7):
        tk.Label(frame, text=f"{feature_names[i+3]}:").grid(row=i+5, column=0, sticky='w', pady=2)
        entry = tk.Entry(frame, width=10)
        entry.insert(0, "0")  # Default to 0
        entry.grid(row=i+5, column=1, pady=2)
        cat_entries.append(entry)
    
    def get_prediction():
        try:
            quant_values = [float(entry.get()) for entry in quant_entries]
            cat_values = [int(entry.get()) for entry in cat_entries]
            if not all(v in [0, 1] for v in cat_values):
                raise ValueError("Categorical features must be 0 or 1.")
            all_features = quant_values + cat_values
            probability = predict_probability(model, scaler, all_features)
            messagebox.showinfo("Prediction Result", f"Win Probability: {probability:.2f}%")
            create_probability_chart(probability)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
    
    predict_button = tk.Button(root, text="Predict Win Probability", command=get_prediction,
                             bg="#4CAF50", fg="white", font=('Arial', 12), padx=10, pady=5)
    predict_button.pack(pady=20)
    
    root.mainloop()

# Function to create a probability chart
def create_probability_chart(probability):
    """
    Display a bar chart of the win probability
    """
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.barh(["Win Probability"], [probability], color='green', height=0.5)
    ax.barh(["Win Probability"], [100-probability], left=[probability], color='red', height=0.5)
    ax.text(probability/2, 0, f"{probability:.1f}%", ha='center', va='center', color='white', fontweight='bold')
    ax.text(probability + (100-probability)/2, 0, f"{100-probability:.1f}%", ha='center', va='center', color='white', fontweight='bold')
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel("Probability (%)")
    ax.set_yticks([])
    ax.set_title("Win Probability", fontsize=14)
    plt.tight_layout()
    plt.show(block=False)  # Non-blocking for GUI responsiveness

# Main function
def main():
    # Prompt for CSV file path
    data_path = input("Enter path to your CSV file (default: Just_One_Hot_Encoded_Data.csv): ") or "Just_One_Hot_Encoded_Data.csv"
    
    # Check for existing model
    try:
        model = joblib.load('random_forest_model.pkl')
        scaler = joblib.load('scaler.pkl')
        print("Loaded existing model.")
        retrain = input("Retrain model? (y/n): ").lower()
        if retrain == 'y':
            raise FileNotFoundError  # Force retraining
    except:
        print("No existing model found or retraining requested. Training new model...")
        X, y = load_data(data_path)
        model, scaler, X_test, y_test = train_model(X, y)
        print("Model training complete.")
    
    # Launch GUI
    create_prediction_gui(model, scaler)

if __name__ == "__main__":
    main()