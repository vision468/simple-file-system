# مستندات سیستم فایل مازوست (Mazust File System)
## مقدمه

MazustFileSystem یک پیاده‌سازی ساده از سیستم فایل در پایتون است که به کاربران اجازه می‌دهد فایل‌ها و دایرکتوری‌ها را ایجاد، مدیریت و با آن‌ها تعامل داشته باشند. این سیستم از ایجاد فایل و دایرکتوری، خواندن از فایل‌ها، نوشتن به فایل‌ها و حذف فایل‌ها یا دایرکتوری‌ها پشتیبانی می‌کند.

### کلاس‌ها و کاربرد آن‌ها

- MazustFileSystem:

مدیریت عملکردهای اصلی سیستم فایل، از جمله ایجاد فایل‌ها و دایرکتوری‌ها، حذف آن‌ها، خواندن محتویات فایل‌ها و نوشتن داده به فایل‌ها.
نگه‌داری متادیتا درباره فایل‌ها و دایرکتوری‌ها و مدیریت فضای در دسترس روی دیسک.

- SimpleFileSystemCLI:

ارائه یک رابط خط فرمان برای تعامل با MazustFileSystem.
به کاربران اجازه می‌دهد تا دستورات را برای مدیریت فایل‌ها و دایرکتوری‌ها از طریق یک رابط کاربری مبتنی بر ترمینال اجرا کنند.
### کلاس: MazustFileSystem

- ویژگی‌ها:

**disk_file**: نام فایلی که ذخیره‌سازی دیسک را شبیه‌سازی می‌کند.

**free_blocks**: فهرستی نگه‌داری‌ شده از بلوک‌های در دسترس روی دیسک برای ذخیره‌سازی فایل.

**files**: دیکشنری که کلیدها نام فایل‌ها و مقادیر متادیتای مربوط به فایل‌ها هستند.

**directories**: دیکشنری تو در تو که ساختار دایرکتوری‌ها و زیر دایرکتوری‌ها را نمایان می‌کند.

**current_directory**: نقطه‌گذاری که نشان‌دهنده دایرکتوری فعلی است.

- متدها:

*__init__*(self, disk_file)

ورودی: disk_file (str) - نام فایلی که نماینده دیسک است.

خروجی: None

منطق: سیستم فایل را با راه‌اندازی متغیرها و فراخوانی initialize_file_system() راه‌اندازی می‌کند.

*initialize_file_system(self)*

ورودی: None

خروجی: None

منطق: سوپر بلاک را در فایل دیسک تنظیم کرده و free_blocks را راه‌اندازی می‌کند.

*touch(self, file_name)*

ورودی: file_name (str) - نام فایلی که باید ایجاد شود.

خروجی: None

منطق: یک فایل خالی ایجاد می‌کند اگر قبلاً وجود نداشته باشد. یک بلوک شروع از free_blocks تخصیص می‌دهد.

*write(self, file_name, data)*

ورودی: file_name (str) - نام فایلی که باید نوشته شود، data (str) - محتوایی که باید نوشته شود.

خروجی: None

منطق: داده را به فایل مشخص شده می‌نویسد و تعداد بلوک‌های مورد نیاز را تعیین می‌کند.

*cat(self, file_name)*

ورودی: file_name (str) - نام فایلی که باید خوانده شود.

خروجی: None

منطق: محتویات فایل مشخص شده را می‌خواند و نمایش می‌دهد.

*rm(self, file_name)*

ورودی: file_name (str) - نام فایلی که باید حذف شود.

خروجی: None

منطق: فایل مشخص شده را حذف کرده و بلوک‌های تخصیص داده شده را آزاد می‌کند.

*mkdir(self, directory_name)*

ورودی: directory_name (str) - نام دایرکتوری که باید ایجاد شود.

خروجی: None

منطق: یک دایرکتوری جدید ایجاد می‌کند اگر از قبل وجود نداشته باشد.

*rmdir(self, directory_name)*

ورودی: directory_name (str) - نام دایرکتوری که باید حذف شود.

خروجی: None

منطق: دایرکتوری مشخص شده را اگر خالی باشد حذف می‌کند.

*ls(self)*

ورودی: None

خروجی: None

منطق: فایل‌ها و دایرکتوری‌ها را در دایرکتوری فعلی لیست می‌کند.

*cd(self, directory_name)*

ورودی: directory_name (str) - نام دایرکتوری که باید به آن تغییر نماییم.

خروجی: None

منطق: دایرکتوری فعلی را به دایرکتوری مشخص شده تغییر می‌دهد اگر معتبر باشد.

*normalize_paths(self)*

ورودی: None

خروجی: لیستی از str - مسیرهای نرمالized در سیستم فایل.

منطق: یک لیست از تمام مسیرهای معتبر در سیستم ایجاد می‌کند.

*__find_paths(self, tree=None, current_path=None)*

ورودی: tree (dict) - درخت دایرکتوری که باید پیمایش شود، current_path (list) - مسیر جاری که در حال ساخت است.

خروجی: لیستی از لیست‌ها - هر لیست نمایانگر یک مسیر معتبر در سیستم فایل است.

منطق: به صورت بازگشتی به دنبال تمام مسیرها در درخت دایرکتوری می‌گردد.

*__create_valid_path(self, path)*

ورودی: path (list) - اجزای مسیر.

خروجی: str - یک مسیر معتبر به عنوان رشته.

منطق: یک رشته مسیر معتبر از اجزای مسیر تشکیل می‌دهد.

*__get_directory(self, dir_name)*

ورودی: dir_name (str) - نام دایرکتوری.

خروجی: dict - محتوای دایرکتوری.

منطق: محتوای دایرکتوری مورد نظر را از درخت دایرکتوری دریافت می‌کند.

*__find_directory(self, current_dir, parts)*

ورودی: current_dir (dict) - دایرکتوری جاری، parts (list) - اجزاء مسیر.

خروجی: dict - دایرکتوری نمایانگر اجزاء مسیر.

منطق: به دنبال دایرکتوری در درخت دایرکتوری جاری می‌گردد.

*__is_file(self, file_name, dir_temp=None)*

ورودی: file_name (str) - نام فایلی که باید بررسی شود، dir_temp (dict) - دایرکتوری که باید در آن جستجو کند.

خروجی: bool - اگر مورد یک فایل باشد True، در غیر این صورت False.

منطق: بررسی می‌کند که آیا file_name به عنوان یک فایل در دایرکتوری مشخص شده وجود دارد یا خیر.

*__has_file_attributes(self, attr)*

ورودی: attr (list) - ویژگی‌هایی که باید بررسی شوند.

خروجی: bool - اگر ویژگی‌های لازم وجود داشته باشد True، در غیر این صورت False.

منطق: تعیین می‌کند آیا ویژگی‌های لازم (اندازه، بلوک آغازین، زمان‌سنجی) در متادیتای فایل وجود دارد.

### کلاس: SimpleFileSystemCLI

- ویژگی‌ها:

**sfs**: یک نمونه از MazustFileSystem که برای تعامل استفاده می‌شود.

- متدها:

*__init__(self, sfs)*

ورودی: sfs (MazustFileSystem) - یک نمونه از کلاس MazustFileSystem.

خروجی: None

منطق: CLI را با نمونه MazustFileSystem راه‌اندازی می‌کند.

*do_touch(self, arg)*

ورودی: arg (str) - نام فایلی که باید ایجاد شود.

خروجی: None

منطق: متد touch کلاس MazustFileSystem را برای ایجاد یک فایل فراخوانی می‌کند.

*do_write(self, arg)*

ورودی: arg (str) - نام فایل و داده‌ای که باید نوشته شود.

خروجی: None

منطق: متد write کلاس MazustFileSystem را برای نوشتن داده به یک فایل فراخوانی می‌کند.

*do_cat(self, arg)*

ورودی: arg (str) - نام فایلی که باید خوانده شود.

خروجی: None

منطق: متد cat کلاس MazustFileSystem را برای نمایش محتویات فایل فراخوانی می‌کند.

*do_rm(self, arg)*

ورودی: arg (str) - نام فایلی که باید حذف شود.

خروجی: None

منطق: متد rm کلاس MazustFileSystem را برای حذف یک فایل فراخوانی می‌کند.

*do_mkdir(self, arg)*

ورودی: arg (str) - نام دایرکتوری که باید ایجاد شود.

خروجی: None

منطق: متد mkdir کلاس MazustFileSystem را برای ایجاد یک دایرکتوری فراخوانی می‌کند.

*do_rmdir(self, arg)*

ورودی: arg (str) - نام دایرکتوری که باید حذف شود.

خروجی: None

منطق: متد rmdir کلاس MazustFileSystem را برای حذف یک دایرکتوری فراخوانی می‌کند.

*do_ls(self, arg)*

ورودی: arg (str) - استفاده نمی‌شود و فقط نیاز به یک رشته خالی دارد.

خروجی: None

منطق: متد ls کلاس MazustFileSystem را برای لیست کردن فایل‌ها و دایرکتوری‌ها فراخوانی می‌کند.

*do_cd(self, arg)*

ورودی: arg (str) - نام دایرکتوری که باید به آن تغییر وضعیت دهیم.

خروجی: None

منطق: متد cd کلاس MazustFileSystem را برای تغییر دایرکتوری فعلی فراخوانی می‌کند.

*do_exit(self, arg)*

ورودی: arg (str) - استفاده نمی‌شود و فقط نیاز به یک رشته خالی دارد.

خروجی: None

منطق: برای خروج از جلسه CLI به کار می‌رود.

## نحوه استفاده
- برای ایجاد یک فایل، تایپ کنید touch <file_name>.
- برای نوشتن داده به یک فایل، تایپ کنید write <file_name> <data>.
- برای خواندن یک فایل، تایپ کنید cat <file_name>.
- برای حذف یک فایل، تایپ کنید rm <file_name>.
- برای ایجاد یک دایرکتوری، تایپ کنید mkdir <directory_name>.
- برای لیست کردن فایل‌ها و دایرکتوری‌ها، تایپ کنید ls.
- برای تغییر دایرکتوری، از cd <directory_name> یا cd .. برای رفتن یک سطح بالا استفاده کنید.
- برای خروج، تایپ کنید exit.

این مستندات یک مرور جامع از کلاس MazustFileSystem و CLI مربوطه را ارائه می‌دهد و جزئیات مختلف متدها و عملکرد آن‌ها را توضیح می‌دهد


# Mazust File System

## Overview

The MazustFileSystem is a basic file system implementation in Python that allows users to create, manage, and interact with a virtual file system. It supports the creation of files and directories, reading from files, writing to files, and removing files or directories.

### Classes and Their Purpose

- MazustFileSystem:

Manages the core functionalities of the file system, including creating files and directories, removing them, reading file contents, and writing data to files.
Holds metadata about files and directories, and manages available space on the disk.

- SimpleFileSystemCLI:

Provides a command-line interface to interact with the MazustFileSystem.
Allows users to execute commands to manage files and directories through a user-friendly terminal interface.

### Class: MazustFileSystem

- Attributes:

**disk_file**: The name of the file that simulates the disk storage.

**free_blocks**: A list maintaining available blocks on the disk for file storage.

**files**: A dictionary where keys are file names, and values are dictionaries containing file metadata.

**directories**: A nested dictionary representing the structure of directories and subdirectories.

**current_directory**: A string representing the currently active directory.

- Methods:

*__init__(self, disk_file)*

Input: disk_file (str) - The name of the file representing the disk.

Output: None

Logic: Initializes the file system by setting up variables and calling initialize_file_system().

*initialize_file_system(self)*

Input: None

Output: None

Logic: Sets up the superblock in the disk file, initializes the free_blocks, and prepares the disk for file operations.

*touch(self, file_name)*

Input: file_name (str) - The name of the file to create.

Output: None

Logic: Creates an empty file if it doesn't exist already. Allocates a start block from free_blocks.

*write(self, file_name, data)*

Input: file_name (str) - The name of the file to write to, data (str) - The content to write.

Output: None

Logic: Writes data to the specified file by determining how many blocks are needed and writing to each block sequentially.

*cat(self, file_name)*

Input: file_name (str) - The name of the file to read from.

Output: None

Logic: Reads and displays the contents of the specified file.

*rm(self, file_name)*

Input: file_name (str) - The name of the file to remove.

Output: None

Logic: Deletes the specified file and frees up its allocated blocks.

*mkdir(self, directory_name)*

Input: directory_name (str) - The name of the directory to create.

Output: None

Logic: Creates a new directory if it doesn't already exist.

*rmdir(self, directory_name)*

Input: directory_name (str) - The name of the directory to remove.

Output: None

Logic: Removes the specified directory if it is empty.

*ls(self)*

Input: None

Output: None

Logic: Lists the files and directories in the current directory.

*cd(self, directory_name)*

Input: directory_name (str) - The name of the directory to change to.

Output: None

Logic: Changes the current directory to the specified one if it is valid.

*normalize_paths(self)*

Input: None

Output: List of str - Normalized paths in the file system.

Logic: Generates a list of all valid paths in the system.

*__find_paths(self, tree=None, current_path=None)*

Input: tree (dict) - The directory tree to traverse, current_path (list) - The current path being built.

Output: List of list - Each list represents a valid path in the file system.

Logic: Recursively finds all paths in the given directory tree.

*__create_valid_path(self, path)*

Input: path (list) - Path components.

Output: str - A valid path as a string.

Logic: Constructs a valid path string from path components.

*__get_directory(self, dir_name)*

Input: dir_name (str) - The name of the directory.

Output: dict - The directory's contents.

Logic: Retrieves the specified directory's contents from the directory tree.

*__find_directory(self, current_dir, parts)*

Input: current_dir (dict) - The current directory, parts (list) - Parts of the path.

Output: dict - The directory represented by the path parts.

Logic: Searches for the directory in the current directory tree.

*__is_file(self, file_name, dir_temp=None)*

Input: file_name (str) - The name of the file to check, dir_temp (dict) - Directory to search in.

Output: bool - True if the item is a file, False otherwise.

Logic: Checks if the given file_name exists as a file in the specified directory.

*__has_file_attributes(self, attr)*

Input: attr (list) - Attributes to check.

Output: bool - True if required attributes exist, False otherwise.

Logic: Determines if the necessary attributes (size, start_block, timestamp) are present in the file's metadata.

### Class: SimpleFileSystemCLI

- Attributes:

**sfs**: An instance of the MazustFileSystem used for interaction.

-Methods:

*__init__(self, sfs)*

Input: sfs (MazustFileSystem) - An instance of the MazustFileSystem class.

Output: None

Logic: Initializes the CLI with the MazustFileSystem instance.

*do_touch(self, arg)*

Input: arg (str) - Name of the file to create.

Output: None

Logic: Calls touch method of MazustFileSystem to create a file.

*do_write(self, arg)*

Input: arg (str) - The file name and data to write.

Output: None

Logic: Calls write method of MazustFileSystem to write data to a file.

*do_cat(self, arg)*

Input: arg (str) - Name of the file to read.

Output: None

Logic: Calls cat method of MazustFileSystem to display file contents.

*do_rm(self, arg)*

Input: arg (str) - Name of the file to delete.

Output: None

Logic: Calls rm method of MazustFileSystem to delete a file.

*do_mkdir(self, arg)*

Input: arg (str) - Name of the directory to create.

Output: None

Logic: Calls mkdir method of MazustFileSystem to create a directory.

*do_rmdir(self, arg)*

Input: arg (str) - Name of the directory to remove.

Output: None

Logic: Calls rmdir method of MazustFileSystem to remove a directory.

*do_ls(self, arg)*

Input: arg (str) - Not used, just requires an empty string.

Output: None

Logic: Calls ls method of MazustFileSystem to list files and directories.

*do_cd(self, arg)*

Input: arg (str) - Name of the directory to change to.

Output: None

Logic: Calls cd method of MazustFileSystem to change the current directory.

*do_exit(self, arg)*

Input: arg (str) - Not used, just requires an empty string.

Output: None

Logic: Exits the CLI session.

## Usage

- To create a file, type touch <file_name>.
- To write data to a file, type write <file_name> <data>.
- To read a file, type cat <file_name>.
- To delete a file, type rm <file_name>.
- To create a directory, type mkdir <directory_name>.
- To list files and directories, type ls.
- To change directories, use cd <directory_name> or cd .. to go up one level.
- To exit, type exit.

This documentation provides a comprehensive overview of the MazustFileSystem class and its associated CLI, detailing the various methods and their functionality.