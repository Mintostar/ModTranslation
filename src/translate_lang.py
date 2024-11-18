import json
import os
import googletrans
from googletrans import Translator
import time
from tqdm import tqdm
from datetime import datetime  # タイムスタンプ用

# Google翻訳のインスタンス作成
translator = Translator()

# ログディレクトリのパス設定
LOG_DIR = "logs"
TRANSLATION_LOG_DIR = os.path.join(LOG_DIR, "translation_logs")
ERROR_LOG_DIR = os.path.join(LOG_DIR, "error_logs")

# JSONファイルを読み込む関数
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 翻訳対象部分を翻訳し、そのまま返す
def translate_text(text, retries=3):
    cleaned_text = text.strip('"').strip(',')
    for attempt in range(retries):
        try:
            translated = translator.translate(cleaned_text, src='en', dest='ja')
            return translated.text
        except googletrans.TranslatorError as e:
            time.sleep(2)
        except Exception:
            break
    return f"翻訳失敗: {text}"

# JSONのキーと値を分割
def split_key_value(json_data):
    split_data = {}
    for key, value in json_data.items():
        split_data[key] = value
    return split_data

# 翻訳後のデータを結合
def merge_key_value(split_data, translation_log_file, error_log_file):
    merged_data = {}
    errors = []
    total_items = len(split_data)
    for idx, (key, value) in enumerate(tqdm(split_data.items(), desc="翻訳中", total=total_items, ncols=100)):
        translated_value = translate_text(value)
        if translated_value.startswith("翻訳失敗"):
            errors.append(f"キー: {key}, 値: {value}")
        else:
            with open(translation_log_file, 'a', encoding='utf-8') as log:
                log.write(f"{datetime.now()}: キー: {key}, 値: {value} -> {translated_value}\n")
        merged_data[key] = translated_value
    with open(error_log_file, 'a', encoding='utf-8') as log:
        for error in errors:
            log.write(f"{datetime.now()}: {error}\n")
    return merged_data, errors

# 結果を新しいJSONファイルに保存
def save_to_json(merged_data, output_file):
    if not os.path.exists('output'):
        os.makedirs('output')
    output_path = os.path.join('output', output_file)
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, ensure_ascii=False, indent=4)

# ログディレクトリのセットアップ
def setup_log_directories():
    os.makedirs(TRANSLATION_LOG_DIR, exist_ok=True)
    os.makedirs(ERROR_LOG_DIR, exist_ok=True)

# メインの処理
def main():
    input_file = input("翻訳元のファイルのパスを指定してください：")
    output_file = "ja_jp.json"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    translation_log_file = os.path.join(TRANSLATION_LOG_DIR, f"translation_{timestamp}.log")
    error_log_file = os.path.join(ERROR_LOG_DIR, f"error_{timestamp}.log")

    setup_log_directories()
    json_data = load_json(input_file)
    split_data = split_key_value(json_data)
    merged_data, errors = merge_key_value(split_data, translation_log_file, error_log_file)
    save_to_json(merged_data, output_file)
    print(f"翻訳が完了しました。{output_file}に保存されました。")
    if errors:
        print(f"エラーログが {error_log_file} に保存されました。")
    else:
        os.remove(error_log_file)
        print("すべての翻訳が成功しました。エラーログは削除されました。")

if __name__ == "__main__":
    main()
