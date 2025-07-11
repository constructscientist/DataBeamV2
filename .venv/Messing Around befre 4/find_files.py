import os

def print_directory_contents(path):
    print(f"\nContents of: {path}")
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                print(f"📁 {item} (folder)")
            else:
                print(f"📄 {item}")
    except Exception as e:
        print(f"Error reading directory: {e}")

# Get the current directory
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

# Print contents of current directory
print_directory_contents(current_dir)

# Print contents of DataBeam Project folder
databeam_path = os.path.join(current_dir, 'DataBeam Project')
if os.path.exists(databeam_path):
    print_directory_contents(databeam_path)
    
    # Check models folder if it exists
    models_path = os.path.join(databeam_path, 'models')
    if os.path.exists(models_path):
        print_directory_contents(models_path)

print("\nSearching for .pkl files...")
for root, dirs, files in os.walk(current_dir):
    for file in files:
        if file.endswith('.pkl'):
            full_path = os.path.join(root, file)
            size_mb = os.path.getsize(full_path) / (1024 * 1024)
            print(f"\nFound .pkl file:")
            print(f"Name: {file}")
            print(f"Location: {root}")
            print(f"Size: {size_mb:.2f} MB")
            
            if size_mb > 250:
                print("⚠️ WARNING: File is larger than Vercel's 250MB limit!")
            else:
                print("✅ File size is within Vercel's limit")

print("\nSearch complete!") 