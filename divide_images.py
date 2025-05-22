import os
import shutil
import random

# Define the source directory and target directories
source_dir = 'dataset'
labels_dir = os.path.join(source_dir, 'labels')
target_dirs = ['Arun', 'Abhinas', 'Roman', 'Nashim', 'Aadish']


for dir_name in target_dirs:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# Ensure labels directory exists
if not os.path.exists(labels_dir):
    os.makedirs(labels_dir)

# Get all image files from the source directory, excluding those in labels directory
image_files = []
for f in os.listdir(source_dir):
    if f.endswith(('.jpg', '.jpeg', '.png')) and not os.path.exists(os.path.join(labels_dir, f)):
        image_files.append(f)

# Shuffle the files to ensure random distribution
random.shuffle(image_files)


total_files = len(image_files)
files_per_person = total_files // len(target_dirs)
extra_files = total_files % len(target_dirs)

# Distribute files
start_idx = 0
for i, dir_name in enumerate(target_dirs):
    # Calculate how many files this person gets
    num_files = files_per_person + (1 if i < extra_files else 0)
    
    # Get the files for this person
    person_files = image_files[start_idx:start_idx + num_files]
    
    # Move the files
    for file_name in person_files:
        # Copy to person's directory
        source_path = os.path.join(source_dir, file_name)
        target_path = os.path.join(dir_name, file_name)
        shutil.copy2(source_path, target_path)
    
    start_idx += num_files
    print(f"Copied {len(person_files)} files to {dir_name}")

print("\nDistribution complete!")
