import pickle
import pandas as pd
import os

print("Checking for saved model files...")

# Check if files exist
if os.path.exists('model.pkl'):
    print(f"model.pkl exists! File size: {os.path.getsize('model.pkl')} bytes")
else:
    print("model.pkl not found")

if os.path.exists('encoder.pkl'):
    print(f"encoder.pkl exists! File size: {os.path.getsize('encoder.pkl')} bytes")
else:
    print("encoder.pkl not found")

# Try to load and use the model
try:
    # Load the model and encoder
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)
    print("\nSuccessfully loaded both model and encoder!")
    
    # Create a sample input to test the model
    sample_data = pd.DataFrame({
        'project_type': ['Commercial'],  # Adjust this to match your actual project types
        # Add other features that your model expects
    })
    
    # Encode the project type
    type_encoded = encoder.transform(sample_data[['project_type']])
    type_cols = encoder.get_feature_names_out(['project_type'])
    type_df = pd.DataFrame(type_encoded, columns=type_cols)
    
    # Make a prediction
    prediction = model.predict(type_df)
    probability = model.predict_proba(type_df)
    
    print("\nTest prediction successful!")
    print(f"Prediction: {'Win' if prediction[0] == 1 else 'Loss'}")
    print(f"Win probability: {probability[0][1]:.2%}")
    
except Exception as e:
    print(f"\nError testing the model: {e}")