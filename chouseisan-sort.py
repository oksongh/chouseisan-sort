import pandas as pd
import argparse
import pathlib
import io
import sys

# 調整さんが使う丸バツ三角の定数
class chouseisan_mark:
    maru = "◯"
    batu = "×"
    sankaku = "△"
    marks = [maru, sankaku, batu]


def required_query(user: list[str]) -> str:
    """必須の参加者が全員出席できる日程だけ抽出し、dfを更新"""

    query = ""
    for i, v in enumerate(user):
        query += "{} == '{}'".format(v, chouseisan_mark.maru)

        if i < len(user) - 1:
            query += " and "
    return query


def append_count_mark_column(df: pd.DataFrame):
    """各行の◯×△の数をカラムとして追加"""
    for mark in chouseisan_mark.marks:
        markcounts: list[int] = []
        for l in df.values:
            c = 0
            for v in l:
                if v == mark:
                    c += 1
            markcounts.append(c)
        df[mark] = markcounts


def format_csv(file: io.TextIOWrapper) -> tuple[io.TextIOWrapper, str]:

    """
    調整さんcsvの最初についているコメント等を除く処理。
    行をカンマで区切って得たリストの最初の要素が"日程"か"Schedule"になるまで行を捨てたファイルと"日程"か"Schedule"を返す。
    """

    date_column_name = ["日程", "Schedule"]  # 最初のカラム名

    dispose_line = 0
    found = False
    localed_date = ""

    while not found:
        line = f.readline()
        s = line.split(",")[0]
        for ss in date_column_name:
            if s == ss:
                # f.seek(line., os.see)
                found = True
                localed_date = ss
                break
        dispose_line += 1

    file.seek(0)
    # dispose_line行にカラム名がある
    for _ in range(dispose_line - 1):
        file.readline()
    return file, localed_date


def args_parse():
    """コマンドライン引数の設定"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="file path", type=pathlib.Path)
    parser.add_argument(
        "-r", "--required", nargs="*", help="required participants", type=str
    )
    parser.add_argument("-o", "--output", help="output csv file", type=pathlib.Path)
    return parser.parse_args()


if __name__ == "__main__":
    args = args_parse()

    path: pathlib.Path = args.path
    required_user: list[str] | None = args.required
    output_file: pathlib.Path | None = args.output

    localed_date = ""
    df = pd.DataFrame()
    with open(path) as f:
        f, localed_date = format_csv(f)
        df = pd.read_csv(f)

    # コメントの行(最後)を削除
    df.drop(index=len(df.index) - 1, inplace=True)

    if required_user is not None:
        try:
            df.query(required_query(required_user), inplace=True)
        except pd.errors.UndefinedVariableError as e:
            print(e)
            sys.exit(1)

    append_count_mark_column(df)
    df.sort_values(by=[chouseisan_mark.maru, localed_date], inplace=True)

    # ...のような省略なしで表示
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    # カラム途中で改行なし
    pd.set_option("display.width", None)
    print(str(df))

    if output_file is not None:
        df.to_csv(output_file)
