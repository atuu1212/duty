#! /bin/bash

set -eu

function catch {
    echo Catch
}
function finally {
    echo Finally
}
trap catch ERR
trap finally EXIT

/usr/bin/python /home/radtec/src/file_upload_dropbox.py -d duty.xlsx

echo "ファイルのダウンロードが完了しました"

/usr/bin/python /home/radtec/src/A_shift_record_script.py
echo "ファイルのA勤務追記が完了しました"

/usr/bin/python /home/radtec/src/file_upload_dropbox.py -u duty_A_shift_add.xlsx
echo "ファイルのアップロードが完了しました"
