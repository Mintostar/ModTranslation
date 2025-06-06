import json
import os
import googletrans
from googletrans import Translator
import time
from tqdm import tqdm
from datetime import datetime
import readline  # 追加: readlineモジュールをインポート

# Google翻訳のインスタンス作成
translator = Translator()

# JSONファイルを読み込む関数
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# JSON形式と構造の検証
def is_valid_json(file_path):
    """
    ファイルが有効なJSON形式かつ構造が正しいかを判定する。

    Args:
        file_path (str): チェックするファイルのパス。

    Returns:
        bool: 有効な場合はTrue、無効な場合はFalse。
    """
    if not os.path.exists(file_path):
        print(f"ファイルが見つかりません: {file_path}")
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # JSONデータが辞書形式またはリスト形式であることを確認
        if isinstance(data, dict) and bool(data):  # 空の辞書ではない
            return True
        elif isinstance(data, list) and bool(data):  # 空のリストではない
            return True
        else:
            print(f"JSON形式ですが、構造が無効です: {file_path}")
            return False
    except json.JSONDecodeError as e:
        print(f"JSON形式ではありません: {e}")
        return False
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False

# 翻訳対象部分を翻訳し、そのまま返す
def translate_text(text, retries=3):
    # 空文字列や短すぎる値をスキップ
    if not text or len(text.strip()) <= 3:
        return text, None  # 翻訳せずにそのまま返す

    # 残りの処理はそのまま
    cleaned_text = text.strip('"').strip(',')
    for attempt in range(retries):
        try:
            translated = translator.translate(cleaned_text, src='en', dest='ja')
            return translated.text, None
        except googletrans.TranslatorError as e:
            print(f"翻訳エラー: {e}, 再試行中... ({attempt + 1}/{retries})")
            time.sleep(2)
        except Exception as e:
            print(f"予期しないエラー: {e}")
            break
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
    success_logs = {
        "success": [],
        "failure": []
    }  # 成功したログを保持するリスト
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
        timestamp_now = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 翻訳成功
        if error_message is None:
            success_logs["success"].append({
                "timestamp": timestamp_now,
                "key": key,
                "original_text": value,
                "translated_text": translated_value,
            })
            merged_data[key] = translated_value
        else:
            # 翻訳失敗
            errors.append({
                "timestamp": timestamp_now,
                "key": key,
                "original_text": value,
                "error_message": error_message,
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

# ファイルパスの補完機能を追加する関数
def autocomplete_file_path(prompt, base_dir='data'):
    """
    data/ディレクトリ以下のファイルとサブディレクトリの補完を提供する
    """
    def completer(text, state):
        # base_dir（デフォルトはdata）以下のファイルを補完候補にする
        directory = os.path.join(base_dir, '')  # base_dirの絶対パスを取得
        file_list = []

        if os.path.exists(directory):
            file_list = [x for x in os.listdir(directory) if x.startswith(text)]

        return [x for x in file_list][state]

    readline.set_completer(completer)
    readline.parse_and_bind('tab: complete')
    return input(prompt)

# メインの処理
def main():
    input_file = autocomplete_file_path("翻訳元のファイルのパスを指定してください（data/以下のファイル）：")  # 補完機能を呼び出し
    output_file = "ja_jp.json"

    # JSON形式と構造を検証
    if not is_valid_json(input_file):
        print("無効なJSONファイルです。処理を終了します。")
        return

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
