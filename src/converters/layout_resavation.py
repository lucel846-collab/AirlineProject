import pandas as pd

from src.detect_layout import Layout_type
from src.resultform import ReadResult


def layout_reservation_flight(df) -> pd.DataFrame:
    # 1. 全体で共通の情報（ヘッダー部分）を取得
    jigyosho = df.iloc[2, 1]   # B列: 空港コード (0:A, 1:B, 2:C, 3:D) 

    # 日付列の範囲（H列:日付 〜 AL列:31日分等）
    # 6列目からAJカラム数まで
    date_cols = list(range(5, df.shape[1]))

    records = []

    # 2. 便ごとのデータブロックを4行単位でループ処理
    start_index = 4
    block_size = 7
    #　Range(開始,終了,ステップ) len(df)はDFの全行数なので、4行目からDFの行数まで、4行ずつ
    for start_row in range(start_index, len(df), block_size):
        if start_row + block_size > len(df):
            break
        #　(block)範囲抽出データには4行目から7行目（4行分）のデータをひとかたまりで生成する    
        block = df.iloc[start_row : start_row + block_size]
        #print(block)
        # 便情報の取得（ブロックの1行目・A~G列）
        #unkou_kbn = block.iloc[0, 1]  # A列: 運航区分
        airline2L1   = block.iloc[2, 0]  # A列: Airline 2Letter Code
        airline2L2   = block.iloc[4, 0]  # A列: Airline 2Letter Code
        flight_no1   = block.iloc[2, 1]  # B列: FlightNO
        flight_no2   = block.iloc[4, 1]  # B列: FlightNO
        dep_airport1 = block.iloc[2, 2]  # C列 (index 2): FROM
        dep_airport2 = block.iloc[4, 2]  # D列 (index 4): FROM
        arr_airport1 = block.iloc[2, 3]  # C列 (index 2): TO
        arr_airport2 = block.iloc[4, 3]  # D列 (index 4): TO
        lead_time    = block.iloc[6, 1]  # C列 (index 3): LeadTime
        # データが入っていない空行・パディング行ならループ脱出
        if pd.isna(flight_no1) and pd.isna(flight_no2):
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

            if  jigyosho == dep_airport1: 
                record1 = {
                #   '運航区分': unkou_kbn,
                    '運航日': day_val,
                    '航空会社2Lコード': airline2L1,
                    '便名': flight_no1,
                    '出発空港': dep_airport1,
                    '到着空港': arr_airport1,
                    '機材名': block.iloc[0, col_idx], # 1行目
                    '座席数': block.iloc[1, col_idx], # 2行目
                    '旅客数': block.iloc[2, col_idx], # 3行目
                    '出発時刻': block.iloc[3, col_idx],  # 4行目
                    '到着時刻': "",
                    '事業所': jigyosho,
                    'リードタイム': lead_time,
                }
            else:
                record1 = {
                    '運航日': day_val,
                    '航空会社2Lコード': airline2L1,
                    '便名': flight_no1,
                    '出発空港': dep_airport1,
                    '到着空港': arr_airport1,
                    '機材名': block.iloc[0, col_idx], # 1行目
                    '座席数': block.iloc[1, col_idx], # 2行目
                    '旅客数': block.iloc[2, col_idx], # 3行目
                    '出発時刻': "",
                    '到着時刻': block.iloc[3, col_idx],  # 4行目
                    '事業所': jigyosho,
                    'リードタイム': lead_time,
                }
            records.append(record1)
            if  jigyosho == dep_airport2: 
                record2 = {
                    '運航日': day_val,
                    '航空会社2Lコード': airline2L2,
                    '便名': flight_no2,
                    '出発空港': dep_airport2,
                    '到着空港': arr_airport2,
                    '機材名': block.iloc[0, col_idx], # 1行目
                    '座席数': block.iloc[1, col_idx], # 2行目
                    '旅客数': block.iloc[4, col_idx], # 4行目
                    '出発時刻': block.iloc[5, col_idx],  # 5行目,
                    '到着時刻': "",
                    '事業所': jigyosho,
                    'リードタイム': lead_time,
                }
            else:
                record2 = {
                    '運航日': day_val,
                    '航空会社2Lコード': airline2L2,
                    '便名': flight_no2,
                    '出発空港': dep_airport2,
                    '到着空港': arr_airport2,
                    '機材名': block.iloc[0, col_idx], # 1行目
                    '座席数': block.iloc[1, col_idx], # 2行目
                    '旅客数': block.iloc[4, col_idx], # 4行目
                    '出発時刻': "",
                    '到着時刻': block.iloc[5, col_idx],  # 5行目
                    '事業所': jigyosho,
                    'リードタイム': lead_time,
                }
            records.append(record2)
            processed_days += 1

    # 3. データフレーム化
    results = []
    results.append(ReadResult(df=pd.DataFrame(records),layout=Layout_type.RESERVATION.value))
    return results

