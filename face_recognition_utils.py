# backend/model/face_recognition_utils.py

import os
import face_recognition

# Module‐level variables (so imports work)
known_face_encodings = []
known_face_names     = []

def load_known_faces(folder="Faculty_images"):
    """
    Load all .jpg/.jpeg/.png files from model/Faculty_images/ into memory.
    The filename (minus extension) becomes the recognized name.
    """

    # __file__ is .../backend/model/face_recognition_utils.py
    base_dir    = os.path.dirname(__file__)
    folder_path = os.path.join(base_dir, folder)  # .../backend/model/Faculty_images

    if not os.path.isdir(folder_path):
        print(f"[WARNING] Face folder not found: {folder_path}")
        return

    for fname in os.listdir(folder_path):
        # Only accept common image extensions
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        full_path = os.path.join(folder_path, fname)
        try:
            img  = face_recognition.load_image_file(full_path)
            encs = face_recognition.face_encodings(img)

            if not encs:
                print(f"[WARNING] No face found in: {fname}")
                continue

            known_face_encodings.append(encs[0])
            name = os.path.splitext(fname)[0]
            known_face_names.append(name)
            print(f"[INFO] Loaded encoding for: {name}")

        except Exception as e:
            print(f"[ERROR] Could not process {fname}: {e}")

    print(f"[INFO] Total known faces loaded: {len(known_face_names)}")
