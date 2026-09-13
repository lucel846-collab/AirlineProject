import numpy as np
import pandas as pd

from src.detect_layout import Layout_type
from src.resultform import ReadResult


def layout_passenger_report(df) -> list[ReadResult]:

    # 1. 全体で共通の情報（ヘッダー部分）を取得
    year_date = df.iloc[1, 2] # C列：年月
    jigyosho = df.iloc[2, 4]  # D列: 空港コード (0:A, 1:B, 2:C, 3:D) 
    airline  = df.iloc[2, 7]  # B列: 航空会社
       
    # 日付列の範囲（H列:日付 〜 AL列:31日分等）

    skd_records = []
    dvt_records = []
    # 1. 定期便の最終位置設定
    start_row_teiki = df[df.iloc[:,0] == '■定期便'].index[0]
    start_row_DVT = df[df.iloc[:,0] == '■ダイバート'].index[0]
    start_row_CHRT = df[df.iloc[:,0] == '■チャーター便等'].index[0]
    # 2. 便ごとのデータブロックを6行単位でループ処理
    #　定期便の運用データを生成する 
    start_index = start_row_teiki + 2     #　EXCEL6行目から開始
    max_teiki = start_row_DVT- start_row_teiki
    target_rng = df.iloc[start_index:max_teiki]
    col2_clean = target_rng.iloc[:, 1].astype(str).str.strip().replace('', np.nan)
    last_idx = col2_clean.last_valid_index()
    if not last_idx is None:
        for start_row in range(start_index, last_idx+1):
            # 便情報の取得（ブロックの1行目・A~G列）
            record = {
                '運航区分': 'SD(定期)',
                '年月': year_date,
                '航空会社': airline,
                '出発空港': jigyosho,
                '到着空港': df.iloc[start_row, 1],
                '計画便数': None,
                '便数': df.iloc[start_row, 2], # 1行目,
                '発着区分':'出発',
                '路線名': df.iloc[start_row, 1], # 1行目,
                '座席数': df.iloc[start_row, 3], # 2行目
                '旅客数': df.iloc[start_row, 4], # 3行目
                'INF数': df.iloc[start_row, 5],  # 4行目
                '貨物重量': df.iloc[start_row, 6],# 5行目
                'メール重量': df.iloc[start_row, 7], # 6行目
                '有償貨物件数': None,
                '備考': None,
                '事業所': jigyosho
            }
            skd_records.append(record)
            record = {
                '運航区分': 'SD(定期)',
                '年月': year_date,
                '航空会社': airline,
                '出発空港': df.iloc[start_row, 1],
                '到着空港': jigyosho,
                '計画便数': None,
                '便数': df.iloc[start_row, 8], # 1行目,
                '発着区分':'到着',
                '路線名': df.iloc[start_row, 1], # 1行目,
                '座席数': df.iloc[start_row, 9], # 2行目
                '旅客数': df.iloc[start_row, 10], # 3行目
                'INF数': df.iloc[start_row, 11],  # 4行目
                '貨物重量': df.iloc[start_row, 12],# 5行目
                'メール重量': df.iloc[start_row, 13], # 6行目
                '有償貨物件数': None,
                '備考': None,
                '事業所': jigyosho
            }
            skd_records.append(record)

    #　DVT便の運用データを生成する 
    start_index = start_row_DVT + 2     #　DVT指標から＋2行目を開始とする
    target_rng = df.iloc[start_index:start_row_CHRT]
    col2_clean = target_rng.iloc[:, 1].astype(str).str.strip().replace('', np.nan)
    last_idx = col2_clean.last_valid_index()
    if not last_idx is None:
        for start_row in range(start_index, last_idx+1):
            # 便情報の取得（ブロックの1行目・A~G列）
            record = {
            '運航区分': 'XD(DVT)',
            '運航日': df.iloc[start_row, 1],
            '便名': df.iloc[start_row, 2],
            '航空会社': airline,
            '出発空港': df.iloc[start_row, 3],
            '到着空港': jigyosho,
            '到着予定空港':df.iloc[start_row, 4],
            '機材名': '',
            '座席数': df.iloc[start_row, 5], # 2行目
            '旅客数': df.iloc[start_row, 6], # 3行目
            'INF数': df.iloc[start_row, 7],  # 4行目
            '貨物重量': df.iloc[start_row, 8],# 5行目
            'メール重量': df.iloc[start_row, 9], # 6行目
            '備考': None,
            '事業所': jigyosho
            }
            dvt_records.append(record)
            
    #　CHRTER便の運用データを生成する 
    start_index = start_row_CHRT+2
    target_rng = df.iloc[start_index:df.shape[0]]
    col2_clean = target_rng.iloc[:, 1].astype(str).str.strip().replace('', np.nan)
    last_idx = col2_clean.last_valid_index()
    if not last_idx is None:
         for start_row in range(start_index, last_idx+1):
            # 便情報の取得（ブロックの1行目・A~G列）
            record = {
            '運航区分': 'ND(CHRT)',
            '運航日': df.iloc[start_row, 1],
            '便名': df.iloc[start_row, 2],
            '航空会社': airline,
            '出発空港': df.iloc[start_row, 3],
            '到着空港': df.iloc[start_row, 4],
            '到着予定空港':'',
            '機材名': '',
            '座席数': df.iloc[start_row, 5], # 2行目
            '旅客数': df.iloc[start_row, 6], # 3行目
            'INF数': df.iloc[start_row, 7],  # 4行目
            '貨物重量': df.iloc[start_row, 8],# 5行目
            'メール重量': df.iloc[start_row, 9], # 6行目
            '備考': None,
            '事業所': jigyosho
            }
            dvt_records.append(record)
    # 3. データフレーム化
    results = []
    if skd_records:
        results.append(ReadResult(df=pd.DataFrame(skd_records),layout=Layout_type.MONTHLY_ROUTE.value))
    if dvt_records:
        results.append(ReadResult(df=pd.DataFrame(dvt_records),layout=Layout_type.DAILY.value))

    return results

def layout_passenger_report2(df) -> list[ReadResult]:

    # 1. 全体で共通の情報（ヘッダー部分）を取得
    year_date = df.iloc[1, 2] # C列：年月
    jigyosho = df.iloc[2, 4]  # D列: 空港コード (0:A, 1:B, 2:C, 3:D) 
    airline  = df.iloc[2, 7]  # B列: 航空会社
       
    # 日付列の範囲（H列:日付 〜 AL列:31日分等）

    skd_records = []
    dvt_records = []
    # 1. 定期便の最終位置設定
    start_row_teiki = df[df.iloc[:,0] == '■定期便'].index[0]
    start_row_DVT = df[df.iloc[:,0] == '■ダイバート'].index[0]
    start_row_CHRT = df[df.iloc[:,0] == '■チャーター便等'].index[0]
    # 2. 便ごとのデータブロックを6行単位でループ処理
    #　定期便の運用データを生成する 
    start_index = start_row_teiki + 2     #　EXCEL6行目から開始
    max_teiki = start_row_DVT- start_row_teiki
    target_rng = df.iloc[start_index:max_teiki]
    col2_clean = target_rng.iloc[:, 1].astype(str).str.strip().replace('', np.nan)
    last_idx = col2_clean.last_valid_index()
    if not last_idx is None:
        for start_row in range(start_index, last_idx+1):
            # 便情報の取得（ブロックの1行目・A~G列）
            record = {
                '運航区分': 'SD(定期)',
                '年月': year_date,
                '航空会社': airline,
                '出発空港': jigyosho,
                '到着空港': df.iloc[start_row, 1],
                '計画便数': df.iloc[start_row, 2],
                '便数': df.iloc[start_row, 3], # 1行目,
                '発着区分':'出発',
                '路線名': df.iloc[start_row, 1], # 1行目,
                '座席数': df.iloc[start_row, 4], # 2行目
                '旅客数': df.iloc[start_row, 5], # 3行目
                'INF数': df.iloc[start_row, 6],  # 4行目
                '貨物重量': df.iloc[start_row, 7],# 5行目
                'メール重量': df.iloc[start_row, 8], # 6行目
                '有償貨物件数': None,
                '備考': None,
                '事業所': jigyosho
            }
            skd_records.append(record)
            record = {
                '運航区分': 'SD(定期)',
                '年月': year_date,
                '航空会社': airline,
                '出発空港': df.iloc[start_row, 1],
                '到着空港': jigyosho,
                '計画便数': df.iloc[start_row, 9],
                '便数': df.iloc[start_row, 10], # 1行目,
                '発着区分':'到着',
                '路線名': df.iloc[start_row, 1], # 1行目,
                '座席数': df.iloc[start_row, 11], # 2行目
                '旅客数': df.iloc[start_row, 12], # 3行目
                'INF数': df.iloc[start_row, 13],  # 4行目
                '貨物重量': df.iloc[start_row, 14],# 5行目
                'メール重量': df.iloc[start_row, 15], # 6行目
                '有償貨物件数': None,
                '備考': None,
                '事業所': jigyosho
            }
            skd_records.append(record)

    #　DVT便の運用データを生成する 
    start_index = start_row_DVT + 2     #　DVT指標から＋2行目を開始とする
    target_rng = df.iloc[start_index:start_row_CHRT]
    col2_clean = target_rng.iloc[:, 1].astype(str).str.strip().replace('', np.nan)
    last_idx = col2_clean.last_valid_index()
    if not last_idx is None:
        for start_row in range(start_index, last_idx+1):
            # 便情報の取得（ブロックの1行目・A~G列）
            record = {
            '運航区分': 'XD(DVT)',
            '運航日': df.iloc[start_row, 1],
            '便名': df.iloc[start_row, 2],
            '航空会社': airline,
            '出発空港': df.iloc[start_row, 3],
            '到着空港': jigyosho,
            '到着予定空港':df.iloc[start_row, 4],
            '機材名': '',
            '座席数': df.iloc[start_row, 5], # 2行目
            '旅客数': df.iloc[start_row, 6], # 3行目
            'INF数': df.iloc[start_row, 7],  # 4行目
            '貨物重量': df.iloc[start_row, 8],# 5行目
            'メール重量': df.iloc[start_row, 9], # 6行目
            '備考': None,
            '事業所': jigyosho
            }
            dvt_records.append(record)
            
    #　CHRTER便の運用データを生成する 
    start_index = start_row_CHRT+2
    target_rng = df.iloc[start_index:df.shape[0]]
    col2_clean = target_rng.iloc[:, 1].astype(str).str.strip().replace('', np.nan)
    last_idx = col2_clean.last_valid_index()
    if not last_idx is None:
         for start_row in range(start_index, last_idx+1):
            # 便情報の取得（ブロックの1行目・A~G列）
            record = {
            '運航区分': 'ND(CHRT)',
            '運航日': df.iloc[start_row, 1],
            '便名': df.iloc[start_row, 2],
            '航空会社': airline,
            '出発空港': df.iloc[start_row, 3],
            '到着空港': df.iloc[start_row, 4],
            '到着予定空港':'',
            '機材名': '',
            '座席数': df.iloc[start_row, 5], # 2行目
            '旅客数': df.iloc[start_row, 6], # 3行目
            'INF数': df.iloc[start_row, 7],  # 4行目
            '貨物重量': df.iloc[start_row, 8],# 5行目
            'メール重量': df.iloc[start_row, 9], # 6行目
            '備考': None,
            '事業所': jigyosho
            }
            dvt_records.append(record)
    # 3. データフレーム化
    results = []
    if skd_records:
        results.append(ReadResult(df=pd.DataFrame(skd_records),layout=Layout_type.MONTHLY_ROUTE.value))
    if dvt_records:
        results.append(ReadResult(df=pd.DataFrame(dvt_records),layout=Layout_type.DAILY.value))

    return results

def layout_passenger_report3(df) -> list[ReadResult]:

    # 1. 全体で共通の情報（ヘッダー部分）を取得
    year_date = df.iloc[1, 2] # C列：年月
    jigyosho = df.iloc[2, 4]  # D列: 空港コード (0:A, 1:B, 2:C, 3:D) 
    airline  = df.iloc[2, 7]  # B列: 航空会社
       
    # 日付列の範囲（H列:日付 〜 AL列:31日分等）

    skd_records = []
    dvt_records = []
    # 1. 定期便の最終位置設定
    start_row_teiki = df[df.iloc[:,0] == '■定期便'].index[0]
    start_row_DVT = df[df.iloc[:,0] == '■ダイバート'].index[0]
    start_row_CHRT = df[df.iloc[:,0] == '■チャーター便等'].index[0]
    # 2. 便ごとのデータブロックを6行単位でループ処理
    #　定期便の運用データを生成する 
    start_index = start_row_teiki + 2     #　EXCEL6行目から開始
    max_teiki = start_row_DVT- start_row_teiki
    target_rng = df.iloc[start_index:max_teiki]
    col2_clean = target_rng.iloc[:, 1].astype(str).str.strip().replace('', np.nan)
    last_idx = col2_clean.last_valid_index()
    if not last_idx is None:
        for start_row in range(start_index, last_idx+1):
            # 便情報の取得（ブロックの1行目・A~G列）
            record = {
                '運航区分': 'SD(定期)',
                '年月': year_date,
                '航空会社': airline,
                '出発空港': jigyosho,
                '到着空港': df.iloc[start_row, 1],
                '計画便数': None,
                '便数': df.iloc[start_row, 2], # 1行目,
                '発着区分':'出発',
                '路線名': df.iloc[start_row, 1], # 1行目,
                '座席数': df.iloc[start_row, 3], # 2行目
                '旅客数': df.iloc[start_row, 4], # 3行目
                'INF数': df.iloc[start_row, 5],  # 4行目
                '貨物重量': df.iloc[start_row, 7],# 5行目
                'メール重量': df.iloc[start_row, 8], # 6行目
                '有償貨物件数': df.iloc[start_row, 6],# 5行目
                '備考': None,
                '事業所': jigyosho
            }
            skd_records.append(record)
            record = {
                '運航区分': 'SD(定期)',
                '年月': year_date,
                '航空会社': airline,
                '出発空港': df.iloc[start_row, 1],
                '到着空港': jigyosho,
                '計画便数': None,
                '便数': df.iloc[start_row, 9], # 1行目,
                '発着区分':'到着',
                '路線名': df.iloc[start_row, 1], # 1行目,
                '座席数': df.iloc[start_row, 10], # 2行目
                '旅客数': df.iloc[start_row, 11], # 3行目
                'INF数': df.iloc[start_row, 12],  # 4行目
                '貨物重量': df.iloc[start_row, 14],# 5行目
                'メール重量': df.iloc[start_row, 15], # 6行目
                '有償貨物件数': df.iloc[start_row, 13], # 6行目
                '備考': None,
                '事業所': jigyosho
            }
            skd_records.append(record)

    #　DVT便の運用データを生成する 
    start_index = start_row_DVT + 2     #　DVT指標から＋2行目を開始とする
    target_rng = df.iloc[start_index:start_row_CHRT]
    col2_clean = target_rng.iloc[:, 1].astype(str).str.strip().replace('', np.nan)
    last_idx = col2_clean.last_valid_index()
    if not last_idx is None:
        for start_row in range(start_index, last_idx+1):
            # 便情報の取得（ブロックの1行目・A~G列）
            record = {
            '運航区分': 'XD(DVT)',
            '運航日': df.iloc[start_row, 1],
            '便名': df.iloc[start_row, 2],
            '航空会社': airline,
            '出発空港': df.iloc[start_row, 3],
            '到着空港': jigyosho,
            '到着予定空港':df.iloc[start_row, 4],
            '機材名': '',
            '座席数': df.iloc[start_row, 5], # 2行目
            '旅客数': df.iloc[start_row, 6], # 3行目
            'INF数': df.iloc[start_row, 7],  # 4行目
            '貨物重量': df.iloc[start_row, 8],# 5行目
            'メール重量': df.iloc[start_row, 9], # 6行目
            '備考': None,
            '事業所': jigyosho
            }
            dvt_records.append(record)
            
    #　CHRTER便の運用データを生成する 
    start_index = start_row_CHRT+2
    target_rng = df.iloc[start_index:df.shape[0]]
    col2_clean = target_rng.iloc[:, 1].astype(str).str.strip().replace('', np.nan)
    last_idx = col2_clean.last_valid_index()
    if not last_idx is None:
         for start_row in range(start_index, last_idx+1):
            # 便情報の取得（ブロックの1行目・A~G列）
            record = {
            '運航区分': 'ND(CHRT)',
            '運航日': df.iloc[start_row, 1],
            '便名': df.iloc[start_row, 2],
            '航空会社': airline,
            '出発空港': df.iloc[start_row, 3],
            '到着空港': df.iloc[start_row, 4],
            '到着予定空港':'',
            '機材名': '',
            '座席数': df.iloc[start_row, 5], # 2行目
            '旅客数': df.iloc[start_row, 6], # 3行目
            'INF数': df.iloc[start_row, 7],  # 4行目
            '貨物重量': df.iloc[start_row, 8],# 5行目
            'メール重量': df.iloc[start_row, 9], # 6行目
            '備考': None,
            '事業所': jigyosho
            }
            dvt_records.append(record)
    # 3. データフレーム化
    results = []
    if skd_records:
        results.append(ReadResult(df=pd.DataFrame(skd_records),layout=Layout_type.MONTHLY_ROUTE.value))
    if dvt_records:
        results.append(ReadResult(df=pd.DataFrame(dvt_records),layout=Layout_type.DAILY.value))

    return results
