import os
import time
import cmd
from datetime import datetime
BLOCK_SIZE = 4096  
SUPERBLOCK_SIZE = BLOCK_SIZE

class SimpleFileSystem:
    def __init__(self, disk_file):
        self.disk_file = disk_file
        self.free_blocks = []
        self.files = {}
        self.directories = {"/": {}}
        self.current_directory = "/" # "/" : root , "./a": root / a, "./a/b": root / a / b
        self.initialize_file_system()
        print("Mazust File System Init!")

    def initialize_file_system(self):
        total_size = 100 * BLOCK_SIZE  
        data_size = total_size - SUPERBLOCK_SIZE  
        num_blocks = data_size // BLOCK_SIZE
        fileSystemType = 'FileSystemMazust'.encode('utf-8')
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode('utf-8')
        status = '****'.encode('utf-8')
        with open(self.disk_file, 'wb') as f:
            superblock_data = (
            BLOCK_SIZE.to_bytes(4, 'little') +  
            total_size.to_bytes(4, 'little') +  
            num_blocks.to_bytes(4, 'little') + 
            (fileSystemType ) + 
            (date_created) +
            (status) + 
            b'\x00' * (SUPERBLOCK_SIZE - (12 + len(fileSystemType + date_created + status) )) 
            )
            f.write(superblock_data) # Bottom of file
            # rest of disk
            f.write(b'\x00' * data_size) # Top of file
        self.free_blocks = list(range(num_blocks))
        print(f'free_blocks {self.free_blocks}')
    def touch(self, file_name):
        if file_name in self.files:
            print("File already exists.")
            return
        start_block = self.free_blocks.pop() if self.free_blocks else None
        if start_block is None:
            print("No enough space to create file.")
            return
        metadata = {'size': 0, 'start_block': start_block, 'timestamp': time.time()}
        self.files[file_name] = metadata
        self.__get_directory(self.current_directory)[file_name] = metadata
        print(f"File '{file_name}' created.")

    def write(self, file_name, data):
        if file_name not in self.files:
            print("File does not exist.")
            return
        metadata = self.files[file_name]
        data_bytes = data.encode('utf-8')
        blocks_needed = (len(data_bytes) + BLOCK_SIZE - 1) // BLOCK_SIZE
        
        block = metadata['start_block']
        for _ in range(blocks_needed):
            if not self.free_blocks:
                print("Not enough space to write.")
                return
            with open(self.disk_file, 'r+b') as f:
                f.seek(block * BLOCK_SIZE)
                f.write(data_bytes[:BLOCK_SIZE])
                data_bytes = data_bytes[BLOCK_SIZE:]
            block += 1
        metadata['size'] += len(data)
        print(f"Data written to file '{file_name}'.")

    def cat(self, file_name):
        if file_name not in self.files:
            print("File does not exist.")
            return
        metadata = self.files[file_name]
        data = b''
        block = metadata['start_block']
        blocks_to_read = (metadata['size'] + BLOCK_SIZE - 1) // BLOCK_SIZE
        
        with open(self.disk_file, 'rb') as f:
            for _ in range(blocks_to_read):
                f.seek(block * BLOCK_SIZE)
                data += f.read(BLOCK_SIZE)
                block += 1
                
        print(f"Contents of '{file_name}':")
        print(f"{data.decode('utf-8')}")

    def rm(self, file_name):
        if file_name not in self.files:
            print("File does not exist.")
            return
        metadata = self.files.pop(file_name)
        block = metadata['start_block']
        blocks_to_free = (metadata['size'] + BLOCK_SIZE - 1) // BLOCK_SIZE
        
        for _ in range(blocks_to_free):
            self.free_blocks.append(block)
            block += 1
        del self.__get_directory(self.current_directory)[file_name]
        print(f"File '{file_name}' deleted.")

    def mkdir(self, directory_name):
        if directory_name in self.__get_directory(self.current_directory):
            print("Directory already exists.")
            return
        directory_name = directory_name #if directory_name[0] == '/' else '/' + directory_name
        # self.directories[self.current_directory][directory_name] = {}
        self.__get_directory(self.current_directory)[directory_name] = {}
        print(f"Directory '{directory_name}' created.")
        print(f"All Directory '{self.directories}'")

    def rmdir(self, directory_name):
        if directory_name not in self.__get_directory(self.current_directory):
            print("Directory does not exist.")
            return
        if self.__get_directory(self.current_directory)[directory_name]:
            print("Directory is not empty.")
            return
        del self.__get_directory(self.current_directory)[directory_name]
        print(f"Directory '{directory_name}' deleted.")

    def ls(self):
        print(f"Files and directories in {self.current_directory}:")
        ls_temp = self.__get_directory(self.current_directory)
        if ls_temp == {}:
            print("Empty directory")
        for item in ls_temp.keys():
            type_status = 'file' if self.__is_file(item, ls_temp) else 'dir'
            print(f" {type_status} - {item}")
            # print( self.directories[self.current_directory][item])

    def cd(self, directory_name):
        if directory_name == "..":
            if self.current_directory != "/":
                parent_dir = '/'.join(self.current_directory.split('/')[:-1]) or '/'
                self.current_directory = parent_dir
                print(f"Changed to directory '{self.current_directory}'.")
        
        # elif directory_name in self.directories[self.current_directory]:
        elif directory_name in self.__get_directory(self.current_directory):
            if self.__is_file(directory_name): 
                print(f"! {directory_name} is a file, it's not possible to execute the CD command.")
            else:
                print(f"current directory: {self.current_directory}")
                if self.current_directory != '/':
                    full_directory_name = f"{self.current_directory}/{directory_name}"  
                else: 
                    full_directory_name = f"{self.current_directory}{directory_name}"
                    
                print(f"fdn: {full_directory_name}")
                all_paths = self.normalize_paths()
                print( f"all Paths:  {all_paths}")
                if full_directory_name in all_paths:
                    self.current_directory = full_directory_name
                    print(f"Changed directory to '{self.current_directory}'.")
                else:
                    print("Directory does not exist. (inner)")
        else:
            print("Directory does not exist. (outer)")

    def normalize_paths(self):
        raw_paths = self.__find_paths(self.__get_directory(self.current_directory)) + self.__find_paths(self.directories)
        print(f"raw_paths: {raw_paths}")
        
        [print(f" path {path}") for path in raw_paths]
        normalized_paths = [self.__create_valid_path(path) for path in raw_paths]
        return normalized_paths

    def __find_paths(self, tree=None, current_path=None):
        if tree is None:
            tree = self.directories
            
        if current_path is None:
            current_path = []

        if not isinstance(tree, dict):
            raise ValueError("The input 'tree' must be a dictionary.")

        paths = []
        for key, value in tree.items():
            # print(f"key: {key}, value: {value}, paths: {paths}")
            new_path = current_path + [key]
            # print(f"new path: {new_path}")
            # print(f" when key is {key} value is: {(value.keys())}")
            # if (not value) or (("size" and  "start_block" and "timestamp") in value.keys()) :  
            if not value:
                paths.append(new_path)
            elif self.__has_file_attributes(value):
                paths.append(new_path)
            else:
                paths.append(new_path)
                paths.extend(self.__find_paths(value, new_path))
        print(f"final paths: {paths}")
        return paths

    def __create_valid_path(self, path):
        if path[0] == '/':
            return '/' + '/'.join(path[1:])
        if self.current_directory[0] == '/':
            return '/' + '/'.join(path)
        return '/'.join(path)
        # return os.path.join(*path)

    def __get_directory(self, dir_name):
        parts = (['/'] + dir_name[1:].split('/')) if dir_name[0] == '/' else dir_name.split('/')
        # parts = parts.pop() if parts[-1] == '' else parts
        # print(f"__get_directory: {parts, dir_name}")
        return self.__find_directory(self.directories, parts)

    def __find_directory(self, current_dir, parts):
        if not parts or parts[0] == '': 
            return current_dir
        # print(f"__find_directory:  Current_dir {current_dir}, parts {parts}")
        first_part = parts[0]  
        if first_part in current_dir:
            return self.__find_directory(current_dir[first_part], parts[1:])  
        else:
            return {}  
    def __is_file(self, file_name, dir_temp=None):
        if not isinstance(dir_temp, dict):
            dir_temp = self.__get_directory(self.current_directory)
        # print(f'file_name: {file_name} dir_temp: {dir_temp}')
        if (file_name in dir_temp) and isinstance(dir_temp[file_name], dict) and self.__has_file_attributes(dir_temp[file_name].keys()) :
            return True
        return False
    def __has_file_attributes(self, attr):
        return True if ("size" and  "start_block" and "timestamp") in attr else False 


class SimpleFileSystemCLI(cmd.Cmd):
    intro = 'Welcome to the Mazust File System. Type help or ? to list commands.'
    prompt = '(Mazust FS) >'

    def __init__(self, sfs):
        super().__init__()
        self.sfs = sfs

    def do_touch(self, arg):
        'Create an empty file: touch <file_name>'
        self.sfs.touch(arg)

    def do_write(self, arg):
        'Write to a file: write <file_name> <data>'
        args = arg.split(" ", 1)
        if len(args) < 2:
            print("Please provide file name and data.")
            return
        self.sfs.write(args[0], args[1])

    def do_cat(self, arg):
        'Display the contents of a file: cat <file_name>'
        self.sfs.cat(arg)

    def do_rm(self, arg):
        'Delete a file: rm <file_name>'
        self.sfs.rm(arg)

    def do_mkdir(self, arg):
        'Create a new directory: mkdir <directory_name>'
        self.sfs.mkdir(arg)

    def do_rmdir(self, arg):
        'Remove a directory: rmdir <directory_name>'
        self.sfs.rmdir(arg)

    def do_ls(self, arg):
        'List files in the current directory: ls'
        self.sfs.ls()

    def do_cd(self, arg):
        'Change directory: cd <directory_name>'
        self.sfs.cd(arg)

    def do_exit(self, arg):
        'Exit the CLI: exit'
        print("Goodbye Mazust!")
        return True


sfs = SimpleFileSystem("disk.sfs")
cli = SimpleFileSystemCLI(sfs)
cli.cmdloop()
