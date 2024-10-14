import argparse

def get_args():

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Find duplicate files in a directory.')
    parser.add_argument('directory', type=str, help='The directory to check for duplicates')
    parser.add_argument('outputname', type=str, help='The name of the output file (without .xlsx extension)')
    parser.add_argument('--sort_key', type=str, nargs='*', 
                        default=['filename', 'size_bytes'],
                        help='Optional sort key(s), default is ["filename", "size_bytes"]')

    args = parser.parse_args()

    # Ensure output name ends with .xlsx
    if not args.outputname.endswith('.xlsx'):
        args.outputname += '.xlsx'

    return args