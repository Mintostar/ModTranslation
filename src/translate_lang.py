import json
import os
import googletrans
from googletrans import Translator
import time
from tqdm import tqdm
from datetime import datetime

# Google翻訳のインスタンス作成
translator = Translator()

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
            return translated.text, None  # 成功したら翻訳結果とエラーメッセージなしを返す
        except googletrans.TranslatorError as e:
            print(f"翻訳エラー: {e}, 再試行中... ({attempt + 1}/{retries})")
            time.sleep(2)  # 再試行前に少し待機
        except Exception as e:
            print(f"予期しないエラー: {e}")
            break
    # すべてのリトライで失敗した場合はエラーメッセージを返す
    return None, f"翻訳失敗: {text}"

# JSONのキーと値を分割し、翻訳部分だけを処理
def split_key_value(json_data):
    split_data = {}
    for key, value in json_data.items():
        split_data[key] = value
    return split_data

# 翻訳後のデータを結合
def merge_key_value(split_data):
    merged_data = {}
    errors = []  # エラーメッセージを保持するリスト
    success_logs = []  # 成功したログを保持するリスト
    total_items = len(split_data)

    # ログ用のディレクトリがなければ作成
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # 現在の時間を取得してログファイル名に使用
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    success_log_path = os.path.join(logs_dir, f"translation_log_{timestamp}.json")
    error_log_path = os.path.join(logs_dir, f"error_log_{timestamp}.json")

    # tqdmで進捗バーを表示
    for idx, (key, value) in enumerate(tqdm(split_data.items(), desc="翻訳中", total=total_items, ncols=100)):
        translated_value, error_message = translate_text(value)

        # 翻訳成功
        if error_message is None:
            success_logs.append({
                "timestamp": timestamp,
                "key": key,
                "original_text": value,
                "translated_text": translated_value,
                "status": "success"
            })
            merged_data[key] = translated_value
        else:
            # 翻訳失敗
            errors.append({
                "timestamp": timestamp,
                "key": key,
                "original_text": value,
                "error_message": error_message,
                "status": "error"
            })

    # 成功ログをファイルに保存
    with open(success_log_path, 'w', encoding='utf-8') as success_file:
        json.dump(success_logs, success_file, ensure_ascii=False, indent=4)

    # エラーログをファイルに保存（エラーがあれば）
    if errors:
        with open(error_log_path, 'w', encoding='utf-8') as error_file:
            json.dump(errors, error_file, ensure_ascii=False, indent=4)

    return merged_data, errors, success_log_path, error_log_path

# 結果を新しいJSONファイルに保存
def save_to_json(merged_data, output_file):
    # outputディレクトリが存在しない場合は作成
    if not os.path.exists('output'):
        os.makedirs('output')

    # ファイルパスをoutputディレクトリに設定
    output_path = os.path.join('output', output_file)

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, ensure_ascii=False, indent=4)

# エラーログを表示
def display_errors(errors, error_log_path):
    if errors:
        print("\n翻訳に失敗した項目:")
        for error in errors:
            print(error)
        print(f"\nエラーログが保存されました: {error_log_path}")
    else:
        print("すべての翻訳が成功しました。")

# メインの処理
def main():
    input_file = input("翻訳元のファイルのパスを指定してください：")
    output_file = "ja_jp.json"

    # JSONファイルを読み込む
    json_data = load_json(input_file)

    # JSONを分割
    split_data = split_key_value(json_data)

    # 翻訳後のJSONを生成
    merged_data, errors, success_log_path, error_log_path = merge_key_value(split_data)

    # 結果をja_jp.jsonに保存
    save_to_json(merged_data, output_file)
    print(f"翻訳が完了しました。{output_file}に保存されました。")

    # エラーメッセージを表示
    display_errors(errors, error_log_path)

    # エラーがない場合はエラーログを削除
    if not errors and os.path.exists(error_log_path):
        os.remove(error_log_path)
        print(f"エラーログが削除されました: {error_log_path}")

# プログラムの実行
if __name__ == "__main__":
    main()
