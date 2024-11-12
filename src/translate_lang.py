import json
import googletrans
from googletrans import Translator

# Google翻訳のインスタンス作成
translator = Translator()

# JSONファイルを読み込む関数
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 翻訳対象部分を翻訳し、そのまま返す
def translate_text(text):
    # 余分なエスケープやクオーテーションを除去
    cleaned_text = text.strip('"').strip(',')
    
    # 翻訳
    translated = translator.translate(cleaned_text, src='en', dest='ja')
    
    # 翻訳後はクオーテーションとカンマを追加せずそのまま返す
    return translated.text

# JSONのキーと値を分割し、翻訳部分だけを処理
def split_key_value(json_data):
    split_data = {}
    for key, value in json_data.items():
        # キーと値を分割し、後で翻訳部分だけを処理
        split_data[key] = value
    return split_data

# 翻訳後のデータを結合
def merge_key_value(split_data):
    merged_data = {}
    for key, value in split_data.items():
        translated_value = translate_text(value)
        merged_data[key] = translated_value
    return merged_data

# 結果を新しいJSONファイルに保存
def save_to_json(merged_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, ensure_ascii=False, indent=4)

# メインの処理
def main():
    input_file = input("翻訳元のファイルのパスを指定してください：")
    output_file = "ja_jp.json"
    
    # JSONファイルを読み込む
    json_data = load_json(input_file)
    
    # JSONを分割
    split_data = split_key_value(json_data)
    
    # 翻訳後のJSONを生成
    merged_data = merge_key_value(split_data)
    
    # 結果をja_jp.jsonに保存
    save_to_json(merged_data, output_file)
    print(f"翻訳が完了しました。{output_file}に保存されました。")

# プログラムの実行
if __name__ == "__main__":
    main()
