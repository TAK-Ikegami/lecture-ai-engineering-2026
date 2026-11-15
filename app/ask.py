"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(model=MODEL, contents=question)

    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage else "不明"
    output_tokens = usage.candidates_token_count if usage else "不明"
    print(f"[usage] 入力トークン数: {input_tokens}, 出力トークン数: {output_tokens}")

    return response.text

def print_usage(response) -> None:
    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage else "不明"
    output_tokens = usage.candidates_token_count if usage else "不明"

    print(
        f"[usage] 入力トークン数: {input_tokens}, "
        f"出力トークン数: {output_tokens}"
    )

def chat() -> None:
    """会話履歴を保持して、繰り返し質問する"""
    client = genai.Client(api_key=get_api_key())
    session = client.chats.create(model=MODEL)

    print(f"[model] {MODEL}")
    print("質問を入力してください。終了するには exit または quit を入力します。")

    while True:
        question = input("\n質問: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("終了します。")
            break

        if not question:
            print("質問が空です。")
            continue

        response = session.send_message(question)

        print_usage(response)
        print(f"\n[回答]\n{response.text}")


def main() -> None:
    parser = argparse.ArgumentParser(description="LLMに質問する")
    parser.add_argument("question", nargs="?", help="質問内容を記憶しない")
    parser.add_argument("--chat", action="store_true", help="会話モードで質問する")
    args = parser.parse_args()


    try:
        if args.chat:
            chat()
        else:
            question = args.question or DEFAULT_QUESTION
            print(f"[model] {MODEL}")
            print(f"[質問] {question}\n")
            print(ask(question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
