import pandas as pd


def layout_conv_domestic(df) -> pd.DataFrame:

    # 1. 全体で共通の情報（ヘッダー部分）を取得
    jigyosho = df.iloc[2, 3]   # D列: 空港コード (0:A, 1:B, 2:C, 3:D) 

    # 日付列の範囲（H列:日付 〜 AL列:31日分等）
    # 10列目からDFのカラム数まで
    date_cols = list(range(10, df.shape[1]))

    records = []

    # 2. 便ごとのデータブロックを6行単位でループ処理
    start_index = 4     #　EXCEL5行目から開始
    block_size = 6      #　6行単位で取得する
    #　Range(開始,終了,ステップ) len(df)はDFの行数なので、4行目からDFの行数まで、6行ずつ
    for start_row in range(start_index, len(df), block_size):
        if start_row + block_size > len(df):
            break
        #　(block)範囲抽出データには4行目から9行目（6行分）のデータをひとかたまりで生成する    
        block = df.iloc[start_row : start_row + block_size]
        
        # 便情報の取得（ブロックの1行目・A~G列）
        unkou_kbn = block.iloc[0, 1]  # A列: 運航区分
        airline   = block.iloc[0, 2]  # B列: 航空会社
        flight_no = block.iloc[0, 3]  # C列: 便名
        dep_airport = block.iloc[0, 4]  # D列: 出発
        raw_arr_airport = block.iloc[0, 5]  # E列 (index 4): 到着 "旭川"

        # ダイバート（目的地変更）判定
        if unkou_kbn in ["SD(DVT)", "SI(DVT)"]:
            plan_arr_airport = raw_arr_airport # E列: 到着(予定)
            arr_airport = jigyosho
        else:
            plan_arr_airport = ""
            arr_airport = raw_arr_airport # E列: 到着
        # データが入っていない空行・パディング行ならループ脱出
        if pd.isna(flight_no):
            continue
        processed_days =0 # 処理した日数（便数）のカウンター
        # 日付ごとの列を展開（縦持ち変換）
        for col_idx in date_cols:
            if processed_days >= 31: 
                break
            # 列インデックスがデータフレームの列数を超えていないか判定
            if col_idx >= df.shape[1]:
                break
            # ※日付自体が共通行（4行目）にあるので、日付として取得
            raw_day_val = df.iloc[3, col_idx] 
            # 日付カラムがブランクの場合は処理SKIP
            if pd.isna(raw_day_val):
                continue
            # 日付形式としてデータ変換を行う            
            day_val =pd.to_datetime(raw_day_val, errors="coerce")

            # 日付形式でない場合は処理SKIPする        
            if pd.isna(day_val):
                continue

            record = {
                '運航区分': unkou_kbn,
                '運航日': day_val,
                '航空会社': airline,
                '便名': flight_no,
                '出発空港': dep_airport,
                '到着空港': arr_airport,
                '到着予定空港': plan_arr_airport,
                '機材名': block.iloc[0, col_idx], # 1行目
                '座席数': block.iloc[1, col_idx], # 2行目
                '旅客数': block.iloc[2, col_idx], # 3行目
                'INF数': block.iloc[3, col_idx],  # 4行目
                '貨物重量': block.iloc[4, col_idx],# 5行目
                'メール重量': block.iloc[5, col_idx], # 6行目
                '備考':'',
                '事業所': jigyosho
            }
            records.append(record)
            processed_days += 1

    # 3. データフレーム化
    return pd.DataFrame(records)


def layout_conv_inter(df) -> pd.DataFrame:

    # 1. 全体で共通の情報（ヘッダー部分）を取得
    jigyosho = df.iloc[2, 3]   # D列: 空港コード (0:A, 1:B, 2:C, 3:D) 

    # 日付列の範囲（H列:日付 〜 AL列:31日分等）
    # 10列目からDFのカラム数まで
    date_cols = list(range(10, df.shape[1]))

    records = []

    # 2. 便ごとのデータブロックを6行単位でループ処理
    start_index = 4
    block_size = 4
    #　Range(開始,終了,ステップ) len(df)はDFの全行数なので、4行目からDFの行数まで、4行ずつ
    for start_row in range(start_index, len(df), block_size):
        if start_row + block_size > len(df):
            break
        #　(block)範囲抽出データには4行目から7行目（4行分）のデータをひとかたまりで生成する    
        block = df.iloc[start_row : start_row + block_size]
        
        # 便情報の取得（ブロックの1行目・A~G列）
        unkou_kbn = block.iloc[0, 1]  # A列: 運航区分
        airline   = block.iloc[0, 2]  # B列: 航空会社
        flight_no = block.iloc[0, 3]  # C列: 便名
        dep_airport = block.iloc[0, 4]  # D列: 出発
        raw_arr_airport = block.iloc[0, 5]  # E列 (index 4): 到着 "旭川"

        # ダイバート（目的地変更）判定
        if unkou_kbn in ["SD(DVT)", "SI(DVT)"]:
            plan_arr_airport = raw_arr_airport # E列: 到着(予定)
            arr_airport = jigyosho
        else:
            plan_arr_airport = ""
            arr_airport = raw_arr_airport # E列: 到着

        # データが入っていない空行・パディング行ならループ脱出
        if pd.isna(flight_no):
            continue

        processed_days =0 # 処理した日数（便数）のカウンター

        # 日付ごとの列を展開（縦持ち変換）
        for col_idx in date_cols:
            if processed_days >= 31: 
                break

            # 列インデックスがデータフレームの列数を超えていないか判定
            if col_idx >= df.shape[1]:
                break

            # ※日付自体が共通行（4行目）にあるので順次取得する
            raw_day_val = df.iloc[3, col_idx] 

            if pd.isna(raw_day_val):
                continue
            # 日付形式としてデータ変換を行う            
            day_val =pd.to_datetime(raw_day_val, errors="coerce")

            if pd.isna(day_val):
                continue

            record = {
                '運航区分': unkou_kbn,
                '運航日': day_val,
                '航空会社': airline,
                '便名': flight_no,
                '出発空港': dep_airport,
                '到着空港': arr_airport,
                '到着予定空港': plan_arr_airport,
                '機材名': block.iloc[0, col_idx], # 1行目
                '座席数': block.iloc[1, col_idx], # 2行目
                '旅客数': block.iloc[2, col_idx], # 3行目
                'INF数': block.iloc[3, col_idx],  # 4行目
                '備考':'',
                '事業所': jigyosho
            }
            records.append(record)
            processed_days += 1

    # 3. データフレーム化
    return pd.DataFrame(records)
