import os
import shutil

def setup_project_structure():
    print("Setting up project structure...")
    
    # Create necessary directories
    directories = ['api', 'models']
    for dir_name in directories:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"Created {dir_name} directory")
    
    # Find and move pkl files to models directory
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith('.pkl'):
                source = os.path.join(root, file)
                destination = os.path.join('models', file)
                shutil.copy2(source, destination)
                print(f"Copied {file} to models directory")
    
    # Verify files were moved correctly
    print("\nVerifying files in models directory:")
    if os.path.exists('models'):
        for file in os.listdir('models'):
            if file.endswith('.pkl'):
                size_mb = os.path.getsize(os.path.join('models', file)) / (1024 * 1024)
                print(f"Found {file} (Size: {size_mb:.2f} MB)")

    print("\nSetup complete! Ready for deployment.")

if __name__ == "__main__":
    setup_project_structure() 