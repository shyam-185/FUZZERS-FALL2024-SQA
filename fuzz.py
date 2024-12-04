import os
import pandas as pd
import numpy as np
import time
import datetime
from unittest.mock import patch
from myLogger import giveMeLoggingObject

logger = giveMeLoggingObject()

# Fuzzer for question 4b            
# Method 1 - getFileLength from: /MLForensics-farzana/empirical/dataset.stats.py         
def getFileLength(file_):
    return sum(1 for line in open(file_, encoding='latin-1'))

# Fuzzing Method 1: getFileLength
def fuzz_getFileLength():
    logger.info("=== Fuzzing getFileLength ===")
    invalid_cases = [
        "non_existent_file.txt", # File does not exist in dir
        None, # None as input
        "", # Emprty string as input
    ]
    for i, file_ in enumerate(invalid_cases):
        try:
            result = getFileLength(file_)
            logger.info(f"Test Case {i + 1}: Input={file_}, Lines={result}")
        except Exception as e:
            logger.error(f"Test Case {i + 1}: Input={file_}, Exception={e}")

# Method 2 getGeneralStats from: /MLForensics-farzana/empirical/dataset.stats.py
# getAllFileCount needed for gotGeneralStats
def getAllFileCount(df_):
    tot_fil_size = 0
    file_names_ = np.unique(df_['FILE_FULL_PATH'].tolist())
    for file_ in file_names_:
        tot_fil_size += getFileLength(file_)
    return tot_fil_size, len(file_names_)

def getGeneralStats(all_dataset_list):
    all_repos = [] 
    for result_file in all_dataset_list:
        res_df = pd.read_csv(result_file)
        file_size, file_count = getAllFileCount(res_df)
        logger.debug(f"File Size={file_size}, File Count={file_count}")
        return file_size, file_count
    
# Fuzz Method 2: getGeneralStats
def fuzz_getGeneralStats():
    logger.info("=== Fuzzing getGeneralStats ===")
    temp_dir = "test_datasets"
    if not os.path.exists(temp_dir):
        logger.error(f"Directory '{temp_dir}' does not exist.")
        return
    test_cases = [os.path.join(temp_dir, file_name) for file_name in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, file_name))]
    for i, dataset_list in enumerate([[file] for file in test_cases] + [test_cases]):
        try:
            getGeneralStats(dataset_list)
            logger.info(f"Test Case {i + 1}: Input={dataset_list} - Success")
        except Exception as e:
            logger.error(f"Test Case {i + 1}: Input={dataset_list}, Exception={e}")

# Method 3 - dumpContentIntoFile from: MLForensics-farzana/mining/git.repo.miner.py
def dumpContentIntoFile(strP, fileP):
    with open(fileP, 'w') as fileToWrite:
        fileToWrite.write(strP)
    return str(os.stat(fileP).st_size)

# Fuzz Method 3: get_dumpContentInfoFile
def fuzz_dumpContentIntoFile():
    logger.info("=== Fuzzing dumpContentIntoFile ===")
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
        try:
            file_path = os.path.join(fuzz_dir, file_name)
            if not file_name:
                raise ValueError("File name cannot be empty.")
            result = dumpContentIntoFile(content, file_path)
            logger.info(f"Test Case {i + 1}: content={content}, file_path={file_path}, Size={result} bytes")
        except Exception as e:
            logger.error(f"Test Case {i + 1}: content={content}, file_path={file_name}, Exception={e}")
    for file in os.listdir(fuzz_dir):
        os.remove(os.path.join(fuzz_dir, file))
    os.rmdir(fuzz_dir)

# Method 4 - getPythonCount from: MLForensics-farzana/mining/git.repo.miner.py
# Removed 'full_path_file = os.path.join(root_, file_)'
def getPythonCount(path2dir):
    usageCount = 0
    for root_, _, filenames in os.walk(path2dir):
        usageCount += sum(1 for file_ in filenames if file_.endswith('py'))
    return usageCount

# Fuzz Method 4: getPythonCount
def fuzz_getPythonCount():
    logger.info("=== Fuzzing getPythonCount ===")
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
        try:
            if dir_path and files:
                for file in files:
                    with open(os.path.join(dir_path, file), "w") as f:
                        f.write("print('Hello, world!')")
            result = getPythonCount(dir_path)
            logger.info(f"Test Case {i + 1}: dir_path={dir_path}, Python File Count={result}")
        except Exception as e:
            logger.error(f"Test Case {i + 1}: dir_path={dir_path}, Exception={e}")
    for file in os.listdir(fuzz_dir):
        os.remove(os.path.join(fuzz_dir, file))
    os.rmdir(fuzz_dir)

# Method 5 - giveTimeStamp from: MLForensics-farzana/FAME-ML/main.py
# Define Time Constants
class constants:
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def giveTimeStamp():
    tsObj = time.time()
    return datetime.datetime.fromtimestamp(tsObj).strftime(constants.TIME_FORMAT)

# Fuzz Method 5: giveTimeStamp
def fuzz_giveTimeStamp():
    logger.info("=== Fuzzing giveTimeStamp ===")
    test_cases = [
        0,  # Unix epoch start
        2**31 - 1,  # Maximum 32-bit integer timestamp (Year 2038 issue)
        2**31,  # After 32-bit integer limit
        -1,  # Negative timestamp (before Unix epoch)
        time.time(),  # Current time
    ]
    for i, mocked_time in enumerate(test_cases):
        with patch("time.time", return_value=mocked_time):
            try:
                result = giveTimeStamp()
                logger.info(f"Test Case {i + 1}: Mocked time={mocked_time}, Output={result}")
            except Exception as e:
                logger.error(f"Test Case {i + 1}: Mocked time={mocked_time}, Exception={e}")

if __name__ == "__main__":
    fuzz_getFileLength()
    fuzz_getGeneralStats()
    fuzz_dumpContentIntoFile()
    fuzz_getPythonCount()
    fuzz_giveTimeStamp()
