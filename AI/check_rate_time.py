import warnings
warnings.filterwarnings('ignore')

import json
import pandas as pd
import csv

import torch
import torch.nn as nn
import pymysql

import argparse

from pytz import timezone
from datetime import datetime

from sqlalchemy import create_engine

from collections import defaultdict

def parse_arguments() :
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--target_start', type=str, default='2007-01-01', help='start date for the target period')
    parser.add_argument('--target_end', type=str, default='2024-03-01', help='End date for the target period')
    parser.add_argument('--word', type=str, default='attention', help='target_word')
    parser.add_argument('--interval', type=int, default=1, help='interval')

    args = parser.parse_args()
    return args

args = parse_arguments()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class RNN(nn.Module):    # Define the RNN model

    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(RNN, self).__init__()
        self.rnn = nn.RNN(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.rnn.num_layers, x.size(0), self.rnn.hidden_size).to(device)  # Move initial hidden state to device
        out, _ = self.rnn(x, h0)
        out = self.fc(out[:, -1, :])
        return out

model_rnn = RNN(input_size=1, hidden_size=128, num_layers=1, output_size=1).to(device)  # Move model to device

model_rnn.load_state_dict(torch.load('/home/kev/kev/models/model_rnn_state_dict.pth', map_location=device))

def show_time(str1) :
    now1 = datetime.now(timezone('Asia/Seoul'))
    now2 = str(now1.strftime('%Y.%m.%d - %H:%M:%S'))
    print('------------ ' + str1 + '_' + now2 + ' ------------')
    
def citation_list_interval(list1, int1) : # time interval 적용하여 간격에 따른 누적인용 리스트 

    # 인용일자가 적힌 리스트
    quote_dates = list1

    # 각 n개월 간격별 누적 인용 횟수를 저장할 딕셔너리
    quarterly_quotes = defaultdict(int)
    max_quotes = 0

    # 인용일자를 날짜 객체로 변환하여 처리
    for date_str in quote_dates:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        # 해당 날짜를 n개월 간격으로 변환하여 연도와 분기를 튜플로 저장
        year_quarter = (date.year, (date.month - 1) // int1 + 1)
        quarterly_quotes[year_quarter] += int(list1.get(date_str)) - max_quotes
        max_quotes = int(list1.get(date_str))
    
    # n개월 간격별로 누적 인용 횟수 리스트 생성
    accumulated_quotes = defaultdict(int)
    total_quotes = 0

    start_year = min(quarterly_quotes.keys())[0]
    start_quarter = min(quarterly_quotes.keys(), key=lambda x: (x[0], x[1]))[1]
    end_year = max(quarterly_quotes.keys())[0]
    end_quarter = max(quarterly_quotes.keys(), key=lambda x: (x[0], x[1]))[1]

    current_year = start_year
    current_quarter = start_quarter

    while (current_year, current_quarter) <= (end_year, end_quarter):
        total_quotes += quarterly_quotes[(current_year, current_quarter)]
        if len(str(current_quarter)) == 1 : 
            keys_name = f'{current_year}-0{current_quarter}'
        else : 
            keys_name = f'{current_year}-{current_quarter}'
        accumulated_quotes[keys_name] = total_quotes

        current_quarter += 1
        if current_quarter > (12//int1):
            current_year += 1
            current_quarter = 1
            
    return accumulated_quotes

def str_to_dict(str1) : 
    return json.loads(str1)

def dict_to_values(dict1) : 
    return list(dict1.values())

def get_model_score(model, values_list) : 

    texst_sequences = torch.tensor(values_list, dtype=torch.float32).unsqueeze(-1)  # Adding channel dimension
    texst_sequences1 = texst_sequences.unsqueeze(0).to(device)
    output_score = model(texst_sequences1).item()

    return round(output_score, 5)

sql_user = 'dohyun'
sql_password = 'Dhyoon96!'
sql_port = 3306

engine = create_engine(f'mysql+pymysql://{sql_user}:{sql_password}@223.130.141.170:{sql_port}/final_project')
conn = engine.connect()

db = pymysql.connect(
    host = '223.130.141.170',  # DATABASE_HOST
    port = int(sql_port),
    user = sql_user,  # DATABASE_USERNAME
    passwd = sql_password,  # DATABASE_PASSWORD
    db = 'final_project',  # DATABASE_NAME
    charset = 'utf8'
)

cursor = db.cursor() # db 연결 후 cursor 객체를 통한 상호작용 

target_word = args.word
citation_graph_sql = f"SELECT id, citation_graph FROM PaperInfo WHERE title LIKE '%{target_word}%' OR categories LIKE '%{target_word}%'"

citation_graph_list = pd.read_sql(citation_graph_sql, db)
print(target_word)
db.close()

target_start = args.target_start[:10]
target_end = args.target_end[:10]
interval = args.interval

show_time(f'Wait!! {interval}_interval citation convert start!!')

for i, data in enumerate(citation_graph_list['citation_graph']) : 
    data = json.loads(data)
    
    # 끝 처리 
    last_key = max(data.keys())
    last_value = data[last_key]

    if target_end not in data.keys() : 
        data[target_end] = last_value

    # 시작 처리 
    data[target_start] = 0
    data = dict(sorted(data.items()))

    if min(data.keys()) != target_start : 

        previous_key = None
        for key in data.keys():
            if key == target_start : 
                data[key] = data[previous_key]
                break
            previous_key = key

        to_remove = [key for key in data if key < target_start]
        for key in to_remove:
            del data[key] 

    data = citation_list_interval(data, interval)
    citation_graph_list.loc[i, f'citation_graph_interval'] = json.dumps(data) 
    
    if (i+1)%10000 == 0 : 
        show_time(f'Wait!! {i}th {interval}_interval citation convert Done!!')

show_time(f'Wait!! {interval}_interval citation convert Done!!')

citation_graph_list['citation_graph_interval'] = citation_graph_list['citation_graph_interval'].apply(str_to_dict)
citation_graph_list['citation_values'] = citation_graph_list['citation_graph_interval'].apply(dict_to_values)

print('data_len', len(citation_graph_list))

dict_keys = list(citation_graph_list.loc[0, 'citation_graph_interval'].keys())

# 파일명 설정
filename = f'/home/kev/kev/csv_files/model_rate_{target_word}.csv'

# 헤더
header = ['times', 'rate_values', 'rate_models', 'targets_id', 'values_id', 'models_id']

# CSV 파일 열기
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)    
    # 헤더 쓰기
    writer.writerow(header)

    for i in range(1, len(dict_keys)) : # 1, 2007-02 

        values_target = defaultdict(int)
        values_dict = defaultdict(int)
        values_model = defaultdict(int)

        keys_t0 = dict_keys[i-1]
        keys_t1 = dict_keys[i]
        
        print('t0', keys_t0)
        print('t1', keys_t1)

        for j in range(len(citation_graph_list)) : 
            
            model_list = citation_graph_list.loc[j, 'citation_values'][:i]
            values_dict_list = citation_graph_list.loc[j, 'citation_graph_interval'] 

            id = citation_graph_list.loc[j, 'id'] 

            # 데이터, 모델 dict 선언
            values_target[id] = values_dict_list.get(keys_t0)
            values_dict[id] = values_dict_list.get(keys_t1) 
            values_model[id] = get_model_score(model_rnn, model_list)
            
            sorted_dict_targets = sorted(values_target.items(), key = lambda item: item[1], reverse = True)      
            sorted_dict_values = sorted(values_dict.items(), key = lambda item: item[1], reverse = True)
            sorted_dict_models = sorted(values_model.items(), key = lambda item: item[1], reverse = True)

            sorted_targets_10 = [a[0] for a in sorted_dict_targets][:10]    
            sorted_values_10 = [a[0] for a in sorted_dict_values][:10]  
            sorted_models_10 = [b[0] for b in sorted_dict_models][:10]

            target = set(sorted_targets_10) 
            models = set(sorted_values_10) 
            values = set(sorted_models_10) 
 
            answer_rate_values = (len(target) - len(target-values)) / len(target) * 100
            answer_rate_models = (len(target) - len(target-models)) / len(target) * 100

        writer.writerow([keys_t1, answer_rate_values, answer_rate_models, sorted_targets_10, sorted_values_10, sorted_models_10])



# t시점 top-k => 그대로 들고왔을 떄 t+1시점 top-k와의 비교를 통한 정답률 1
# t시점 top-k => 모델 예측을 통한 t+1시점 top-k와의 비교를 통한 정답률 2
        
        


