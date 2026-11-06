# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
app.askが一般的な回答だが、app.agentはより正確な回答になっている。
@TAK-Ikegami ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
[model] gemini-3.5-flash-lite
AIE2026の講座における「3レベル」とは、宿題の難易度や取り組み方の構成を指しています。

宿題には以下の3つのレベルが用意されており、受講者はどれか1つに取り組めばその回の宿題完了となります：

1. **基礎**：講義内容の確認
2. **実装**：自分でコードを書く
3. **発展**：調査や試行

※原則として採点は行われません

- `--trace` で見えたツール呼び出し（ツール名と引数）：

@TAK-Ikegami ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent --trace "LoRA とQLoRAの違いは？"
[model] gemini-3.5-flash-lite
LoRAとQLoRAの違いは、ベースモデルの重みをそのまま使うか、量子化してメモリを節約するかにあります。

- **LoRA**
  事前学習済みの重みを固定したまま、更新分（低ランク行列）のみを学習する手法です。学習パラメータを大幅に削減できます。
- **QLoRA**
  LoRAの仕組みに加え、ベースモデルの重みを4ビットなどに**量子化**して読み込むことで、さらにメモリ消費を抑え、より大きなモデルを小さなGPUでも学習できるようにした手法です。

関係する回：第2回

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0007738'), details={'text_prompt_tokens': 1196}, input_text_tokens=1196, input_tokens=1196, output_tokens=166, requests=2, tool_calls=2)

- 1つの質問での LLM 呼び出し回数（`requests`）：2回

- 追加したツールと、docstring に書いた説明：

[search_glossary]
  講座の用語集から用語を検索し、定義と、どの回で扱うかを返す。
  
  AIエンジニアリングの用語や、この講座（AIE2026）に固有の言葉について
  答える前に使うこと。query には調べたい用語を1つだけ入れる（例: "LoRA"）。
  引数: {"query": {"type": "string"}}

[get_lecture_summary]
  指定した回（1始まりの整数）の講義の要点を返す。
  
  「第3回では何を学ぶ？」のように、回の内容や関係を聞かれたときに使う。
  引数: {"lecture": {"type": "integer"}}

[make_quiz]
  指定した回の用語から1つを選び、
  確認問題と答えを返す。
  「第2回の確認問題を出して」のように、
  復習用の問題を求められたときに使う。
  引数: {"lecture": {"type": "integer"}}

@TAK-Ikegami ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent --trace " 第2回の内容から確認問題を1問出して"
[model] gemini-3.5-flash-lite
第2回からの確認問題です！ぜひ挑戦してみてください。

**【確認問題】**
大規模言語モデル（LLM）のファインチューニング手法の一つで、モデルの全パラメータを更新するのではなく、モデルの一部（または追加した低ランク行列）だけを効率的に学習させる手法の総称を何と呼ぶでしょうか？

（ヒント：日本語では「パラメータ効率の良い微調整」などと訳されることがあります）

---
第2回

--- trace ---
[tool call]   make_quiz({'lecture': 2})
[tool return] make_quiz -> None…
[usage] RunUsage(cost=Decimal('0.0005242'), details={'text_prompt_tokens': 814}, input_text_tokens=814, input_tokens=814, output_tokens=112, requests=2, tool_calls=1)
@TAK-Ikegami ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run pytest -q
...........                                                                                               [100%]
11 passed in 4.49s


## 宿題

- 取り組んだレベル：基礎
- やったこと：
- 結果：
- 気づき・疑問：
