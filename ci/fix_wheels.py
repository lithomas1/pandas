import shutil
import zipfile
import sys
import os

try:
    _, wheel_path, dest_dir, is_32 = sys.argv
    PYTHON_ARCH = "x86" if is32 else "x64"
except ValueError:
    # Too many/little values to unpack
    raise ValueError("User must pass in the path to the wheel"
                    "destination directory, and whether the Python is 32/64-bit"
                    "for the repaired wheel.")
# Wheels are zip files
if not os.path.isdir(dest_dir):
    print(f"Created directory {dest_dir}")
    os.mkdir(dest_dir)
shutil.copy(wheel_path, dest_dir) # Remember to delete if process fails
wheel_name = os.path.basename(wheel_path)
success = True
exception = None
repaired_wheel_path = os.path.join(dest_dir, wheel_name)
with zipfile.ZipFile(repaired_wheel_path, "a") as zipf:
    try:
        # TODO: figure out how licensing works for the redistributables
        base_redist_dir = f"C:/Program Files (x86)/Microsoft Visual Studio/2019/Enterprise/VC/Redist/MSVC/14.29.30133/{PYTHON_ARCH}/Microsoft.VC142.CRT/"
        zipf.write(os.path.join(base_redist_dir, "msvcp140.dll"), "pandas/_libs/window")
        zipf.write(os.path.join(base_redist_dir, "concrt140.dll"), "pandas/_libs/window")
        zipf.write(os.path.join(base_redist_dir, "vcruntime140_1.dll"), "pandas/_libs/window")
    except Exception as e:
        success = False
        exception = e

if not success:
    os.remove(repaired_wheel_path)
    raise exception
else:
    print(f"Successfully repaired wheel was written to {repaired_wheel_path}")
    
