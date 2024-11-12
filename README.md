# Minecraft MOD 日本語化ツール

このツールは、MinecraftのMOD用の`.json`ファイルを自動で翻訳するためのプログラムです。Google翻訳APIを利用して、英語のテキストを日本語に翻訳し、翻訳結果を新しいJSONファイルとして保存します。

## 概要

MinecraftのMODファイルに含まれるテキストを日本語化するために、以下のステップを自動化します：

1. 翻訳元となるJSONファイルを指定します。
2. 各キーに対応する英語のテキストをGoogle翻訳APIを用いて日本語に翻訳します。
3. 翻訳されたテキストを新しいJSONファイルに書き込みます。

このツールは個人開発のプロジェクトであり、MinecraftのMOD翻訳作業を効率化することを目的としています。

## 使い方

## 必要なライブラリ

このツールの実行には、以下のライブラリが必要です：

- `googletrans==4.0.0-rc1` (Google翻訳APIを利用するため)

### 仮想環境の設定手順

システム環境に直接パッケージをインストールするのではなく、Pythonの仮想環境を作成してその中でパッケージを管理することをおすすめします。

### Linux / macOS  
<ol>
    <li><b>仮想環境を作成する：</b></li>
    <pre><code>python3 -m venv ./ModTranslation/venv</code></pre>
    <li><b>仮想環境をアクティベートする：</b></li>
    <pre><code>source ./ModTranslation/venv/bin/activate</code></pre>
    <li><b>必要なパッケージをインストールする：</b></li>
    <pre><code>pip install googletrans==4.0.0-rc1</code></pre>
    <li><b>仮想環境を終了する：</b></li>
    <pre><code>deactivate</code></pre>
</ol>

### Windows
<ol>
    <li><b>仮想環境を作成する：</b></li>
    <pre><code>python -m venv C:\path\to\project\venv</code></pre>
    <li><b>仮想環境をアクティベートする：</b></li>
    <pre><code>.\venv\Scripts\activate</code></pre>
    <li><b>必要なパッケージをインストールする：</b></li>
    <pre><code>pip install googletrans==4.0.0-rc1</code></pre>
    <li><b>仮想環境を終了する：</b></li>
    <pre><code>deactivate</code></pre>
</ol>





### 実行方法

1. プログラムをダウンロードします。
2. 翻訳したいMODの言語ファイル（JSON形式）を用意します。
3. プログラムを実行し、翻訳したいファイルのパスを入力します。
4. プログラムは自動で英語のテキストを日本語に翻訳し、結果を`ja_jp.json`という名前のファイルに保存します。

```bash
python translate_mod.py
```
実行後、`ja_jp.json`ファイルが生成され、翻訳結果が書き込まれます。

### 例
入力ファイル(例)：

```
{
    "advancement.create.andesite_alloy": "Sturdier Rocks",
    "advancement.create.andesite_alloy.desc": "Obtain some Andesite Alloy, it creates one of the most important resources."
}
```
翻訳後のファイル（`ja_jp.json`）：

```
{
    "advancement.create.andesite_alloy": "頑丈な岩",
    "advancement.create.andesite_alloy.desc": "いくつかのAndesite合金を入手してください。これは、最も重要なリソースを作成します。"
}
```
### 開発者

このツールは個人開発であり、MinecraftのMOD日本語化作業を効率化するために作成されました。現在、Google翻訳APIを使用して翻訳を行っていますが、他の翻訳エンジンの利用も検討しています。

### ライセンス

このプロジェクトは、個人使用の目的で開発されたものであり、特に商用利用を目的としていません。すべてのコードは自由に使用・改変できますが、商用利用に関しては自己責任でお願いします。

### 注意事項

Google翻訳APIの制限や変更により、翻訳結果が期待通りでない場合があります。
現在、英語から日本語への翻訳に特化しています。他の言語に対応させる場合は、コードの修正が必要です。

### 今後の予定

- 他の翻訳エンジン（DeepLなど）への対応。
- 処理を最適化して、大きいファイルも対応可能に。
- 複数の.langファイルを一括で翻訳する機能の追加。
- Minecraft固有の単語を登録して、より正確な翻訳を。
- GUIの実装
- 翻訳結果のキャッシュ。すでに翻訳されたテキストをキャッシュする機能を追加することで、APIのリクエストを最小に。重複翻訳を避ける。
- 翻訳の進捗を表示。
- 関数のモジュール化。
- より多言語への対応。
- .jarファイルを投げるだけで翻訳までしたい。
- ファイルのパスの保管機能の追加。
