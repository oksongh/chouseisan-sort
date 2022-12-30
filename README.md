# chouseisan-sort

調整さん(https://chouseisan.com/)で出力したcsvファイルを○の数でソートします。

## 環境 enviroment

python3

## 使い方 usage

```bash
python chouseisan-sort.py chouseisan.csv
```

```bash
python chouseisan-sort.py chouseisan.csv -r 絶対参加する人
```
-rで絶対に参加する人を指定します。(指定された人が○の日程だけでソート)

## コマンドライン引数
usage: chouseisan-sort.py [-h] [-r [REQUIRED ...]] [-o OUTPUT] path

positional arguments:
  path                  file path

options:
  -h, --help            show this help message and exit
  -r [REQUIRED ...], --required [REQUIRED ...]
                        required participants
  -o OUTPUT, --output OUTPUT
                        output csv file


