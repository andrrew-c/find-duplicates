import logging
from python_scripts.utils import get_args
from python_scripts.dup_utils import get_file_info, get_file_dups

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    
    # Get user command line args
    args = get_args()
    
    # Directory to check
    #directory = '/Users/andrew.craik/Documents'

    # For sorting the dataframe
    #sort_key = ['filename', 'size_bytes']

    # Get the file inforation
    file_info_df = get_file_info(args.directory,
                                 sort_key=args.sort_key,
                                )

    a = get_file_dups(file_info_df, args.sort_key)
    a.to_excel(args.outputname)
