import pickle
import gzip
import os

# Load your existing model and encoder
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

# Save compressed versions
with gzip.open('model.pkl.gz', 'wb') as f:
    pickle.dump(model, f)
with gzip.open('encoder.pkl.gz', 'wb') as f:
    pickle.dump(encoder, f)

def search_all_directories(start_path):
    print(f"Starting search in: {start_path}\n")
    
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith('.pkl'):
                try:
                    full_path = os.path.join(root, file)
                    size_mb = os.path.getsize(full_path) / (1024 * 1024)
                    print(f"Found: {file}")
                    print(f"Location: {full_path}")
                    print(f"Size: {size_mb:.2f} MB\n")
                except Exception as e:
                    print(f"Error with {file}: {e}\n")

# Define the correct path to your DataBeam Project folder
base_path = r"C:\Users\ijtin\OneDrive - University of Nebraska-Lincoln\Data Science_AI_ML\Python Projects\.venv\DataBeam Project"

def check_files():
    print(f"Checking in: {base_path}")
    
    # Check models directory
    models_path = os.path.join(base_path, 'models')
    if os.path.exists(models_path):
        print("\nChecking models folder:")
        for file in os.listdir(models_path):
            if file.endswith('.pkl'):
                file_path = os.path.join(models_path, file)
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                print(f"Found {file} (Size: {size_mb:.2f} MB)")
    else:
        print("\nmodels folder not found")
    
    # Check root directory
    print("\nChecking root directory:")
    for file in os.listdir(base_path):
        if file.endswith('.pkl'):
            file_path = os.path.join(base_path, file)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"Found {file} (Size: {size_mb:.2f} MB)")

try:
    check_files()
except Exception as e:
    print(f"Error: {e}")
    print("Current working directory:", os.getcwd())

def get_file_size(file_path):
    size = os.path.getsize(file_path)
    return size / (1024 * 1024)  # Convert to MB

# Get current directory
current_dir = os.getcwd()

# Find and check pkl files
for root, dirs, files in os.walk(current_dir):
    for file in files:
        if file.endswith('.pkl'):
            full_path = os.path.join(root, file)
            size_mb = get_file_size(full_path)
            print(f"\nFile: {file}")
            print(f"Size: {size_mb:.2f} MB")
            
            if size_mb > 250:
                print("⚠️ WARNING: File is larger than Vercel's 250MB limit!")
            else:
                print("✅ File size is within Vercel's limit")

total_size = sum(get_file_size(os.path.join(root, file)) 
                 for root, _, files in os.walk(current_dir) 
                 for file in files if file.endswith('.pkl'))

print(f"\nTotal size of all .pkl files: {total_size:.2f} MB")
