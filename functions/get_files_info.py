import os
import sys

def get_files_info(boundary_directory, directory_to_check="."):
    ...
    # need to check whether the diretory_to_check is within the boundary directory
    abs_boundary_dir_path = os.path.abspath(boundary_directory)

    target_path = os.path.join(boundary_directory, directory_to_check)
    
    print(target_path)
    print(abs_boundary_dir_path)

    print(os.path.abspath(target_path))
    print(os.path.abspath(target_path).startswith(abs_boundary_dir_path))
    
    
    

# get_files_info("calculator", directory_to_check="bin")
get_files_info("calculator", directory_to_check=".")