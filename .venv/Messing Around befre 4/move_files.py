import os
import shutil

# Create models directory if it doesn't exist
if not os.path.exists('models'):
    os.makedirs('models')

# Move the files from .venv to models directory
shutil.move('.venv/model.pkl', 'models/model.pkl')
shutil.move('.venv/encoder.pkl', 'models/encoder.pkl') 