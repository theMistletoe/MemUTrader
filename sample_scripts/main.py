import requests

API_KEY = "mu_NvuKO_RzIPGJ_cNM1CZxPwuSZpeZkruT9Tp7L9NpfIPL76AVcJgm-jrJp3HWNJzy0gcYRdUKod_OgDXHZtY9QB8hbwemIM9Xb_7R2Q"
BASE_URL = "https://api.memu.so"

# Prepare the conversation (minimum 3 messages required)
payload = {
    "conversation": [
        {"role": "user", "content": "最近の米ドル円の動向について教えてください。"},
        {"role": "assistant", "content": "現在、米ドル円は約150円前後で推移しており、米国の利上げ継続観測と日銀の金融政策が注目されています。"},
        {"role": "user", "content": "今後の見通しはどうですか？"},
        {"role": "assistant", "content": "今後も米国の経済指標や日銀の政策修正のタイミングによって、為替相場は大きく変動する可能性があります。"},
        {"role": "user", "content": "投資に関するアドバイスはありますか？"},
        {"role": "assistant", "content": "為替変動リスクを考慮し、分散投資や適切なヘッジ戦略を取ることが重要です。専門家の意見も参考にしてください。"},
        {"role": "user", "content": "USD/JPYは、いま「大きな流れはドル高・円安寄り、でも一方向に突っ走りにくい」みたいな空気感で、たとえば日本銀行が公表する2月6日（JST）のスポットは9:00で156.79–82、17:00で156.88–90、日中レンジも156.56–157.06あたりに収まっていることから「荒れてないように見える日でも、じわっと上（＝円安）を試しやすい地合い」が続いていると見やすく、その背景としてはFOMCが1月の声明で政策金利（FF金利）の誘導目標を3.50%–3.75%に維持している一方（[1]）、日銀側は政策運営のガイドラインとして翌日物金利を0.75%程度にする方針を示しており（[2]）、この金利差がある限り「円を持つよりドルを持ったほうが金利的に得」という力が残ってUSD/JPYは下がりにくい（=円高が続きにくい）土台になりやすいのだけど、同時にロイター報道では日銀内で「インフレ対応が遅れるリスク」への意識や追加利上げの必要性が議論されているトーンも出ていて（[3]）、市場が「次の利上げが早まるかも」と思い始めると円は材料を得て反発しやすく、つまり今は“円安トレンド”と“円の戻りやすさ”が同居しがちな局面であり、円安が進むと必ず出てくる「介入ある？」問題についても財務省が公表している12/29/2025〜1/28/2026の為替介入実績が0円であることから（[4]）「いつでも来る」ではなく“ある水準”と“スピード”が揃ったときに警戒が跳ねるタイプと捉えるのが実務的で、今後のチェックポイントとしては米金利の方向感（FRB高官発言などで「利下げの余地はあるがデータ次第」という温度感が見え、期待が揺れるたびにドルが振れやすい）（[5]）、日銀の“賃金と物価”の確信度（追加利上げのタイミング観測が前倒しになれば円は戻りやすい）（[3]）、そして株式や地政学リスクを含むリスクセンチメント（不安定化すると円買いが入りやすいが金利差が強いと戻りは限定的になりがち）で、まとめると2月6日時点でレートは156円台後半中心、構造的には金利差でドル優位が残る一方で日銀の追加利上げ観測が出るたびに円が戻る“綱引き”が続きやすく（[1][2][3]）、介入は「いつ来るか」より「急な動きが出たか」で警戒が強まりやすい（直近の公表期間は実績ゼロ）という整理になります（[4]）。"}
    ],
    "user_id": "user_B",
    "agent_id": "agent_USD/JPY"
}

# Submit the memorization task
response = requests.post(
    f"{BASE_URL}/api/v3/memory/memorize",
    json=payload,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
)

result = response.json()
print(f"Status Code: {response.status_code}")
print(f"Response: {result}")

if response.status_code == 200:
    task_id = result.get("task_id")
    print(f"Task submitted: {task_id}")
else:
    print("Error submitting task.")