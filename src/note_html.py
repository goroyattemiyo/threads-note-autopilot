"""
Markdown → note互換HTML 変換スクリプト
drafts/ 内の .md ファイルを note エディタにコピペ可能な HTML に変換
出力先: drafts/html/
"""

import os
import sys
import glob
import markdown


def convert_md_to_note_html(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html = markdown.markdown(
        md_text,
        extensions=["extra", "nl2br", "sane_lists"],
    )

    html = html.replace("<h1>", "<h2>").replace("</h1>", "</h2>")
    html = html.replace("<hr />", "<p>---</p>")
    html = html.replace("<hr>", "<p>---</p>")

    return html


def main():
    drafts_dir = os.path.join(os.path.dirname(__file__), "..", "drafts")
    output_dir = os.path.join(drafts_dir, "html")
    os.makedirs(output_dir, exist_ok=True)

    if len(sys.argv) > 1:
        md_files = [os.path.join(drafts_dir, sys.argv[1])]
    else:
        md_files = glob.glob(os.path.join(drafts_dir, "*.md"))

    if not md_files:
        print("変換対象の .md ファイルがありません")
        print(f"  確認先: {os.path.abspath(drafts_dir)}")
        sys.exit(1)

    for md_path in md_files:
        if not os.path.exists(md_path):
            print(f"ファイルが見つかりません: {md_path}")
            continue

        filename = os.path.splitext(os.path.basename(md_path))[0]
        html = convert_md_to_note_html(md_path)

        html_path = os.path.join(output_dir, f"{filename}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"OK: {os.path.basename(md_path)} -> html/{filename}.html")

    print(f"\n完了: {len(md_files)} 件変換")
    print(f"出力先: {os.path.abspath(output_dir)}")
    print("\n使い方: HTMLファイルを開く -> 全選択コピー -> noteエディタに貼り付け")


if __name__ == "__main__":
    main()
