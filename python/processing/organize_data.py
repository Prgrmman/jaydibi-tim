"""
Small utility script to rename all the datasets in standard way with incremental value.
This probably doesn't need to be in the GitHub
"""

import os
import shutil

def __rename_files(dataset_dir):
    """For each dice class data directory, renames all the files to have simple incremental name"""
    dice_dirs = [os.path.join(dataset_dir, data) for data in os.listdir(dataset_dir)]
    for data in dice_dirs:
        all_files = os.listdir(data)
        for index, file_name in enumerate(all_files):
            new_name = "{:03d}".format(index) + os.path.splitext(file_name)[1]
            os.rename(os.path.join(data, file_name), os.path.join(data, new_name))

def restructure_dataset(data_dir):
    """Restructures entire dice data set to have simple incrementing file names in each directory"""
    if not os.path.exists(data_dir + '_cpy'):
        shutil.copytree(data_dir, data_dir + '_cpy')

    for directory in os.listdir(data_dir):
        print("Restructuring data dir:", directory)
        __rename_files(os.path.join(data_dir, directory))

if __name__ == '__main__':
    restructure_dataset('data')
