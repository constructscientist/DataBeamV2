import os

def verify_project():
    print("Verifying project structure...")
    
    # Required files and directories
    required = {
        'files': ['vercel.json', 'requirements.txt'],
        'dirs': ['api', 'models'],
        'models': ['.pkl files'],
        'api': ['main.py']
    }
    
    # Check root directory
    print("\nChecking root directory:")
    for file in required['files']:
        if os.path.exists(file):
            print(f"✅ Found {file}")
        else:
            print(f"❌ Missing {file}")
    
    # Check directories
    for dir_name in required['dirs']:
        if os.path.exists(dir_name):
            print(f"\nChecking {dir_name} directory:")
            if dir_name == 'models':
                pkl_found = False
                for file in os.listdir(dir_name):
                    if file.endswith('.pkl'):
                        print(f"✅ Found {file}")
                        pkl_found = True
                if not pkl_found:
                    print("❌ No .pkl files found")
            elif dir_name == 'api':
                if os.path.exists(os.path.join('api', 'main.py')):
                    print("✅ Found main.py")
                else:
                    print("❌ Missing main.py")
        else:
            print(f"❌ Missing {dir_name} directory")

verify_project() 