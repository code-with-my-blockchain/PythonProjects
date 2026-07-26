import os

folder_path = r"C:\Users\user\OneDrive\Desktop\PYTHON\clutteredFolder"


if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' create kar diya gaya hai.")


for i in range(1, 6):
    file_name = f"random_photo_{i}.png"
    file_full_path = os.path.join(folder_path, file_name)
    
    
    with open(file_full_path, "w") as f:
        f.write("This is a dummy image file content.")
    
    print(f"Created: {file_name}")

print("\nAb aap apni 'clutter.py' wali script chala kar inhein rename kar sakte hain!")
