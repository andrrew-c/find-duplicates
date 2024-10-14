import logging
from python_scripts.dup_utils import get_file_info, get_file_dups

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Directory to check
directory = '/Users/andrew.craik/Documents'

# For sorting the dataframe
sort_key = ['filename', 'size_bytes']

# Get the file inforation
file_info_df = get_file_info(directory, sort_key=sort_key)

a = get_file_dups(file_info_df, sort_key)
a.to_excel('blah.xlsx')
