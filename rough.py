import os

# Define the root directory for the file system
root_dir = 'file_system'
disk = [None] * 4096  # 1024 blocks in the disk
total_blocks = len(disk)
used_blocks = 0
# Define the maximum size of the file system in bytes
max_size = 1048576  # 1 MB

# Check if the root directory exists, create it if it doesn't
if not os.path.exists(root_dir):
    os.makedirs(root_dir)

# Calculate the current size of the file system
current_size = sum(
    os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(root_dir) for filename
    in filenames)


# Define a function to calculate the available space in the file system
def get_available_space():
    return max_size - current_size


# Define a function to create a new file
def creation(name, size):
    global current_size
    available_space = get_available_space()
    if size > available_space:
        return False
    else:
        file_path = os.path.join(root_dir, name)
        with open(file_path, 'wb') as f:
            f.write(os.urandom(size))
        current_size += size
        return True


# Define a function to delete a file
def deletion(name):
    global current_size
    file_path = os.path.join(root_dir, name)
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        os.remove(file_path)
        current_size -= file_size
        return True
    else:
        return False


# Define a function to rename a file
def renaming(old_name, new_name):
    file_path = os.path.join(root_dir, old_name)
    if os.path.exists(file_path):
        new_path = os.path.join(root_dir, new_name)
        os.rename(file_path, new_path)
        return True
    else:
        return False


def calculate_fragmentation():
    free_blocks = 0
    for i in range(total_blocks):
        if disk[i] == None:
            free_blocks += 1
    return free_blocks


# Define a function to move a file to a new location
def moving(name, new_location):
    file_path = os.path.join(root_dir, name)
    if os.path.exists(file_path):
        new_path = os.path.join(root_dir, new_location, name)
        if not os.path.exists(os.path.join(root_dir, new_location)):
            os.makedirs(os.path.join(root_dir, new_location))
        os.rename(file_path, new_path)
        return True
    else:
        return False


# Define a function to display the files in the file system
def display_files():
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_size = os.path.getsize(file_path)
            print(f'{filename} ({file_size} bytes)')


# Main loop
while True:
    print('Select an operation:')
    print('1. Creation of a new file')
    print('2. Deletion of an existing file')
    print('3. Moving an existing file to a new location')
    print('4. Renaming an existing file')
    print('5. Displaying the files in the file system')
    print("6. To know Fragmentation")
    print('7. Exit')
    operation = input('Enter the operation you need to do: ')
    if operation == '1':
        name = input('Enter the name of the file: ')
        size = int(input('Enter the size of the file in bytes: '))
        if creation(name, size):
            print('Added the file successfully')
        else:
            print('Not enough space in the file system to create the file')
    elif operation == '2':
        name = input('Enter the name of the file to delete: ')
        if deletion(name):
            print('File deleted successfully')
        else:
            print('File not found')
    elif operation == '3':
        name = input('Enter the name of the file to move: ')
        new_location = input('Enter the new location for the file: ')
        if moving(name, new_location):
            print('File moved successfully')
        else:
            print('File not found')
    elif operation == '4':
        old_name = input('Enter the name of the file to rename: ')
        new_name = input('Enter the new name for the file: ')
        if renaming(old_name, new_name):
            print('File renamed successfully')
        else:
            print('File not found')

    elif operation == '5':
        print('Files in the file system:')
        display_files()
    elif operation == "6":
        print("No. of Fragmented blocks are: {}".format(calculate_fragmentation()))
    elif operation == '7':
        break

    else:
        print('Enter the valid operation')