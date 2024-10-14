import os
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def get_ignore_patterns():

    ignore_patterns = [
        r'/.git/',
        r'/venv/',
        r'/\.DS_Store$',
        r'/\.Rhistory',
        r'/\.flake8',
        r'/\.git',
        r'/\.github',
        r'/\.icon.png.meta',

    ]
    logging.debug(f"Loaded ignore patterns: {ignore_patterns}")

    # Combine files to ingore into single regex
    combined_ignore_pattern = '|'.join(ignore_patterns)
    return combined_ignore_pattern


def get_file_info(directory, sort_key):
    file_info_list = []

    def recursive_search(current_dir):
        logging.debug(f"Current directory: {current_dir}")

        for entry in os.scandir(current_dir):
            if entry.is_file():
                file_size_bytes = entry.stat().st_size
                file_size_mb = file_size_bytes / (1024 * 1024)
                file_size_gb = file_size_mb / 1024
                file_info = {
                    'type': 'file',
                    'filename': entry.name,
                    'full_path': entry.path,
                    'size_bytes': file_size_bytes,
                    'size_mb': file_size_mb,
                    'size_gb': file_size_gb
                }
                file_info_list.append(file_info)
            elif entry.is_dir():
                file_info = {
                    'type': 'directory',
                    'filename': entry.name,
                    'full_path': entry.path,
                    'size_bytes': None,
                    'size_mb': None,
                    'size_gb': None
                }
                file_info_list.append(file_info)
                recursive_search(entry.path)
    
    logging.info(f"Start recursive search of directory: '{directory}")
    recursive_search(directory)
    logging.info("Finished recursive search")

    # Create dataframe
    df = pd.DataFrame(file_info_list)

    # Sort dataframe
    df.sort_values(by=sort_key)
    logging.info(f"Shape of 'file info' dataframe: {df.shape}")

    return df


def get_file_dups(df, sort_key, ignore_files=True):

    logging.info(f"Shape of input df: {df.shape}")
    # Get files (i.e. exclude directories)
    df_files = df[df.type == 'file'].copy()
    logging.info(f"Shape of input df (files only): {df_files.shape}")

    if ignore_files:
        logging.info(f"Excluding files/directories that match ignore patterns")
        # Exclude files/folders to ignore
        ignore_pattern = get_ignore_patterns()
        df_files = df_files[~df_files['full_path'].str.contains(ignore_pattern, regex=True)]
        logging.info(f"New shape of df: {df_files.shape}")

    # Find the duplicates on sort key
    df_files_dups = df_files[df_files.duplicated(sort_key, keep=False)].sort_values(sort_key)
    df_files_dups.sort_values(sort_key)
    logging.info(f"Shape of duplicates files: {df_files_dups.shape}")

    # Create column of 'match group'
    df_files_dups['match_group'] = df_files_dups[sort_key].astype(str).agg('-'.join, axis=1)
    df_files_dups = df_files_dups.sort_values('match_group')

    # Get number of dups in each group
    logging.info(f"Calculate number of duplicates per group")
    dups_num = df_files_dups.groupby('match_group').size()
    df_files_dups['num_dups'] = df_files_dups['match_group'].map(dups_num)

    return df_files_dups
