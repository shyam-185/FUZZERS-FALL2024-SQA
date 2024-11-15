import os
import pandas as pd
import numpy as np
import time
import datetime 
from unittest.mock import patch

# Fuzzer for question 4b            
# Method 1 - getFileLength from: /MLForensics-farzana/empirical/dataset.stats.py
def getFileLength(file_):
    return sum(1 for line in open(file_, encoding='latin-1'))

# Fuzzing Method 1: getFileLength
def fuzz_getFileLength():
    print("\n=== Fuzzing getFileLength ===")
    invalid_cases = [
        "non_existent_file.txt",  # File does not exist
        None,  # None as input
        "",  # Empty string as file path
    ]
    for i, file_ in enumerate(invalid_cases):
        print(f"\nTest Case {i + 1}:")
        try:
            result = getFileLength(file_)
            print(f"Input: {file_} -> Lines: {result}")
        except Exception as e:
            print(f"Input: {file_} -> Exception: {e}")
            
            
# Method 2 getGeneralStats from: /MLForensics-farzana/empirical/dataset.stats.py
# Needed for gotGeneralStats
def getAllFileCount(df_):
    tot_fil_size = 0
    file_names_ = np.unique(df_['FILE_FULL_PATH'].tolist())
    for file_ in file_names_:
        tot_fil_size = tot_fil_size + getFileLength(file_)
    return tot_fil_size, len(file_names_)

def getGeneralStats(all_dataset_list):
    all_repos = [] 
    for result_file in all_dataset_list:
        print('='*50)
        print(result_file)
        print('='*50)
        res_df    = pd.read_csv( result_file ) 
        if 'ZOO' in result_file:
            temp_dirs = np.unique( res_df['REPO_FULL_PATH'].tolist() ) 
            for temp_dir in temp_dirs:
                list_subfolders_with_paths = [f.path for f in os.scandir(temp_dir) if f.is_dir()]
                all_repos = all_repos + list_subfolders_with_paths 
        else: 
            all_repos = np.unique( res_df['REPO_FULL_PATH'].tolist() )
        print('REPO_COUNT:', len(all_repos) ) 
        file_size, file_count   = getAllFileCount(res_df)
        print('ALL_FILE_COUNT:', file_count  ) 
        print('ALL_FILE_SIZE:', file_size  )   
        start_date, end_date, coms, devs  = getAllCommits( all_repos ) 
        print('COMMIT_COUNT:', coms )
        print('DEVS_COUNT:', devs )
        print('START_DATE:', start_date )
        print('END_DATE:', end_date )
        print('='*50)            
            
# Fuzz Method 2: getGeneralStats
def fuzz_getGeneralStats():
    print("\n=== Fuzzing getGeneralStats ===")
    temp_dir = "test_datasets"

    # Collect all files in the directory
    if not os.path.exists(temp_dir):
        print(f"Directory '{temp_dir}' does not exist.")
        return

    test_cases = [os.path.join(temp_dir, file_name) for file_name in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, file_name))]

    for i, dataset_list in enumerate([[file] for file in test_cases] + [test_cases]):
        print(f"\nTest Case {i + 1}:")
        try:
            getGeneralStats(dataset_list)
        except Exception as e:
            print(f"Input: {dataset_list} -> Exception: {e}")
            
            
# Method 3 - dumpContentIntoFile from: MLForensics-farzana/mining/git.repo.miner.py
def dumpContentIntoFile(strP, fileP):
    fileToWrite = open(fileP, 'w')
    fileToWrite.write(strP)
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

# Fuzz Method 3: get_dumpContentInfoFile
def fuzz_dumpContentIntoFile():
    print("\n=== Fuzzing dumpContentIntoFile ===")
    
    fuzz_dir = "fuzz_test"
    os.makedirs(fuzz_dir, exist_ok=True)

    test_cases = [
        ("Hello, World!", "valid.txt"),  # Valid content and file path
        ("", "empty.txt"),  # Empty content
        ("LongContent" * 100, "long_content.txt"),  # Long content
        (None, "null_content.txt"),  # None as content
        ("Hello", ""),  # Empty file path
    ]

    for i, (content, file_name) in enumerate(test_cases):
        print(f"\nTest Case {i + 1}:")
        try:
            file_path = os.path.join(fuzz_dir, file_name)

            if not file_name:
                raise ValueError("File name cannot be empty.")

            result = dumpContentIntoFile(content, file_path)
            print(f"Input: content='{content}', file_path='{file_path}' -> Size: {result} bytes")
        except Exception as e:
            print(f"Input: content='{content}', file_path='{file_name}' -> Exception: {e}")
            
    # Cleanup the fuzz_test directory
    for file in os.listdir(fuzz_dir):
        os.remove(os.path.join(fuzz_dir, file))
    os.rmdir(fuzz_dir)


# Method 4 - getPythonCount from: MLForensics-farzana/mining/git.repo.miner.py
# Removed 'full_path_file = os.path.join(root_, file_)'
def getPythonCount(path2dir):
    usageCount = 0
    for root_, dirnames, filenames in os.walk(path2dir):
        for file_ in filenames:
            if file_.endswith('py'):
                usageCount += 1
    return usageCount

# Fuzz Method 4: getPythonCount
def fuzz_getPythonCount():
    print("\n=== Fuzzing getPythonCount ===")

    fuzz_dir = "fuzz_test"
    os.makedirs(fuzz_dir, exist_ok=True)

    test_cases = [
        (fuzz_dir, []),  # Empty directory
        (fuzz_dir, ["file1.py", "file2.py", "file3.txt"]),  # Mixed files
        ("non_existent_directory", None),  # Non-existent directory
        (None, None),  # None as directory
        ("", None),  # Empty string as directory
    ]

    for i, (dir_path, files) in enumerate(test_cases):
        print(f"\nTest Case {i + 1}:")
        try:
            if dir_path and files is not None:
                for file in files:
                    file_path = os.path.join(dir_path, file)
                    with open(file_path, "w") as f:
                        f.write("print('Hello, world!')")

            result = getPythonCount(dir_path)
            print(f"Input: dir_path='{dir_path}' -> Python File Count: {result}")
        except Exception as e:
            print(f"Input: dir_path='{dir_path}' -> Exception: {e}")

    for file in os.listdir(fuzz_dir):
        os.remove(os.path.join(fuzz_dir, file))
    os.rmdir(fuzz_dir)


# Method 5 - giveTimeStamp from: MLForensics-farzana/FAME-ML/main.py
# Define Time Constants
class constants:
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S" 
    
def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime(constants.TIME_FORMAT) 
  return strToret

# Fuzz Method 5: giveTimeStamp
def fuzz_giveTimeStamp():
    print("\n=== Fuzzing giveTimeStamp ===")

    test_cases = [
        0,  # Unix epoch start
        2**31 - 1,  # Maximum 32-bit integer timestamp (Year 2038 issue)
        2**31,  # After 32-bit integer limit
        -1,  # Negative timestamp (before Unix epoch)
        time.time(),  # Current time
    ]

    for i, mocked_time in enumerate(test_cases):
        print(f"\nTest Case {i + 1}: Mocked time = {mocked_time}")
        with patch("time.time", return_value=mocked_time):
            try:
                result = giveTimeStamp()
                print(f"Output: {result}")
            except Exception as e:
                print(f"Exception: {e}")

if __name__ == "__main__":
    fuzz_getFileLength()
    fuzz_getGeneralStats()
    fuzz_dumpContentIntoFile()
    fuzz_getPythonCount()
    fuzz_giveTimeStamp()