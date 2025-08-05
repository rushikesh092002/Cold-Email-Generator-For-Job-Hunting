import os

def save_uploaded_file(uploaded_file, save_dir="uploades"):
    os.makedirs(save_dir , exist_ok=True)
    file_path = os.path.join(save_dir , uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path