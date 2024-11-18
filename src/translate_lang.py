import json
import os
import googletrans
from googletrans import Translator
import time
from datetime import datetime  # 日時を扱うライブラリをインポート
from tqdm import tqdm  # tqdmライブラリをインポート

# Google翻訳のインスタンス作成
translator = Translator()

# 現在のタイムスタンプを取得する関数
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# JSONファイルを読み込む関数
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 翻訳対象部分を翻訳し、そのまま返す
def translate_text(text, retries=3):
    # 余分なエスケープやクオーテーションを除去
    cleaned_text = text.strip('"').strip(',')

    # 翻訳をリトライ
    for attempt in range(retries):
        try:
            translated = translator.translate(cleaned_text, src='en', dest='ja')
            return translated.text  # 成功したら翻訳結果を返す
        except googletrans.TranslatorError as e:
            print(f"翻訳エラー: {e}, 再試行中... ({attempt + 1}/{retries})")
            time.sleep(2)  # 再試行前に少し待機
        except Exception as e:
            print(f"予期しないエラー: {e}")
            break
    # すべてのリトライで失敗した場合はエラーメッセージを返す
    return f"翻訳失敗: {text}"

# 翻訳後のデータを結合
def merge_key_value(split_data):
    merged_data = {}
    errors = []  # エラーメッセージを保持するリスト
    logs = []  # 翻訳状況ログを保持するリスト
    total_items = len(split_data)

    # tqdmで進捗バーを表示
    for idx, (key, value) in enumerate(tqdm(split_data.items(), desc="翻訳中", total=total_items, ncols=100)):
        translated_value = translate_text(value)
        timestamp = get_timestamp()  # タイムスタンプを取得
        if translated_value.startswith("翻訳失敗"):  # 翻訳に失敗した場合
            errors.append(f"[{timestamp}] キー: {key}, 値: {value}")
        merged_data[key] = translated_value
        logs.append(f"[{timestamp}] [{idx + 1}/{total_items}] {key}: {value} -> {translated_value}")

    # ログファイルを保存
    save_log(logs, "translation_log.txt")
    save_log(errors, "error_log.txt")

    return merged_data, errors

# ログを保存する関数
def save_log(log_data, log_file):
    if not os.path.exists('logs'):
        os.makedirs('logs')  # logsディレクトリが存在しない場合は作成
    log_path = os.path.join('logs', log_file)
    with open(log_path, 'w', encoding='utf-8') as file:
        file.write(f"ログ作成日時: {get_timestamp()}\n")  # ログファイル冒頭にタイムスタンプを追加
        file.write('\n'.join(log_data))

# 結果を新しいJSONファイルに保存
def save_to_json(merged_data, output_file):
    # outputディレクトリが存在しない場合は作成
    if not os.path.exists('output'):
        os.makedirs('output')

    # ファイルパスをoutputディレクトリに設定
    output_path = os.path.join('output', output_file)

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, ensure_ascii=False, indent=4)

# JSONのキーと値を分割
def split_key_value(json_data):
    split_data = {}
    for key, value in json_data.items():
        split_data[key] = value
    return split_data

# エラーログを表示
def display_errors(errors):
    if errors:
        print("\n翻訳に失敗した項目:")
        for error in errors:
            print(error)
    else:
        print("すべての翻訳が成功しました。")

# メインの処理
def main():
    print(f"翻訳開始: {get_timestamp()}")  # 翻訳開始時刻を表示
    input_file = input("翻訳元のファイルのパスを指定してください：")
    output_file = "ja_jp.json"

    # JSONファイルを読み込む
    json_data = load_json(input_file)

    # JSONを分割
    split_data = split_key_value(json_data)

    # 翻訳後のJSONを生成
    merged_data, errors = merge_key_value(split_data)

    # 結果をja_jp.jsonに保存
    save_to_json(merged_data, output_file)
    print(f"翻訳が完了しました。{output_file}に保存されました。")

    # 翻訳終了時刻を表示
    print(f"翻訳終了: {get_timestamp()}")

    # エラーメッセージを表示
    display_errors(errors)

# プログラムの実行
if __name__ == "__main__":
    main()
