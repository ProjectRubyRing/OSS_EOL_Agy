import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_excel_report(file_path):
    wb = openpyxl.Workbook()
    
    # -------------------------------------------------------------
    # Palette & Styles (Monotone Base)
    # -------------------------------------------------------------
    FONT_NAME = "Meiryo UI"
    
    # Fonts
    font_title = Font(name=FONT_NAME, size=16, bold=True, color="FFFFFF")
    font_section = Font(name=FONT_NAME, size=12, bold=True, color="FFFFFF")
    font_sub_section = Font(name=FONT_NAME, size=11, bold=True, color="1E293B")
    font_tbl_header = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
    font_tbl_header_dark = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
    font_bold = Font(name=FONT_NAME, size=9.5, bold=True, color="1E293B")
    font_regular = Font(name=FONT_NAME, size=9.5, color="1E293B")
    font_small = Font(name=FONT_NAME, size=8.5, color="475569")
    font_tag_white = Font(name=FONT_NAME, size=9, bold=True, color="FFFFFF")
    font_tag_dark = Font(name=FONT_NAME, size=9, bold=True, color="0F172A")
    
    # Fills (Monotone / Elegant Greys)
    fill_title = PatternFill(fill_type="solid", fgColor="1E293B")       # Dark Charcoal Slate
    fill_section = PatternFill(fill_type="solid", fgColor="334155")     # Deep Slate
    fill_tbl_header = PatternFill(fill_type="solid", fgColor="475569")  # Slate Gray
    fill_tbl_header_sub = PatternFill(fill_type="solid", fgColor="E2E8F0") # Light Soft Gray
    fill_zebra_odd = PatternFill(fill_type="solid", fgColor="F8FAFC")   # Very light off-white
    fill_zebra_even = PatternFill(fill_type="solid", fgColor="FFFFFF")  # Pure White
    fill_card_bg = PatternFill(fill_type="solid", fgColor="F1F5F9")     # Neutral card fill
    fill_alert_tag = PatternFill(fill_type="solid", fgColor="0F172A")   # Pure Dark for Alert/Critical
    fill_warn_tag = PatternFill(fill_type="solid", fgColor="475569")    # Medium Dark for Warn
    fill_ok_tag = PatternFill(fill_type="solid", fgColor="CBD5E1")      # Soft Silver for OK/Supported
    
    # Borders
    border_thin_side = Side(border_style="thin", color="CBD5E1")
    border_medium_side = Side(border_style="medium", color="64748B")
    border_double_bottom = Side(border_style="double", color="334155")
    
    border_cell = Border(left=border_thin_side, right=border_thin_side, top=border_thin_side, bottom=border_thin_side)
    border_header = Border(left=border_thin_side, right=border_thin_side, top=border_medium_side, bottom=border_medium_side)
    border_summary_card = Border(left=border_medium_side, right=border_medium_side, top=border_thin_side, bottom=border_thin_side)
    
    # Alignments
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
    align_top_center = Alignment(horizontal="center", vertical="top", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center")
    
    def apply_row_style(ws, row_idx, font=font_regular, fill=None, alignment=align_left, border=border_cell, height=None):
        if height:
            ws.row_dimensions[row_idx].height = height
        for cell in ws[row_idx]:
            if font: cell.font = font
            if fill: cell.fill = fill
            if alignment: cell.alignment = alignment
            if border: cell.border = border

    def auto_fit_columns(ws, min_widths=None, max_width=65):
        if min_widths is None:
            min_widths = {}
        for col in ws.columns:
            col_letter = get_column_letter(col[0].column)
            max_len = 0
            for cell in col:
                # ignore merged cells in length calc if row is title
                if cell.row in [1, 2]:
                    continue
                val = cell.value
                if val:
                    # handle multiline
                    lines = str(val).split('\n')
                    for line in lines:
                        # rough estimation for Japanese double-width
                        line_len = sum(2 if ord(c) > 127 else 1 for c in line)
                        if line_len > max_len:
                            max_len = line_len
            calc_width = max(max_len + 3, min_widths.get(col_letter, 12))
            ws.column_dimensions[col_letter].width = min(calc_width, max_width)

    # =========================================================================
    # SHEET 1: エグゼクティブサマリー (Executive Summary)
    # =========================================================================
    ws1 = wb.active
    ws1.title = "01_エグゼクティブサマリー"
    ws1.views.sheetView[0].showGridLines = True
    
    # Title Banner
    ws1.merge_cells("A1:I1")
    ws1["A1"] = "【重要報告】OSS製品 EOL（サポート終了）対策および異常・リスク詳細分析レポート"
    ws1["A1"].font = font_title
    ws1["A1"].fill = fill_title
    ws1["A1"].alignment = align_center
    ws1.row_dimensions[1].height = 42

    ws1.merge_cells("A2:I2")
    ws1["A2"] = "対象: reactor-core-3.6.6 / spring-data-commons-3.4.3 / spring-data-redis-3.4.3 / spring-data-keyvalue-3.4.3 ｜ モノトーン経営・技術報告版"
    ws1["A2"].font = font_small
    ws1["A2"].fill = fill_card_bg
    ws1["A2"].alignment = align_center
    ws1.row_dimensions[2].height = 20

    # Section 1 Header
    ws1.merge_cells("A4:I4")
    ws1["A4"] = "1. 対象OSSライブラリのサポート終了（EOL）状況マトリクス"
    ws1["A4"].font = font_section
    ws1["A4"].fill = fill_section
    ws1["A4"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[4].height = 28

    headers_s1 = [
        "No", "ライブラリ名 (JAR)", "グループ / 提供元", "対象Ver", 
        "関連Spring Boot世代", "コミュニティOSS EOL日", "商用サポート終了日", "現在のライフサイクル状態", "脆弱性・リスク水準"
    ]
    ws1.append([]) # row 5 is empty
    ws1.append(headers_s1) # row 6
    apply_row_style(ws1, 6, font=font_tbl_header, fill=fill_tbl_header, alignment=align_center, border=border_header, height=26)

    data_s1_matrix = [
        ["1", "reactor-core-3.6.6.jar", "io.projectreactor", "3.6.6", "Spring Boot 3.3.0", "2025年7月", "2026年7月 (Tanzu)", "OSS EOL（コミュニティ保守終了）", "【重大】ストリーム永久ハング DoS (CVE-2026-47857) 内在"],
        ["2", "spring-data-commons-3.4.3.jar", "org.springframework.data", "3.4.3", "Spring Boot 3.4.3", "2025年12月31日", "2026年12月31日 (Tanzu)", "OSS EOL（コミュニティ保守終了）", "【高リスク】メモリ枯渇 DoS (CVE-2026-41716) 内在"],
        ["3", "spring-data-redis-3.4.3.jar", "org.springframework.data", "3.4.3", "Spring Boot 3.4.3", "2025年12月31日", "2026年12月31日 (Tanzu)", "OSS EOL（コミュニティ保守終了）", "【高リスク】Commons脆弱性継承＋コネクション枯渇リスク"],
        ["4", "spring-data-keyvalue-3.4.3.jar", "org.springframework.data", "3.4.3", "Spring Boot 3.4.3", "2025年12月31日", "2026年12月31日 (Tanzu)", "OSS EOL（コミュニティ保守終了）", "【中リスク】Commons依存・インデックスメモリ保持リスク"]
    ]

    for idx, row in enumerate(data_s1_matrix, start=7):
        ws1.append(row)
        fill_row = fill_zebra_odd if idx % 2 == 1 else fill_zebra_even
        apply_row_style(ws1, idx, font=font_regular, fill=fill_row, alignment=align_center, border=border_cell, height=28)
        ws1[f"B{idx}"].alignment = align_left
        ws1[f"I{idx}"].alignment = align_left
        ws1[f"I{idx}"].font = font_bold

    # Section 2 Header: 異常の内容と重大リスク
    row_sec2 = 12
    ws1.merge_cells(f"A{row_sec2}:I{row_sec2}")
    ws1[f"A{row_sec2}"] = "2. 『異常の内容』の総括：放置による3大システム障害リスク"
    ws1[f"A{row_sec2}"].font = font_section
    ws1[f"A{row_sec2}"].fill = fill_section
    ws1[f"A{row_sec2}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[row_sec2].height = 28

    sec2_headers = ["リスク区分", "異常の具体的な発症メカニズム", "直接的な影響・業務被害", "根本原因となった欠陥", "対象コンポーネント"]
    ws1.cell(row=row_sec2+1, column=1, value="") # row 13 empty
    ws1.append(["リスク区分", "異常の具体的な発症メカニズム", "直接的なシステム障害・業務被害", "根本原因となった欠陥", "影響を受けるOSS"])
    row_sec2_tbl = row_sec2 + 2
    ws1.merge_cells(f"B{row_sec2_tbl}:C{row_sec2_tbl}")
    ws1.merge_cells(f"D{row_sec2_tbl}:E{row_sec2_tbl}")
    ws1.merge_cells(f"F{row_sec2_tbl}:G{row_sec2_tbl}")
    ws1.merge_cells(f"H{row_sec2_tbl}:I{row_sec2_tbl}")
    ws1.cell(row=row_sec2_tbl, column=1, value="リスク区分").alignment = align_center
    ws1.cell(row=row_sec2_tbl, column=2, value="異常の具体的な発症メカニズム").alignment = align_center
    ws1.cell(row=row_sec2_tbl, column=4, value="直接的なシステム障害・業務被害").alignment = align_center
    ws1.cell(row=row_sec2_tbl, column=6, value="根本原因となった設計・実装欠陥").alignment = align_center
    ws1.cell(row=row_sec2_tbl, column=8, value="主要原因OSS").alignment = align_center
    
    for c in range(1, 10):
        cell = ws1.cell(row=row_sec2_tbl, column=c)
        cell.font = font_tbl_header
        cell.fill = fill_tbl_header
        cell.border = border_header
    ws1.row_dimensions[row_sec2_tbl].height = 25

    risks = [
        ("① メモリ枯渇・強制停止\n(Heap Exhaustion OOM)",
         "外部からの悪意あるHTTPリクエストパラメータ（不正なsortや属性名）を処理する際、プロパティ解析結果を無制限に内部キャッシュ（HashMap）へ蓄積し続ける。",
         "JVMヒープ領域が逼迫し、頻繁なFull GC（Stop-the-World）を経てOutOfMemoryErrorでサーバープロセスが強制クラッシュ・停止する。",
         "PropertyPath解析におけるキャッシュサイズ上限および有効期限（TTL/Eviction）の欠落（CVE-2026-41716）",
         "spring-data-commons\n(Redis/KeyValueへ波及)"),
        ("② パイプライン永久凍結\n(Reactive Stream Hang)",
         "長時間のストリーミング処理やBackpressure（流量制御）下でタイムアウト付きウィンドウ/バッファ処理を行う際、内部カウンタのオーバーフローや競合が発生。",
         "エラーログを一切出力しないままリアクティブストリームが沈黙・停止。通信待ちスレッドが解放されず、リクエストが504 Timeoutで永久に詰まる。",
         "Flux.windowTimeout / bufferTimeout における公平背圧（fairBackpressure）計算の整数溢れおよび排他不全（CVE-2026-47857/47863）",
         "reactor-core\n(Lettuce/Redisへ波及)"),
        ("③ 連鎖的コネクション枯渇\n(Cascading Failure)",
         "Reactor Coreのストリーム停止により、Lettuce（Redisドライバ）の非同期レスポンス受取パイプラインが停止。コネクションが返却されなくなる。",
         "Redis接続プールが瞬時に枯渇。後続の通常DB問い合わせやセッション管理、キャッシュ参照がすべてブロッキングされ、サービス全体が全滅する。",
         "非同期ノンブロッキング通信基盤（Reactor）の不全が同期・非同期の境界を超えてインフラ層に伝播するアーキテクチャ上の連鎖特性",
         "reactor-core ×\nspring-data-redis")
    ]

    curr_r = row_sec2_tbl + 1
    for r_title, r_mech, r_imp, r_root, r_oss in risks:
        ws1.merge_cells(f"B{curr_r}:C{curr_r}")
        ws1.merge_cells(f"D{curr_r}:E{curr_r}")
        ws1.merge_cells(f"F{curr_r}:G{curr_r}")
        ws1.merge_cells(f"H{curr_r}:I{curr_r}")
        
        ws1.cell(row=curr_r, column=1, value=r_title).alignment = align_center
        ws1.cell(row=curr_r, column=2, value=r_mech).alignment = align_top_left
        ws1.cell(row=curr_r, column=4, value=r_imp).alignment = align_top_left
        ws1.cell(row=curr_r, column=6, value=r_root).alignment = align_top_left
        ws1.cell(row=curr_r, column=8, value=r_oss).alignment = align_center
        
        fill_curr = fill_zebra_odd if curr_r % 2 == 1 else fill_zebra_even
        for col_idx in range(1, 10):
            c = ws1.cell(row=curr_r, column=col_idx)
            c.font = font_regular
            c.fill = fill_curr
            c.border = border_cell
        ws1.cell(row=curr_r, column=1).font = font_bold
        ws1.row_dimensions[curr_r].height = 55
        curr_r += 1

    # Section 3: 対策方針の比較
    curr_r += 1
    ws1.merge_cells(f"A{curr_r}:I{curr_r}")
    ws1[f"A{curr_r}"] = "3. EOL対策オプションの比較評価と推奨アクション"
    ws1[f"A{curr_r}"].font = font_section
    ws1[f"A{curr_r}"].fill = fill_section
    ws1[f"A{curr_r}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[curr_r].height = 28

    curr_r += 2
    sol_headers = ["対策案", "区分", "推奨度", "工数・難易度", "根本解決度", "メリット", "デメリット・懸念事項", "対象バージョン・対応内容", "備考"]
    for col_idx, h_text in enumerate(sol_headers, start=1):
        c = ws1.cell(row=curr_r, column=col_idx, value=h_text)
        c.font = font_tbl_header
        c.fill = fill_tbl_header
        c.alignment = align_center
        c.border = border_header
    ws1.row_dimensions[curr_r].height = 25

    solutions = [
        ["方針A: Spring Boot一括アップグレード\n（最新OSSサポート版への移行）", "恒久対策", "★★★★★\n【最推奨】", "中〜高\n(2〜4人月)", "完全解決\n(100%)",
         "・OSS無償サポートの継続享受\n・既知の全CVE（メモリ/ハング）を根本解決\n・新機能・Java最新版・性能向上の恩恵",
         "・API変更に伴うコード修正・再テストが必要\n・周辺ライブラリの依存性解決テストが必要",
         "Spring Boot 3.5.x または 4.x へ移行\n(Spring Data 2025.0+, Reactor 3.7+)", "BOM管理による整合性一括担保が必須"],
        ["方針B: マイナー修正版の適用\n（3.4.15+ へのパッチ更新）", "暫定対策", "★★★★☆\n【準推奨】", "低〜中\n(0.5〜1人月)", "高い\n(既知CVE解消)",
         "・既存コードの破壊的変更が極めて少ない\n・短期間・低コストで直近の致命的CVEを解消可能",
         "・3.4系自体のOSS EOL期限が迫っている/過ぎているため再度のアップグレード計画が必要",
         "spring-data-commons 3.4.15+ へ更新\n(Spring Boot 3.4系の最終パッチ適用)", "商用リポジトリまたは個別バックポートの確認要"],
        ["方針C: 商用長期サポート契約\n（Broadcom Tanzu / HeroDevs NES）", "延命対策", "★★★☆☆\n【状況依存】", "極小\n(コード改修無)", "高い\n(CVEパッチ保証)",
         "・アプリケーションコードの変更・再検証が不要\n・現行バイナリの互換性を維持したままCVE修正版を入手",
         "・年間ライセンス保守費用（有償）が発生\n・根本的なレガシー脱却の先送りに過ぎない",
         "Tanzu Spring Commercial Support 契約\nまたは HeroDevs NES for Spring 契約", "大規模システムや年度内予算で即時改修不可の場合に有効"],
        ["方針D: WAF・入力遮断ワークアラウンド\n（脆弱性緩和プロキシ設定）", "応急処置", "★★☆☆☆\n【緊急時のみ】", "極小\n(即日〜数日)", "部分的\n(外部攻撃のみ)",
         "・アプリの再デプロイ不要でWAF/Gateway側で即座に設定可能\n・悪意あるソートパラメータの侵入を水際で防御",
         "・内部バッチや正規リクエストの誤検知リスク\n・Reactor Coreの内部レースコンディション（ハング）は防げない",
         "WAFによる不正プロパティ名正規表現遮断\nController層でのSort/Pageableホワイトリスト制限", "本格改修（方針A/B）が完了するまでの緊急盾として併用"]
    ]

    for sol in solutions:
        curr_r += 1
        ws1.append(sol)
        fill_curr = fill_zebra_odd if curr_r % 2 == 1 else fill_zebra_even
        apply_row_style(ws1, curr_r, font=font_regular, fill=fill_curr, alignment=align_top_left, border=border_cell, height=52)
        ws1.cell(row=curr_r, column=1).alignment = align_center
        ws1.cell(row=curr_r, column=1).font = font_bold
        ws1.cell(row=curr_r, column=2).alignment = align_center
        ws1.cell(row=curr_r, column=3).alignment = align_center
        ws1.cell(row=curr_r, column=3).font = font_bold
        ws1.cell(row=curr_r, column=4).alignment = align_center
        ws1.cell(row=curr_r, column=5).alignment = align_center

    auto_fit_columns(ws1, min_widths={"A": 22, "B": 32, "C": 18, "D": 14, "E": 20, "F": 22, "G": 22, "H": 28, "I": 28})
    ws1.freeze_panes = "A7"

    # =========================================================================
    # SHEET 2: OSS動作原理と誕生背景 (Deep Dive & Mental Model)
    # =========================================================================
    ws2 = wb.create_sheet(title="02_OSS動作原理と誕生背景")
    ws2.views.sheetView[0].showGridLines = True

    # Title
    ws2.merge_cells("A1:G1")
    ws2["A1"] = "4大OSSライブラリの誕生の歴史・必要になった経緯・動作原理・小学生でもわかる動作イメージ"
    ws2["A1"].font = font_title
    ws2["A1"].fill = fill_title
    ws2["A1"].alignment = align_center
    ws2.row_dimensions[1].height = 42

    ws2.merge_cells("A2:G2")
    ws2["A2"] = "技術的本質（アーキテクチャ）と直感的なメタファー（日常の例え）の両輪による完全解説"
    ws2["A2"].font = font_small
    ws2["A2"].fill = fill_card_bg
    ws2["A2"].alignment = align_center
    ws2.row_dimensions[2].height = 20

    oss_details = [
        {
            "name": "1. reactor-core-3.6.6.jar （Project Reactor コアエンジン）",
            "role": "非同期・ノンブロッキング・リアクティブストリーム処理基盤 (Reactive Streams Specification 実装)",
            "history": "【登場の歴史と背景・必要になった経緯】\n"
                       "・従来のJava（Servlet 3.0以前）は『1リクエスト＝1スレッド』を割り当てる同期ブロッキング方式でした。\n"
                       "・スマホの普及やIoT、リアルタイムWebにより同時接続数が数万〜数十万に急増。1スレッドあたり約1MBのスタックメモリを消費するため、数千接続でメモリがパンクし、OSのCPUコンテキストスイッチ負荷でサーバーが沈黙する『C10K問題』に直面しました。\n"
                       "・この危機を打破するため、2013-2015年にNetflix、Pivotal（現VMware/Broadcom）、Lightbendが結集して『Reactive Streams仕様』を策定。少ないスレッド（CPUコア数程度）で大量の通信を非同期に処理し、下流がパンクしないよう流量制御（Backpressure）を行うコア基盤としてProject Reactorが誕生しました。",
            "principle": "【動作原理（アーキテクチャ）】\n"
                         "① Publisher（発行者: Flux/Mono）とSubscriber（購読者）の契約モデル。subscribe()されるまでデータは流れない。\n"
                         "② Backpressure（背圧制御）：従来のPush型（一方的にデータを押し付けて受信側が溢れる）ではなく、Subscriber側が『request(n)』と要求した数だけデータを送るPull-Pushハイブリッド制御。\n"
                         "③ イベントループとスケジューラ：Netty等のノンブロッキングI/Oセレクタと連携し、I/O待ちの間スレッドを決してブロック（停止）させず、コールバックとシグナル（onNext, onError, onComplete）でCPUを限界まで効率活用する。",
            "analogy": "【小学生にもわかる動作イメージ（日常の例え）】\n"
                       "『大繁盛の超人気回転寿司店と、注文ボタンのバケツリレー』\n"
                       "■ 昔のJava（ブロッキング）:\n"
                       "お客さん1人につき、専属のウェイターが1人付きっきりになります。料理人が寿司を握るまでの間、ウェイターは何分間も厨房の前で腕組みしてじーっと待っています（スレッドのブロック）。お客さんが1,000人来たらウェイターも1,000人雇わなければならず、店内が店員だらけで身動きが取れなくなって倒れてしまいます（メモリパンク）。\n"
                       "■ Reactor Core（リアクティブ）:\n"
                       "店員はたったの数人！店員は注文を受けたら厨房にチケットを投げて、すぐ別のお客さんの対応に向かいます。料理ができたらベルが鳴ってサッと運ぶだけ。さらに回転寿司のレーンにお皿を流しすぎないよう、お客さんの手元にある『2皿ちょうだい！』というボタン（Backpressure）が押された分だけ厨房からお寿司が流れてきます。だから絶対にテーブルがお皿で溢れません！"
        },
        {
            "name": "2. spring-data-commons-3.4.3.jar （Spring Data 共通基盤脳）",
            "role": "全Spring Dataモジュール（JPA, Redis, MongoDB, R2DBC等）共通のデータアクセス抽象化・メタデータ解析エンジン",
            "history": "【登場の歴史と背景・必要になった経緯】\n"
                       "・2000年代初頭のJava開発では、データベースへアクセスするためにDAO（Data Access Object）クラスを作り、SQLの発行、コネクションのオープン/クローズ、検索結果からJavaオブジェクトへの詰め替え（Mapping）、ページネーション計算（全件数カウントやOFFSET計算）を毎回手書きしていました。\n"
                       "・この膨大なボイラープレート（定型コード）とコピペミスを根絶するため、Spring Dataプロジェクトが2010年に発足。『インターフェースを宣言するだけで、実行時に実装が自動生成されるRepositoryパターン』が発明されました。\n"
                       "・RDBMSだけでなく、NoSQL（Redis, Mongo等）が登場した際、ページ送り（Pageable）、並び替え（Sort）、監査情報（作成日時・更新者）、エンティティ解析のロジックが重複しないよう、すべての共通脳として切り出されたのが『spring-data-commons』です。",
            "principle": "【動作原理（アーキテクチャ）】\n"
                         "① 動的プロキシとクエリ導出（Query Derivation）：開発者が『findByLastNameAndAge(String name, int age)』と書くだけで、メソッド名を構文解析し、抽象構文木（AST）を構築して実行時クエリに変換する。\n"
                         "② PropertyPath による属性ツリー解決：ドメインクラスのネストされた属性（例: user.address.zipCode）をリフレクションで探索し、高速化のために内部キャッシュ（ConcurrentReferenceHashMap）に保持する。\n"
                         "③ Web引数リゾルバ：Controllerで受け取ったHTTPリクエストパラメータ（?page=1&size=20&sort=name,asc）を解析し、フレームワーク共通の『Pageable』『Sort』オブジェクトへ透過的に自動変換・バインドする。",
            "analogy": "【小学生にもわかる動作イメージ（日常の例え）】\n"
                       "『世界中の本棚を熟知した、万能の通訳兼スーパー図書委員』\n"
                       "■ 昔のJava:\n"
                       "本（データ）を探すとき、紙のノートに毎回『1ページ目から最後のページまで1行ずつ名前を照らし合わせて、見つかったらメモ帳に書き写す』という手順書を自分で1から書く必要がありました。\n"
                       "■ Spring Data Commons:\n"
                       "スーパー図書委員に『山田くんの算数の本をちょうだい！』と一言お願いするだけ。図書委員は言葉を自動で分解（「山田」＋「算数」＋「探す」）して、本棚係（SQL）やロッカー係（Redis）に正確な命令書を作って届けてくれます。さらに『出席番号順に5冊ずつ持ってきて！』という注文も、自動で整理券を作って綺麗に並べ替えて届けてくれます。"
        },
        {
            "name": "3. spring-data-redis-3.4.3.jar （Redis 高度統合フレームワーク）",
            "role": "インメモリKVS（Redis）への接続プール管理、オブジェクト双方向変換、Reactive連携、キャッシュ抽象化",
            "history": "【登場の歴史と背景・必要になった経緯】\n"
                       "・Webサービスのトラフィックが爆発すると、ディスクへの読み書きを行うリレーショナルDB（MySQL/PostgreSQL等）がボトルネックになり、画面の表示速度が劇的に低下しました。\n"
                       "・そこで、すべてのデータをメモリ上に保持しマイクロ秒単位で応答する超高速ストレージ『Redis』がデファクトスタンダードになりました。\n"
                       "・しかし、低レベルなJavaドライバ（JedisやLettuce）を直接触ると、バイナリ（byte[]）へのシリアライズ/デシリアライズ、接続プールの手動管理、分散ロック、Pub/Sub購読の例外処理などを自前で組む必要があり事故が多発しました。\n"
                       "・これをSpringの強力なアノテーション（@Cacheable）やテンプレート（RedisTemplate, ReactiveRedisTemplate）で安全・容易に扱えるようにしたのが『spring-data-redis』です。",
            "principle": "【動作原理（アーキテクチャ）】\n"
                         "① 低レベルドライバ（Lettuce/Jedis）の抽象化：非同期通信ドライバLettuce（Netty＋Reactor Core上で動作）を統合管理し、スレッドセーフなコネクション共有を実現。\n"
                         "② シリアライザ・パイプライン：Javaオブジェクト ⇔ JSON（Jackson2JsonRedisSerializer）や文字列（StringRedisSerializer）への自動相互変換。\n"
                         "③ Redis Repositories（@RedisHash）：RedisのHash構造にオブジェクトを保存しつつ、セカンダリインデックス（キー以外の検索用Set）を自動生成・管理してRepository経由での検索を可能にする。",
            "analogy": "【小学生にもわかる動作イメージ（日常の例え）】\n"
                       "『超特急のハイテク金庫ロボット（高速ロッカー専属オペレーター）』\n"
                       "■ 昔のやり方:\n"
                       "遠くの巨大倉庫（データベース）まで毎回走って荷物を取りに行っていたので、届くまでとても時間がかかっていました。手元に超速ロッカー（Redis）を置いても、ロッカーには暗号の数字（0と1のバイト列）しか入らないため、荷物をバラバラに解体して詰め込み、出すときにまた組み立てる作業が大変でした。\n"
                       "■ Spring Data Redis:\n"
                       "専属の金庫ロボットです。『このお気に入りのゲーム機をロッカーに入れておいて！』と渡すだけで、ロボットが壊れないよう綺麗な箱にパッキング（シリアライズ）して超特急でロッカーにシュッと格納。必要なときは一瞬で箱から取り出して組み立て、元の状態で手渡してくれます。"
        },
        {
            "name": "4. spring-data-keyvalue-3.4.3.jar （Key-Value型データアクセス基盤）",
            "role": "Key-Value型データ構造（Map/Redis等）に対する共通リポジトリ・インデックス管理・クエリ評価SPI",
            "history": "【登場の歴史と背景・必要になった経緯】\n"
                       "・Spring Dataは当初SQL（リレーショナル）を前提に設計されていましたが、NoSQLの台頭により『キー（鍵）』と『バリュー（値）』だけでデータを管理するシンプルなKVS（Key-Value Store）が急増しました。\n"
                       "・KVSはSQLのような柔軟なWHERE句検索やJOINを持たないため、Spring DataのRepositoryパターン（findByAge等）をそのまま適用することが構造上困難でした。\n"
                       "・そこで、Key-Valueモデル専用の共通インターフェース、インメモリでのインデックス管理、SpEL（Spring Expression Language）を用いた条件フィルタリングエンジンを提供するために誕生しました。Spring Data Redis Repositoriesの内部基盤として直接利用されています。",
            "principle": "【動作原理（アーキテクチャ）】\n"
                         "① KeyValueAdapter と KeyValueTemplate：具体的な格納先（RedisやインメモリMap）へのCRUD操作を共通APIとして仲介するアダプタ設計パターン。\n"
                         "② 擬似セカンダリインデックスの維持：キー以外のフィールド検索を実現するため、プロパティ値ごとのSet構造を構築し、対象キーの集合をトラッキングする。\n"
                         "③ TTL（有効期限）イベントの検知：KVS側の有効期限切れ（Expiration）イベントを捕捉し、連動するインデックスのクリーンアップを行う。",
            "analogy": "【小学生にもわかる動作イメージ（日常の例え）】\n"
                       "『名札付きシューズロッカーの帳簿係（キー・バリューのルールブック）』\n"
                       "■ 困りごと:\n"
                       "学校の下駄箱（ロッカー）は『靴箱の番号（キー）』と『中に入っている靴（バリュー）』しか分かりません。『青いスニーカーを履いている子の靴箱はどれ？』と探そうとすると、全部の扉を1個ずつ開けて靴を確認しなければならず、日が暮れてしまいます。\n"
                       "■ spring-data-keyvalue:\n"
                       "頭の良い帳簿係です。靴が入るたびに『青いスニーカー＝12番と25番』とメモ帳（インデックス）に書き留めておきます。だから『青い靴を出して！』と言われたら、ロッカーを全部開けなくても一瞬で12番と25番を開けて靴を取り出せます。"
        }
    ]

    curr_r2 = 4
    for item in oss_details:
        ws2.merge_cells(f"A{curr_r2}:G{curr_r2}")
        ws2[f"A{curr_r2}"] = item["name"]
        ws2[f"A{curr_r2}"].font = font_section
        ws2[f"A{curr_r2}"].fill = fill_section
        ws2[f"A{curr_r2}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws2.row_dimensions[curr_r2].height = 28

        curr_r2 += 1
        ws2.merge_cells(f"A{curr_r2}:B{curr_r2}")
        ws2[f"A{curr_r2}"] = "【役割・主要機能】"
        ws2[f"A{curr_r2}"].font = font_bold
        ws2[f"A{curr_r2}"].fill = fill_tbl_header_sub
        ws2[f"A{curr_r2}"].alignment = align_center

        ws2.merge_cells(f"C{curr_r2}:G{curr_r2}")
        ws2[f"C{curr_r2}"] = item["role"]
        ws2[f"C{curr_r2}"].font = font_bold
        ws2[f"C{curr_r2}"].fill = fill_card_bg
        ws2[f"C{curr_r2}"].alignment = align_left
        ws2.row_dimensions[curr_r2].height = 24

        curr_r2 += 1
        ws2.merge_cells(f"A{curr_r2}:B{curr_r2}")
        ws2[f"A{curr_r2}"] = "誕生の歴史と背景\n（必要になった経緯）"
        ws2[f"A{curr_r2}"].font = font_bold
        ws2[f"A{curr_r2}"].fill = fill_tbl_header_sub
        ws2[f"A{curr_r2}"].alignment = align_center

        ws2.merge_cells(f"C{curr_r2}:G{curr_r2}")
        ws2[f"C{curr_r2}"] = item["history"]
        ws2[f"C{curr_r2}"].font = font_regular
        ws2[f"C{curr_r2}"].fill = fill_zebra_even
        ws2[f"C{curr_r2}"].alignment = align_top_left
        ws2.row_dimensions[curr_r2].height = 95

        curr_r2 += 1
        ws2.merge_cells(f"A{curr_r2}:B{curr_r2}")
        ws2[f"A{curr_r2}"] = "動作原理\n（技術アーキテクチャ）"
        ws2[f"A{curr_r2}"].font = font_bold
        ws2[f"A{curr_r2}"].fill = fill_tbl_header_sub
        ws2[f"A{curr_r2}"].alignment = align_center

        ws2.merge_cells(f"C{curr_r2}:G{curr_r2}")
        ws2[f"C{curr_r2}"] = item["principle"]
        ws2[f"C{curr_r2}"].font = font_regular
        ws2[f"C{curr_r2}"].fill = fill_zebra_odd
        ws2[f"C{curr_r2}"].alignment = align_top_left
        ws2.row_dimensions[curr_r2].height = 85

        curr_r2 += 1
        ws2.merge_cells(f"A{curr_r2}:B{curr_r2}")
        ws2[f"A{curr_r2}"] = "小学生にもわかる\n動作イメージ\n（日常の例え）"
        ws2[f"A{curr_r2}"].font = font_bold
        ws2[f"A{curr_r2}"].fill = fill_tbl_header_sub
        ws2[f"A{curr_r2}"].alignment = align_center

        ws2.merge_cells(f"C{curr_r2}:G{curr_r2}")
        ws2[f"C{curr_r2}"] = item["analogy"]
        ws2[f"C{curr_r2}"].font = font_regular
        ws2[f"C{curr_r2}"].fill = fill_card_bg
        ws2[f"C{curr_r2}"].alignment = align_top_left
        ws2.row_dimensions[curr_r2].height = 145

        # border styling for the block
        for r in range(curr_r2 - 4, curr_r2 + 1):
            for c in range(1, 8):
                ws2.cell(row=r, column=c).border = border_cell

        curr_r2 += 2 # space before next OSS

    auto_fit_columns(ws2, min_widths={"A": 16, "B": 16, "C": 18, "D": 22, "E": 22, "F": 22, "G": 22})
    ws2.freeze_panes = "A4"

    # =========================================================================
    # SHEET 3: 異常・脆弱性メカニズム (In-Depth Technical Failure Analysis)
    # =========================================================================
    ws3 = wb.create_sheet(title="03_異常・脆弱性メカニズム")
    ws3.views.sheetView[0].showGridLines = True

    # Title
    ws3.merge_cells("A1:H1")
    ws3["A1"] = "【異常の詳細】EOLバージョンに潜在する既知の致命的脆弱性メカニズムと連鎖崩壊シナリオ"
    ws3["A1"].font = font_title
    ws3["A1"].fill = fill_title
    ws3["A1"].alignment = align_center
    ws3.row_dimensions[1].height = 42

    ws3.merge_cells("A2:H2")
    ws3["A2"] = "CVE-2026-41716 (メモリ枯渇) / CVE-2026-47857 (ストリーム凍結) / CVE-2026-47863 (競合) / 連鎖的障害の完全追跡"
    ws3["A2"].font = font_small
    ws3["A2"].fill = fill_card_bg
    ws3["A2"].alignment = align_center
    ws3.row_dimensions[2].height = 20

    ws3.merge_cells("A4:H4")
    ws3["A4"] = "1. 対象バージョンに存在する既知の脆弱性（CVE）詳細データ"
    ws3["A4"].font = font_section
    ws3["A4"].fill = fill_section
    ws3["A4"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws3.row_dimensions[4].height = 28

    cve_headers = ["脆弱性識別子\n(CVE / 識別名)", "対象ライブラリ\nおよび影響範囲", "深刻度\n(CVSS v3)", "脆弱性の種別\n(CWE)", "異常の発生トリガー\n(攻撃・発症条件)", "内部での破綻メカニズム\n(根本原因)", "最終的なシステム障害症状", "修正パッチバージョン"]
    ws3.append([]) # row 5 empty
    ws3.append(cve_headers)
    apply_row_style(ws3, 6, font=font_tbl_header, fill=fill_tbl_header, alignment=align_center, border=border_header, height=32)

    cve_data = [
        ["CVE-2026-41716", "spring-data-commons\n(3.4.0 〜 3.4.14)\n※3.4.3は直撃", "High\n(CVSS 7.5)", "CWE-770\n無制限なリソース割当",
         "外部から大量のランダム・無効なプロパティ名を含むHTTPクエリ（?sort=rndXYZ..等）をWebエンドポイントへ送信",
         "PropertyPath解析結果を保持する内部キャッシュ（Map）に上限サイズ（max-size）および破棄ポリシー（LRU/TTL）が存在せず、永久保持される",
         "ヒープ領域枯渇による頻繁なFull GC（Stop-the-World）およびOutOfMemoryError（OOM）でのJVMクラッシュ", "3.4.15+\nまたは 3.5.x+"],
        ["CVE-2026-47857", "reactor-core\n(3.5.0 〜 3.7.19)\n※3.6.6は直撃", "High\n(CVSS 7.5)", "CWE-190\n整数オーバーフロー",
         "Flux.windowTimeout(..., fairBackpressure=true) を用いた長時間稼働ストリームにおいて、下流からの要求数が特定条件に合致",
         "公平背圧（fairBackpressure）を追跡する内部状態インデックス計算で整数ラップアラウンド（桁あふれ）が発生し、内部ステートマシンが異常状態へ遷移",
         "エラーもスローされずストリームが永久に停止（ハング）。後続のデータ送受信が完全に凍結しリクエストが沈黙", "3.6.17+ (商用)\nまたは 3.7.20+"],
        ["CVE-2026-47863", "reactor-core\n(3.5.0 〜 3.7.19)\n※3.6.6は直撃", "Medium\n(CVSS 5.9)", "CWE-362\n競合状態 (Race Condition)",
         "Flux.bufferTimeout(..., fairBackpressure=true) において、バッファのフラッシュ動作と新たな上流データ到達が完全同時に発生",
         "バッファのフラッシュ処理と新規要素追加の間でスレッド排他制御の隙間が生じ、タイムアウトスケジュールが消失して未フラッシュデータが孤立",
         "データがバッファ内に取り残され、後続のタイマーが発火しないためパイプラインがデッドロック状態に陥る", "3.6.17+ (商用)\nまたは 3.7.20+"],
        ["CVE-2026-41711", "spring-data-commons\n(3.4.0 〜 3.4.14)\n※3.4.3は直撃", "Medium\n(CVSS 5.3)", "CWE-674\n無制御な再帰呼び出し",
         "極端に深くネストされたプロパティ名（a.b.c.d.e....）を持つSortパラメータや投影（Projection）クエリの受信",
         "PropertyPath.from() 内の再帰探索処理において、探索深度（Max Depth）のバリデーションチェックが欠落",
         "Javaスレッドスタック領域が枯渇し、StackOverflowError が発生して当該ワーカースレッドが異常終了", "3.4.15+\nまたは 3.5.x+"]
    ]

    for idx, row in enumerate(cve_data, start=7):
        ws3.append(row)
        fill_curr = fill_zebra_odd if idx % 2 == 1 else fill_zebra_even
        apply_row_style(ws3, idx, font=font_regular, fill=fill_curr, alignment=align_top_left, border=border_cell, height=65)
        ws3.cell(row=idx, column=1).alignment = align_center
        ws3.cell(row=idx, column=1).font = font_bold
        ws3.cell(row=idx, column=2).alignment = align_center
        ws3.cell(row=idx, column=3).alignment = align_center
        ws3.cell(row=idx, column=3).font = font_bold
        ws3.cell(row=idx, column=4).alignment = align_center
        ws3.cell(row=idx, column=8).alignment = align_center
        ws3.cell(row=idx, column=8).font = font_bold

    # Section 2: 連鎖崩壊シナリオ (The Cascade Failure Deep Dive)
    curr_r3 = 12
    ws3.merge_cells(f"A{curr_r3}:H{curr_r3}")
    ws3[f"A{curr_r3}"] = "2. 4つのOSSが結託して引き起こす『ドミノ倒し型 連鎖障害（Cascading Failure）』シナリオ"
    ws3[f"A{curr_r3}"].font = font_section
    ws3[f"A{curr_r3}"].fill = fill_section
    ws3[f"A{curr_r3}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws3.row_dimensions[curr_r3].height = 28

    cascade_steps = [
        ("第1段階\n【侵入・汚染】", "spring-data-commons\n(CVE-2026-41716)",
         "攻撃者または悪質なボットが、検索APIや一覧取得APIに対してランダムな文字列（例: ?sort=attr_a8f93j2...）を大量に付与してリクエストを連打。\n"
         "Spring Data CommonsのPropertyPath解析ルーチンがこれらを正規の要求として解釈し、内部キャッシュ（Map）に無尽蔵に登録し始める。"),
        ("第2段階\n【ヒープ圧迫とGC遅延】", "JVM Heap Memory\n× spring-data-commons",
         "キャッシュがOld領域を占有し続け、空きメモリが激減。JVMはメモリ確保のために頻繁にConcurrent Mark SweepやG1GCのFull GCを誘発。\n"
         "すべてのスレッドが数秒〜十数秒停止する『Stop-The-World（STW）』が発生し、通信レスポンスが極端に悪化する。"),
        ("第3段階\n【タイマー競合の誘発】", "reactor-core\n(CVE-2026-47863 / 47857)",
         "GCによるSTWと高負荷が引き金となり、時間厳格なFlux.windowTimeoutやbufferTimeoutの内部タイマーと上流データ到着のタイミングが衝突（レースコンディション）。\n"
         "整数オーバーフローや競合状態が強制発火し、データ処理パイプラインが完全にハング（フリーズ）する。"),
        ("第4段階\n【接続枯渇と完全沈黙】", "spring-data-redis\n× Lettuce Driver",
         "Spring Data Redisが背後で利用しているLettuceドライバはReactor Core上で動作しているため、Reactorのパイプライン停止によりRedisからの応答受信待ちハンドラが沈黙。\n"
         "コネクションが返却されずプールが瞬時に枯渇。セッション情報やキャッシュ取得を試みる後続の一般ユーザーリクエストが全てブロッキングされ、システム全体が504 Gateway Timeoutで完全停止する。")
    ]

    curr_r3 += 2
    ws3.merge_cells(f"A{curr_r3}:B{curr_r3}")
    ws3.merge_cells(f"C{curr_r3}:D{curr_r3}")
    ws3.merge_cells(f"E{curr_r3}:H{curr_r3}")
    ws3.cell(row=curr_r3, column=1, value="障害進展フェーズ").alignment = align_center
    ws3.cell(row=curr_r3, column=3, value="障害発生コンポーネント").alignment = align_center
    ws3.cell(row=curr_r3, column=5, value="連鎖崩壊（カスケード障害）の進行プロセス").alignment = align_center
    for c in range(1, 9):
        cell = ws3.cell(row=curr_r3, column=c)
        cell.font = font_tbl_header
        cell.fill = fill_tbl_header
        cell.border = border_header
    ws3.row_dimensions[curr_r3].height = 25

    for phase, comp, desc in cascade_steps:
        curr_r3 += 1
        ws3.merge_cells(f"A{curr_r3}:B{curr_r3}")
        ws3.merge_cells(f"C{curr_r3}:D{curr_r3}")
        ws3.merge_cells(f"E{curr_r3}:H{curr_r3}")
        
        ws3.cell(row=curr_r3, column=1, value=phase).alignment = align_center
        ws3.cell(row=curr_r3, column=1).font = font_bold
        ws3.cell(row=curr_r3, column=3, value=comp).alignment = align_center
        ws3.cell(row=curr_r3, column=3).font = font_bold
        ws3.cell(row=curr_r3, column=5, value=desc).alignment = align_top_left
        
        fill_curr = fill_zebra_odd if curr_r3 % 2 == 1 else fill_zebra_even
        for col_idx in range(1, 9):
            c = ws3.cell(row=curr_r3, column=col_idx)
            c.font = font_regular
            c.fill = fill_curr
            c.border = border_cell
        ws3.row_dimensions[curr_r3].height = 55

    auto_fit_columns(ws3, min_widths={"A": 16, "B": 16, "C": 18, "D": 18, "E": 28, "F": 28, "G": 28, "H": 22})
    ws3.freeze_panes = "A7"

    # =========================================================================
    # SHEET 4: 対策ロードマップ・検証手順 (Countermeasures & Frontier Verification)
    # =========================================================================
    ws4 = wb.create_sheet(title="04_対策ロードマップ・検証手順")
    ws4.views.sheetView[0].showGridLines = True

    # Title
    ws4.merge_cells("A1:H1")
    ws4["A1"] = "【恒久・暫定対策】依存関係整合マトリクス、段階的移行ロードマップ、Frontier検証ラダー"
    ws4["A1"].font = font_title
    ws4["A1"].fill = fill_title
    ws4["A1"].alignment = align_center
    ws4.row_dimensions[1].height = 42

    ws4.merge_cells("A2:H2")
    ws4["A2"] = "安全確実なバージョンアップ計画と、推測を排した5段階の実機テスト・エビデンス検証手順"
    ws4["A2"].font = font_small
    ws4["A2"].fill = fill_card_bg
    ws4["A2"].alignment = align_center
    ws4.row_dimensions[2].height = 20

    ws4.merge_cells("A4:H4")
    ws4["A4"] = "1. バージョン整合性マトリクス（BOMによる一括アップグレード定義）"
    ws4["A4"].font = font_section
    ws4["A4"].fill = fill_section
    ws4["A4"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[4].height = 28

    dep_headers = ["対象モジュール (Artifact)", "現行EOLバージョン", "個別JAR単体更新の可否", "【推奨】移行後バージョン\n(Spring Boot 3.5.x系)", "【商用】移行後バージョン\n(Tanzu Commercial)", "主な互換性・破壊的変更事項", "修正・対応方針"]
    ws4.append([]) # row 5 empty
    ws4.append(dep_headers)
    apply_row_style(ws4, 6, font=font_tbl_header, fill=fill_tbl_header, alignment=align_center, border=border_header, height=28)

    deps_data = [
        ["reactor-core", "3.6.6", "× 絶対不可 (バイナリ非互換)", "3.7.x / 3.8.x", "3.6.17+ (商用パッチ)", "fairBackpressureのデフォルト挙動修正、非推奨オペレータの整理", "spring-boot-dependencies BOMの更新により自動整合させる"],
        ["spring-data-commons", "3.4.3", "× 絶対不可 (メソッド不整合)", "3.5.x / 2025.0+", "3.4.15+ (商用パッチ)", "PropertyPathキャッシュの制限導入、Sortバリデーション厳格化", "コントローラでのPageable/Sort受け取り部分の単体テスト再実行"],
        ["spring-data-redis", "3.4.3", "× 絶対不可 (Commonsと密結合)", "3.5.x / 2025.0+", "3.4.15+ (商用パッチ)", "Lettuceドライババージョン同期、Redis接続設定の微細変更", "RedisTemplateおよび@Cacheableのキャッシュキー整合性試験"],
        ["spring-data-keyvalue", "3.4.3", "× 絶対不可 (Commonsと密結合)", "3.5.x / 2025.0+", "3.4.15+ (商用パッチ)", "KeyValueAdapter内部実装の更新", "Redis Repositories（@RedisHash）のCRUD・インデックス動作確認"]
    ]

    for idx, row in enumerate(deps_data, start=7):
        ws4.append(row)
        fill_curr = fill_zebra_odd if idx % 2 == 1 else fill_zebra_even
        apply_row_style(ws4, idx, font=font_regular, fill=fill_curr, alignment=align_top_left, border=border_cell, height=45)
        ws4.cell(row=idx, column=1).alignment = align_center
        ws4.cell(row=idx, column=1).font = font_bold
        ws4.cell(row=idx, column=2).alignment = align_center
        ws4.cell(row=idx, column=3).alignment = align_center
        ws4.cell(row=idx, column=3).font = font_bold
        ws4.cell(row=idx, column=4).alignment = align_center
        ws4.cell(row=idx, column=4).font = font_bold
        ws4.cell(row=idx, column=5).alignment = align_center

    # Section 2: 段階的移行ロードマップ
    curr_r4 = 12
    ws4.merge_cells(f"A{curr_r4}:H{curr_r4}")
    ws4[f"A{curr_r4}"] = "2. 段階的移行ロードマップ（Phased Execution Schedule）"
    ws4[f"A{curr_r4}"].font = font_section
    ws4[f"A{curr_r4}"].fill = fill_section
    ws4[f"A{curr_r4}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[curr_r4].height = 28

    phases = [
        ("Phase 1: 影響分析と依存関係調査", "即時 (1週目)", "・./gradlew dependencies または mvn dependency:tree による推移的依存の完全可視化\n・ソースコード内の `Flux.windowTimeout` / `bufferTimeout` 利用箇所の静的解析\n・Webエンドポイントにおける非サニタイズなSort/Pageableパラメータの洗い出し"),
        ("Phase 2: 応急遮断ワークアラウンド", "1〜2週目", "・WAFまたはGateway層で、ソートクエリに対する正規表現ホワイトリスト（英数字・許可フィールドのみ）を設定\n・悪意あるランダムパラメータによるPropertyPathキャッシュ汚染（CVE-2026-41716）を外部境界で遮断"),
        ("Phase 3: ビルド定義更新と互換性修正", "3〜4週目", "・Spring Boot Parent / BOM のバージョンを引き上げ（3.5.x または最新サポート版）\n・4つのJARが新バージョンへ一斉昇格されたことを依存関係ツリーで確認\n・コンパイルエラーや非推奨API警告の修正、ビルドスクリプトの調整"),
        ("Phase 4: 多層テスト検証（ラダー実行）", "5〜6週目", "・後述の『Frontier検証ラダー』に従い、Level 1（単体）からLevel 4（統合回帰）まで自動テストを完走\n・Testcontainersを用いたローカルRedisコンテナでの実動作検証"),
        ("Phase 5: 負荷耐久・プロファイリング検証", "7週目", "・ステージング環境にてk6/JMeterを用いたスパイク負荷試験を実施\n・JVMヒープ使用量推移（Old領域の安定性）の確認、スレッドダンプ取得によるハング停止の非発生を証明"),
        ("Phase 6: 本番リリースと監視体制", "8週目", "・カナリアリリースまたはBlue-Greenデプロイによる安全な本番展開\n・APM（Datadog/Prometheus）によるJVMヒープ・GC時間・Redisコネクション数のリアルタイム監視")
    ]

    curr_r4 += 2
    ws4.merge_cells(f"A{curr_r4}:B{curr_r4}")
    ws4.cell(row=curr_r4, column=1, value="フェーズ・期間").alignment = align_center
    ws4.cell(row=curr_r4, column=3, value="想定期間").alignment = align_center
    ws4.merge_cells(f"D{curr_r4}:H{curr_r4}")
    ws4.cell(row=curr_r4, column=4, value="具体的な実施タスクと成果物").alignment = align_center
    for c in range(1, 9):
        cell = ws4.cell(row=curr_r4, column=c)
        cell.font = font_tbl_header
        cell.fill = fill_tbl_header
        cell.border = border_header
    ws4.row_dimensions[curr_r4].height = 25

    for p_name, p_time, p_task in phases:
        curr_r4 += 1
        ws4.merge_cells(f"A{curr_r4}:B{curr_r4}")
        ws4.cell(row=curr_r4, column=1, value=p_name).alignment = align_center
        ws4.cell(row=curr_r4, column=1).font = font_bold
        ws4.cell(row=curr_r4, column=3, value=p_time).alignment = align_center
        ws4.cell(row=curr_r4, column=3).font = font_bold
        ws4.merge_cells(f"D{curr_r4}:H{curr_r4}")
        ws4.cell(row=curr_r4, column=4, value=p_task).alignment = align_top_left
        
        fill_curr = fill_zebra_odd if curr_r4 % 2 == 1 else fill_zebra_even
        for col_idx in range(1, 9):
            c = ws4.cell(row=curr_r4, column=col_idx)
            c.font = font_regular
            c.fill = fill_curr
            c.border = border_cell
        ws4.row_dimensions[curr_r4].height = 50

    # Section 3: Frontier検証ラダー (Level 1 - Level 5)
    curr_r4 += 2
    ws4.merge_cells(f"A{curr_r4}:H{curr_r4}")
    ws4[f"A{curr_r4}"] = "3. Frontier-Coding流 厳格な検証ラダー（Verification Ladder）"
    ws4[f"A{curr_r4}"].font = font_section
    ws4[f"A{curr_r4}"].fill = fill_section
    ws4[f"A{curr_r4}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[curr_r4].height = 28

    ladders = [
        ("Level 1\n局所・静的検証", "構文・コンパイル・型整合性", "./gradlew clean testClasses\nまたは mvn test-compile",
         "・Javaソースコードのコンパイルが警告・エラーなく通過すること\n・非推奨（Deprecated）となったReactor/Spring Dataメソッドの呼出箇所の特定と解消"),
        ("Level 2\n焦点・単体検証", "リポジトリ・マッピング層単体試験", "./gradlew test --tests *RepositoryTest*\nまたは mvn test -Dtest=*RepositoryTest",
         "・@DataRedisTest やモックを用いたCRUD操作、エンティティのシリアライズ/デシリアライズの正常性\n・PageableやSortオブジェクトを渡した際のクエリ生成が破綻しないことの確認"),
        ("Level 3\nコンポーネント検証", "Redis Testcontainers実機連携", "./gradlew test --tests *RedisIntegrationTest*",
         "・Docker上の実Redisインスタンスに対してLettuce経由で書き込み・読み込み・TTL消去が想定通り動作すること\n・Pub/Subメッセージの配信やReactiveRedisTemplateのパイプライン処理の疎通確認"),
        ("Level 4\n統合・回帰検証", "全自動テストスイート完走", "./gradlew check\nまたは mvn verify",
         "・リポジトリ全体のユニットテスト・スライステストが1件の失敗もなくAll Green（パス）すること\n・推移的依存関係の不整合（NoSuchMethodError等）が一切発生しないことの証明"),
        ("Level 5\n実行時・負荷耐久検証", "高並行負荷・OOM/ハング非発生の証明", "k6 run load-test.js\nJMeter 1000concurrency\njcmd <pid> GC.heap_info",
         "・大量の不正Sortパラメータを注入した際、ヒープメモリが上限で頭打ちになりOOMが発生しないことの確認\n・長時間ストリーミング処理においてスレッドダンプを取得し、BLOCKED/TIMED_WAITINGの永久滞留がないことの確認")
    ]

    curr_r4 += 2
    ws4.merge_cells(f"A{curr_r4}:B{curr_r4}")
    ws4.cell(row=curr_r4, column=1, value="検証レベル").alignment = align_center
    ws4.cell(row=curr_r4, column=3, value="対象領域").alignment = align_center
    ws4.cell(row=curr_r4, column=4, value="実行コマンド / 手法").alignment = align_center
    ws4.merge_cells(f"E{curr_r4}:H{curr_r4}")
    ws4.cell(row=curr_r4, column=5, value="合格判定基準（エビデンス要件）").alignment = align_center
    for c in range(1, 9):
        cell = ws4.cell(row=curr_r4, column=c)
        cell.font = font_tbl_header
        cell.fill = fill_tbl_header
        cell.border = border_header
    ws4.row_dimensions[curr_r4].height = 25

    for l_lvl, l_area, l_cmd, l_crit in ladders:
        curr_r4 += 1
        ws4.merge_cells(f"A{curr_r4}:B{curr_r4}")
        ws4.cell(row=curr_r4, column=1, value=l_lvl).alignment = align_center
        ws4.cell(row=curr_r4, column=1).font = font_bold
        ws4.cell(row=curr_r4, column=3, value=l_area).alignment = align_center
        ws4.cell(row=curr_r4, column=3).font = font_bold
        ws4.cell(row=curr_r4, column=4, value=l_cmd).alignment = align_top_left
        ws4.merge_cells(f"E{curr_r4}:H{curr_r4}")
        ws4.cell(row=curr_r4, column=5, value=l_crit).alignment = align_top_left
        
        fill_curr = fill_zebra_odd if curr_r4 % 2 == 1 else fill_zebra_even
        for col_idx in range(1, 9):
            c = ws4.cell(row=curr_r4, column=col_idx)
            c.font = font_regular
            c.fill = fill_curr
            c.border = border_cell
        ws4.row_dimensions[curr_r4].height = 55

    auto_fit_columns(ws4, min_widths={"A": 16, "B": 16, "C": 20, "D": 26, "E": 24, "F": 24, "G": 24, "H": 24})
    ws4.freeze_panes = "A7"

    # Save
    wb.save(file_path)
    print(f"Successfully generated Excel workbook at: {file_path}")

if __name__ == "__main__":
    out_file = r"C:\Users\taka_\Agy\OSS_EOL_Agy\OSS_EOL_Countermeasures_Report.xlsx"
    build_excel_report(out_file)
