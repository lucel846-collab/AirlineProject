import pandas as pd

from src.detect_layout import Layout_type
from src.resultform import ReadResult


def layout_arrival_cargo(df) -> pd.DataFrame:

    # 1. 全体で共通の情報（ヘッダー部分）を取得
    jigyosho = df.iloc[2, 1].strip()[-3:]   # B列: 事業所コード (0:A, 1:B, 2:C)右3文字取得
    # 2. データ部分の抽出（14行目以降）と列名の設定
    df_data  = df.iloc[14:].copy()
    df_data.columns =[
                "NOName",
                "出発空港",
                "便名",                      #3列
                "Domestic_Rev_件数",         #4列
                "Domestic_Rev_個数",         #5列
                "Domestic_Rev_重量",         #6列
                "Domestic_NonRev_件数",      #7列
                "Domestic_NonRev_個数",      #8列
                "Domestic_NonRev_重量",      #9列
                "Domestic_Sum_件数",         #10列
                "Domestic_Sum_個数",         #11列
                "Domestic_Sum_重量",         #12列
                "International_Rev_件数",    #13列
                "International_Rev_個数",    #14列
                "International_Rev_重量",    #15列
                "International_NonRev_件数", #16列
                "International_NonRev_個数", #17列
                "International_NonRev_重量", #18列
                "International_Sum_件数",    #19列
                "International_Sum_個数",    #20列
                "International_Sum_重量",    #21列
                "Flight_Sum_件数",           #22列
                "Flight_Sum_個数",           #23列
                "Flight_Sum_重量",           #24列
                ] 
    # 3. 空白行や「合計：」より後の不要なフッター行を削除するためのトリミング
    # 「合計：」という文字が含まれるインデックスを取得
    total_row_idx = df_data[df_data["出発空港"].astype(str).str.contains("合計：")].index
    if not total_row_idx.empty:
        # 最初の「合計：」が出現した位置より前（上）だけを残す
        df_data = df_data.loc[:total_row_idx[0] - 1]
    # 3.5. 便名が空の行を削除
    df_data = df_data.dropna(subset=["便名"]).copy()    
    # 4. 出発空港列の空欄（NaN）を上の値で埋める（Forward Fill）
    df_data["出発空港"] = df_data["出発空港"].ffill()
    # 5. 「小計：」が含まれる行（集計行）を除外して、純粋なデータ行のみを残す
    df_clean = df_data[~df_data["出発空港"].astype(str).str.contains("小計：")].copy()
    # 6. 不要な文字列スペース等のクレンジング（必要に応じて）
    df_clean["出発空港"] = df_clean["出発空港"].str.strip()
    # 7. 出力用データフレームの作成
    output_df = pd.DataFrame()
    #output_df = df_data.copy()  # 元のデータフレームをコピーして出力用に使用
    output_df['運航区分'] = ["SD(定期)"] * len(df_clean)
    
    # 8.便名から航空会社コードを抽出して一括変換（.apply を使用）
    output_df['航空会社2Lコード'] = df_clean["便名"].astype(str).str.strip().str[:2]
    
    output_df['便名'] = df_clean["便名"]
    output_df['出発空港'] = df_clean["出発空港"]
    output_df['到着空港'] = [jigyosho] * len(df_clean)
    output_df['便数'] = df_clean["Flight_Sum_件数"]
    output_df['貨物重量'] = df_clean["Flight_Sum_重量"]
    output_df['メール重量'] = [0] * len(df_clean)
    output_df['事業所'] = [jigyosho] * len(df_clean)
    # 9. 便名が空の行を削除して、純粋なデータ行のみを残す
    output_df = output_df.dropna(subset=["便名"]).copy()
    # 10. NaNを0に置換(便数、貨物重量、メール重量)
    output_df['便数'] = output_df['便数'].fillna(0)
    output_df['貨物重量'] = output_df['貨物重量'].fillna(0)
    output_df['メール重量'] = output_df['メール重量'].fillna(0)
    #print(output_df.head(20))  # デバッグ用に先頭20行を表示
    results = []
    results.append(ReadResult(df=output_df,layout=Layout_type.MONTHLY_CARGO2.value))
    return results

def layout_departure_cargo(df) -> pd.DataFrame:
    # 1. 全体で共通の情報（ヘッダー部分）を取得
    jigyosho = df.iloc[1, 1].strip()[-3:]   # B列: 事業所コード (0:A, 1:B, 2:C)右3文字取得
    # 2. データ部分の抽出（13行目以降）と列名の設定
    df_data  = df.iloc[13:].copy()
    df_data.columns =[
                "NOName",
                "到着空港",
                "便名",                      #3列
                "Domestic_Rev_件数",         #4列
                "Domestic_Rev_個数",         #5列
                "Domestic_Rev_重量",         #6列
                "Domestic_NonRev_件数",      #7列
                "Domestic_NonRev_個数",      #8列
                "Domestic_NonRev_重量",      #9列
                "Domestic_Sum_件数",         #10列
                "Domestic_Sum_個数",         #11列
                "Domestic_Sum_重量",         #12列
                "International_Rev_件数",    #13列
                "International_Rev_個数",    #14列
                "International_Rev_重量",    #15列
                "International_NonRev_件数", #16列
                "International_NonRev_個数", #17列
                "International_NonRev_重量", #18列
                "International_Sum_件数",    #19列
                "International_Sum_個数",    #20列
                "International_Sum_重量",    #21列
                "Flight_Sum_件数",           #22列
                "Flight_Sum_個数",           #23列
                "Flight_Sum_重量",           #24列
                ] 
    # 3. 空白行や「合計：」より後の不要なフッター行を削除するためのトリミング
    # 「合計：」という文字が含まれるインデックスを取得
    total_row_idx = df_data[df_data["到着空港"].astype(str).str.contains("合計：")].index
    if not total_row_idx.empty:
        # 最初の「合計：」が出現した位置より前（上）だけを残す
        df_data = df_data.loc[:total_row_idx[0] - 1]
    # 3.5. 便名が空の行を削除
    df_data = df_data.dropna(subset=["便名"]).copy()    
    # 4. 到着空港列の空欄（NaN）を上の値で埋める（Forward Fill）
    df_data["到着空港"] = df_data["到着空港"].ffill()
    # 5. 「小計：」が含まれる行（集計行）を除外して、純粋なデータ行のみを残す
    df_clean = df_data.copy()
    # 6. 不要な文字列スペース等のクレンジング（必要に応じて）
    df_clean["到着空港"] = df_clean["到着空港"].str.strip()
    df_clean["便名"] = df_clean["便名"].astype(str).str.strip()
    # 7. 出力用データフレームの作成
    output_df = pd.DataFrame()

    output_df['運航区分'] = ["SD(定期)"] * len(df_clean)
    # 8.便名から航空会社コードを抽出して一括変換（.apply を使用）
    output_df['航空会社2Lコード'] = df_clean["便名"].astype(str).str.strip().str[:2]
    output_df['便名'] = df_clean["便名"]
    output_df['到着空港'] = df_clean["到着空港"]
    output_df['出発空港'] = [jigyosho] * len(df_clean)
    output_df['便数'] = df_clean["Flight_Sum_件数"]
    output_df['貨物重量'] = df_clean["Flight_Sum_重量"]
    output_df['メール重量'] = [0] * len(df_clean)
    output_df['事業所'] = [jigyosho] * len(df_clean)
    # 9. 便名が空の行を削除して、純粋なデータ行のみを残す
    output_df = output_df.dropna(subset=["便名"]).copy()
    # 10. NaNを0に置換(便数、貨物重量、メール重量)
    output_df['便数'] = output_df['便数'].fillna(0)
    output_df['貨物重量'] = output_df['貨物重量'].fillna(0)  
    output_df['メール重量'] = output_df['メール重量'].fillna(0)    
    #print(output_df.head(20))  # デバッグ用に先頭20行を表示 
    results = []
    results.append(ReadResult(df=output_df,layout=Layout_type.MONTHLY_CARGO2.value))
    return results

def layout_departure_mail(df) -> pd.DataFrame:
    # 1. 全体で共通の情報（ヘッダー部分）を取得
    jigyosho = df.iloc[0, 1].strip()[-3:]   # B列: 事業所コード (0:A, 1:B, 2:C)右3文字取得
    # 2. データ部分の抽出（11行目以降）と列名の設定
    df_data  = df.iloc[10:].copy()
    df_data.columns =[
                "NOName",
                "到着空港",
                "便名",             #3列
                "ML1_件数",         #4列
                "ML1_個数",         #5列
                "ML1_重量",         #6列
                "ML2_件数",         #7列
                "ML2_個数",         #8列
                "ML2_重量",         #9列
                "ML3_件数",         #10列
                "ML3_個数",         #11列
                "ML3_重量",         #12列
                "ML4_件数",         #13列
                "ML4_個数",         #14列
                "ML4_重量",         #15列
                "ML5_件数",         #16列
                "ML5_個数",         #17列
                "ML5_重量",         #18列
                "Flight_Sum_件数",  #19列
                "Flight_Sum_個数",  #20列
                "Flight_Sum_重量",  #21列
                ] 

    # 3. 空白行や「合計：」より後の不要なフッター行を削除するためのトリミング
    # 「合計：」という文字が含まれるインデックスを取得
    total_row_idx = df_data[df_data["到着空港"].astype(str).str.contains("合計：")].index
    if not total_row_idx.empty:
        # 最初の「合計：」が出現した位置より前（上）だけを残す
        df_data = df_data.loc[:total_row_idx[0] - 1]
    # 3.5. 便名が空の行を削除
    df_data = df_data.dropna(subset=["便名"]).copy()    
    # 4. 到着空港列の空欄（NaN）を上の値で埋める（Forward Fill）
    df_data["到着空港"] = df_data["到着空港"].ffill()
    # 5. 「小計：」が含まれる行（集計行）を除外して、純粋なデータ行のみを残す
    df_clean = df_data.copy()
    # 6. 不要な文字列スペース等のクレンジング（必要に応じて）
    df_clean["到着空港"] = df_clean["到着空港"].str.strip()
    df_clean["便名"] = df_clean["便名"].astype(str).str.strip()
    # 7. 出力用データフレームの作成
    output_df = pd.DataFrame()

    output_df['運航区分'] = ["SD(定期)"] * len(df_clean)
    # 8.便名から航空会社コードを抽出して一括変換（.apply を使用）
    output_df['航空会社2Lコード'] = df_clean["便名"].astype(str).str.strip().str[:2]
    output_df['便名'] = df_clean["便名"]
    output_df['到着空港'] = df_clean["到着空港"]
    output_df['出発空港'] = [jigyosho] * len(df_clean)
    output_df['便数'] = df_clean["Flight_Sum_件数"]
    output_df['貨物重量'] =  [0] * len(df_clean)
    output_df['メール重量'] =df_clean["Flight_Sum_重量"] 
    output_df['事業所'] = [jigyosho] * len(df_clean)
    # 9. 便名が空の行を削除して、純粋なデータ行のみを残す
    output_df = output_df.dropna(subset=["便名"]).copy()
    # 10. NaNを0に置換(便数、貨物重量、メール重量)
    output_df['便数'] = output_df['便数'].fillna(0)
    output_df['貨物重量'] = output_df['貨物重量'].fillna(0)  
    output_df['メール重量'] = output_df['メール重量'].fillna(0)    
    #print(output_df.head(20))  # デバッグ用に先頭20行を表示 
    results = []
    results.append(ReadResult(df=output_df,layout=Layout_type.MONTHLY_CARGO2.value))
    return results

def layout_arrival_mail(df) -> pd.DataFrame:
    # 1. 全体で共通の情報（ヘッダー部分）を取得
    jigyosho = df.iloc[1, 1].strip()[-3:]   # B列: 事業所コード (0:A, 1:B, 2:C)右3文字取得
    # 2. データ部分の抽出（11行目以降）と列名の設定
    df_data  = df.iloc[10:].copy()
    df_data.columns =[
                "NOName",
                "出発空港",
                "便名",             #3列
                "ML1_件数",         #4列
                "ML1_個数",         #5列
                "ML1_重量",         #6列
                "ML2_件数",         #7列
                "ML2_個数",         #8列
                "ML2_重量",         #9列
                "ML3_件数",         #10列
                "ML3_個数",         #11列
                "ML3_重量",         #12列
                "ML4_件数",         #13列
                "ML4_個数",         #14列
                "ML4_重量",         #15列
                "ML5_件数",         #16列
                "ML5_個数",         #17列
                "ML5_重量",         #18列
                "Flight_Sum_件数",  #19列
                "Flight_Sum_個数",  #20列
                "Flight_Sum_重量",  #21列
                ] 
    # 3. 空白行や「合計：」より後の不要なフッター行を削除するためのトリミング
    # 「合計：」という文字が含まれるインデックスを取得
    total_row_idx = df_data[df_data["便名"].astype(str).str.contains("合計：")].index
    if not total_row_idx.empty:
        # 最初の「合計：」が出現した位置より前（上）だけを残す
        df_data = df_data.loc[:total_row_idx[0] - 1]
    # 3.5. 便名が空の行を削除
    df_data = df_data.dropna(subset=["便名"]).copy()    
    # 4. 出発空港列の空欄（NaN）を上の値で埋める（Forward Fill）
    df_data["出発空港"] = df_data["出発空港"].ffill()
    # 5. 「小計：」が含まれる行（集計行）を除外して、純粋なデータ行のみを残す
    df_clean = df_data[~df_data["便名"].astype(str).str.contains("小計")].copy()
    # 6. 不要な文字列スペース等のクレンジング（必要に応じて）
    df_clean["出発空港"] = df_clean["出発空港"].str.strip()
    # 7. 出力用データフレームの作成
    output_df = pd.DataFrame()
    #output_df = df_data.copy()  # 元のデータフレームをコピーして出力用に使用
    output_df['運航区分'] = ["SD(定期)"] * len(df_clean)
    
    # 8.便名から航空会社コードを抽出して一括変換（.apply を使用）
    output_df['航空会社2Lコード'] = df_clean["便名"].astype(str).str.strip().str[:2]
    
    output_df['便名'] = df_clean["便名"]
    output_df['出発空港'] = df_clean["出発空港"]
    output_df['到着空港'] = [jigyosho] * len(df_clean)
    output_df['便数'] = df_clean["Flight_Sum_件数"]
    output_df['貨物重量'] =  [0] * len(df_clean)
    output_df['メール重量'] =df_clean["Flight_Sum_重量"] 
    output_df['事業所'] = [jigyosho] * len(df_clean)
    # 9. 便名が空の行を削除して、純粋なデータ行のみを残す
    output_df = output_df.dropna(subset=["便名"]).copy()
    # 10. NaNを0に置換(便数、貨物重量、メール重量)
    output_df['便数'] = output_df['便数'].fillna(0)
    output_df['貨物重量'] = output_df['貨物重量'].fillna(0)
    output_df['メール重量'] = output_df['メール重量'].fillna(0)
    #print(output_df.head(20))  # デバッグ用に先頭20行を表示
    results = []
    results.append(ReadResult(df=output_df,layout=Layout_type.MONTHLY_CARGO2.value))
    return results
