#! ~anaconda3/envs/python.exe
import dropbox
from configparser import ConfigParser
import argparse, os


def get_args():
    """コマンドライン引数とその説明
    Returns:
        List: 引数のパースオブジェクト
    """
    psr = argparse.ArgumentParser(description='Upload(-u) or Download(-d) file against dropbox.')
    psr.add_argument('-u', '--upload', help='Upload file to Dropbox. ex.) -u UploadFile.txt')
    psr.add_argument('-d', '--download', help='Download file to Dropbox. ex.) -d duty.xlsx')

    return psr.parse_args()


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        dbx = dropbox.Dropbox(self.access_token)
        print("The link to the drop box was successful.")
        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)
            print(f"Upload: {file_from}")

    def download_file(self, file_from):
        dbx = dropbox.Dropbox(self.access_token)
        with open(os.path.basename(file_from), "wb") as f:
            metadata, res = dbx.files_download(path=file_from)
            f.write(res.content)
            print(f"Download {file_from} is succesful!")

def main():
    args = get_args()
    # print(args)
    config = ConfigParser()
    config.read('config.ini')
    dropbox_access_token = config['DROPBOX']['ACCESS_TOKEN']
    transferdata = TransferData(access_token=dropbox_access_token)

    
    if args.upload != None:
        file_from = args.upload
        file_to = '/放射線部/放射線部当直表/' + file_from
        transferdata.upload_file(file_from, file_to)
    
    if args.download != None:
        file_from = '/放射線部/放射線部当直表/' + args.download
        # file_to = '/' + file_from
        transferdata.download_file(file_from)


if __name__ == '__main__':
    main()



