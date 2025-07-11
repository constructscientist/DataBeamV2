import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os

# Install required packages
import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'scikit-learn'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openpyxl'])

# Load and preprocess data
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

print("Starting model training process...")

# Read the Excel file
df = pd.read_excel('linearmodel.xlsx')
print("Data loaded successfully")

# Convert win_chance to binary outcome
df['win'] = (df['win_chance'] > 0.89).astype(int)
print("Win outcome created")

# One-hot encode the 'project_type' column
encoder = OneHotEncoder(sparse_output=False)
type_encoded = encoder.fit_transform(df[['project_type']])
type_cols = encoder.get_feature_names_out(['project_type'])
print("One-hot encoding completed")

# Create encoded dataframe
type_df = pd.DataFrame(type_encoded, columns=type_cols)

# Combine with original data, dropping original project_type column and win_chance
X = pd.concat([df.drop(['project_type', 'win_chance', 'win'], axis=1), type_df], axis=1)
y = df['win']
print("Features prepared")

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split completed")

# Create and train the model
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train, y_train)
print("Model training completed")

# Calculate cross-validation score
cv_scores = cross_val_score(model, X, y, cv=5)
print("\nCross-validation scores:", cv_scores)
print("Average CV score:", cv_scores.mean())

# 2. Make predictions and create confusion matrix
y_pred = model.predict(X_test)
conf_matrix = confusion_matrix(y_test, y_pred)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Predicted Loss', 'Predicted Win'],
            yticklabels=['Actual Loss', 'Actual Win'])
plt.title('Confusion Matrix')
plt.show()

# 3. Detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 4. Feature importance with confidence intervals
def get_feature_importance_ci(model, X, y, n_iterations=1000):
    coefs = []
    for _ in range(n_iterations):
        # Sample with replacement
        indices = np.random.randint(0, len(X), len(X))
        sample_X = X.iloc[indices]
        sample_y = y.iloc[indices]
        # Fit the model and store the coefs
        model.fit(sample_X, sample_y)
        coefs.append(model.coef_[0])
    
    coefs = np.array(coefs)
    return np.percentile(coefs, [2.5, 97.5], axis=0)

# Calculate and display feature importance with confidence intervals
ci_lower, ci_upper = get_feature_importance_ci(model, X, y)
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_[0],
    'CI_Lower': ci_lower,
    'CI_Upper': ci_upper
})

print("\nFeature Importance with 95% Confidence Intervals:")
print(feature_importance.sort_values(by='Coefficient', key=abs, ascending=False))

# 5. Print example predictions
print("\nExample Predictions:")
example_data = X_test.head(5)
predictions = model.predict(example_data)
probabilities = model.predict_proba(example_data)
for i in range(5):
    print(f"\nExample {i+1}:")
    print(f"Predicted outcome: {'Win' if predictions[i] == 1 else 'Loss'}")
    print(f"Probability of winning: {probabilities[i][1]:.2%}")

print("\nNow saving the model and encoder...")

# Save the model
try:
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved successfully!")
except Exception as e:
    print(f"Error saving model: {e}")

# Save the encoder
try:
    with open('encoder.pkl', 'wb') as f:
        pickle.dump(encoder, f)
    print("Encoder saved successfully!")
except Exception as e:
    print(f"Error saving encoder: {e}")

# Verify files were saved
if os.path.exists('model.pkl'):
    print(f"Verified: model.pkl exists! File size: {os.path.getsize('model.pkl')} bytes")
if os.path.exists('encoder.pkl'):
    print(f"Verified: encoder.pkl exists! File size: {os.path.getsize('encoder.pkl')} bytes")

print("\nProcess completed!")

# Try to load the saved model and encoder
try:
    with open('model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    with open('encoder.pkl', 'rb') as f:
        loaded_encoder = pickle.load(f)
    print("Successfully loaded both model and encoder!")
    
    # Test with first row of your data
    test_data = X.iloc[0:1]  # Get first row of your features
    prediction = loaded_model.predict(test_data)
    print(f"\nTest prediction using loaded model: {prediction}")
    
except Exception as e:
    print(f"Error loading files: {e}")

