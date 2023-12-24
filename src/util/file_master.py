import os, sys

project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)

def remove_file(file_path):
    os.remove(file_path)

def create_file_if_it_does_not_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as new_file:
            pass

def add_content_in_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(content)

def rewrite_file_with_content(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def read_lines_from_file(file_path):
    with open(file_path, 'r') as file:
    	return file.readlines()

def read_line_from_file(file_path):
    with open(file_path, 'r') as file:
    	return file.read()
