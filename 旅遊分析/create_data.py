import pandas as pd
import random
from datetime import datetime, timedelta

# 1. 設定資料筆數
num_rows = 300

# 2. 定義資料庫 (景點、縣市、區域)
spots_data = {
    "北部": {
        "台北市": ["台北101", "故宮博物院", "大稻埕", "陽明山", "士林夜市", "木柵動物園"],
        "新北市": ["九份老街", "淡水漁人碼頭", "野柳地質公園", "平溪放天燈", "十分瀑布"],
        "宜蘭縣": ["礁溪溫泉", "羅東夜市", "太平山", "蘭陽博物館", "梅花湖"],
        "桃園市": ["大溪老街", "石門水庫", "Xpark"],
        "新竹縣": ["六福村", "司馬庫斯", "內灣老街"]
    },
    "中部": {
        "台中市": ["逢甲夜市", "高美濕地", "宮原眼科", "審計新村", "武陵農場"],
        "南投縣": ["日月潭", "清境農場", "溪頭自然教育園區", "九族文化村", "合歡山"],
        "彰化縣": ["鹿港老街", "八卦山大佛"],
        "苗栗縣": ["勝興車站", "龍騰斷橋", "大湖採草莓"]
    },
    "南部": {
        "台南市": ["安平古堡", "奇美博物館", "花園夜市", "四草綠色隧道", "赤崁樓"],
        "高雄市": ["駁二藝術特區", "西子灣", "旗津老街", "佛光山", "愛河"],
        "屏東縣": ["墾丁大街", "鵝鑾鼻燈塔", "國立海洋生物博物館", "小琉球"],
        "嘉義縣": ["阿里山森林遊樂區", "檜意森活村"]
    },
    "東部": {
        "花蓮縣": ["太魯閣國家公園", "七星潭", "東大門夜市", "瑞穗牧場", "清水斷崖"],
        "台東縣": ["伯朗大道", "三仙台", "知本溫泉", "多良車站", "鐵花村"]
    },
    "離島": {
        "澎湖縣": ["澎湖跨海大橋", "雙心石滬", "大菓葉玄武岩"],
        "金門縣": ["翟山坑道", "金門鎮總兵署"],
        "連江縣": ["馬祖藍眼淚", "芹壁聚落"]
    }
}

transport_options = ["飛機", "高鐵", "火車", "客運", "開車", "摩托車", "腳踏車"]
member_types = ["家庭", "情侶", "朋友", "公司", "個人"]

# 輔助函式：產生隨機日期
def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return (start + timedelta(seconds=random_second)).date()

# 3. 開始生成資料
data = []
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

print(f"正在生成 {num_rows} 筆旅遊數據...")

for _ in range(num_rows):
    # 隨機選擇區域、縣市、景點
    region = random.choice(list(spots_data.keys()))
    city = random.choice(list(spots_data[region].keys()))
    spot = random.choice(spots_data[region][city])
    
    # 決定成員類型與人數 (加入邏輯權重)
    member_type = random.choices(member_types, weights=[30, 20, 30, 10, 10])[0]
    if member_type == "個人":
        people = 1
    elif member_type == "情侶":
        people = 2
    elif member_type == "家庭":
        people = random.randint(3, 6)
    elif member_type == "朋友":
        people = random.randint(2, 8)
    else: # 公司
        people = random.randint(10, 40)
        
    # 決定交通工具 (加入邏輯：離島主要搭機/船，公司主要搭客運，遠程少騎車)
    if region == "離島":
        transport = "飛機"
    elif member_type == "公司":
        transport = "客運" # 遊覽車
    elif region in ["東部", "南部"] and random.random() > 0.7:
        transport = random.choice(["高鐵", "火車"]) # 遠程較高機率搭大眾運輸
    else:
        transport = random.choice(transport_options)
        
    # 旅遊天數
    days = random.choices([1, 2, 3, 4, 5], weights=[30, 45, 15, 5, 5])[0]
    
    # 計算花費 (模擬公式：單人日均 * 天數 * 人數 + 交通)
    # 根據成員類型調整日均消費
    base_daily_cost = random.randint(1500, 3500)
    if member_type == "家庭": base_daily_cost += 500 # 家庭通常住好一點
    if member_type == "個人": base_daily_cost -= 300 # 背包客省一點
    
    transport_cost_per_person = 0
    if transport == "飛機": transport_cost_per_person = 4500
    elif transport == "高鐵": transport_cost_per_person = 2800
    elif transport == "開車": transport_cost_per_person = 600
    elif transport == "火車": transport_cost_per_person = 800
    else: transport_cost_per_person = 300
    
    total_cost = (base_daily_cost * days * people) + (transport_cost_per_person * people)
    total_cost = int(total_cost * random.uniform(0.95, 1.05)) # 加入隨機波動
    
    # 日期與保險
    travel_date = random_date(start_date, end_date)
    has_insurance = "有" if (people > 3 or days > 2 or member_type=="公司") else random.choice(["有", "無"])
    
    # 若有保險，將保費(假設每人200)加入總花費
    if has_insurance == "有":
        total_cost += (200 * people)

    data.append([spot, city, region, days, travel_date, transport, people, member_type, total_cost, has_insurance])

# 4. 建立 DataFrame 並存檔
df = pd.DataFrame(data, columns=["景點", "景點縣市", "區域", "旅遊天數", "旅遊日期", "交通工具", "旅遊人數", "成員類型", "總花費", "保險"])

# 設定檔案名稱
filename = "taiwan_tourism_analysis.csv"

# 輸出成 CSV 檔案 (encoding='utf-8-sig' 是為了讓 Excel 開啟時中文不亂碼)
df.to_csv(filename, index=False, encoding='utf-8-sig')

print(f"成功！已產生 {num_rows} 筆資料，並儲存為檔案：{filename}")
print("前 5 筆資料預覽：")
print(df.head())