import json
import re
from collections import defaultdict
from difflib import SequenceMatcher

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_last_raw_edus(file_data, is_file2=False):
    """Trích xuất raw_edu của secid hoặc sentid cuối cùng trong từng phần (section), với việc tăng dần secid/sentid sau mỗi phần."""
    result = defaultdict(set)
    for article_id, content in file_data.items():
        # Chuẩn hóa article_id nếu là file 2
        normalized_id = re.sub(r"_[^_]+$", "", article_id) if is_file2 else article_id
        
        section_last_edus = set()
        secid_offset = 0  # Biến đếm để tăng secid/sentid sau mỗi section
        
        if is_file2:
            sections = content.get("cluster", {}).get("sects", [])
            for section in sections:
                secid_last_edus = {}
                for edu in section.get("edus", []):
                    secid = edu.get("sentid", 0) + secid_offset
                    secid_last_edus[secid] = edu.get("raw_edu")  # Ghi đè để lấy phần tử cuối
                section_last_edus.update(secid_last_edus.values())
                secid_offset += 10  # Tăng offset sau mỗi section
        else:
            for doc in content.get("docs", []):
                for section in doc.get("sents", []):
                    secid_last_edus = {}
                    for sent in section.get("sents", []):
                        secid = sent.get("secid", 0) + secid_offset
                        secid_last_edus[secid] = sent.get("raw_sent")  # Ghi đè để lấy phần tử cuối
                    section_last_edus.update(secid_last_edus.values())
                    secid_offset += 10  # Tăng offset sau mỗi section
        
        result[normalized_id] = section_last_edus
    
    return result

def similar(a, b):
    """Kiểm tra mức độ tương đồng giữa hai câu, trả về True nếu giống nhau ít nhất 80%."""
    return SequenceMatcher(None, a, b).ratio() >= 0.8

def compute_difference(file1_path, file2_path, output_path):
    file1_data = load_json(file1_path)
    file2_data = load_json(file2_path)
    
    file1_edus = extract_last_raw_edus(file1_data, is_file2=False)
    file2_edus = extract_last_raw_edus(file2_data, is_file2=True)
    
    result = {}
    for article_id, edus_file2 in file2_edus.items():
        edus_file1 = file1_edus.get(article_id, set())
        
        diff = []
        for edu2 in edus_file2:
            if not any(similar(edu2, edu1) for edu1 in edus_file1):
                diff.append(edu2)
        
        if diff:
            result[article_id] = diff
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

# Sử dụng chương trình
file1_path = r"D:\\evaluation\\train-cross\\test_input_abstract_conclusion_citing.json"  # Thay bằng đường dẫn thực tế
file2_path = r"C:\\Users\\HUNG\\Downloads\\demo_view\\demo_view_dir\\cluster_demo.json"  # Thay bằng đường dẫn thực tế
output_path = r"D:\\hoc3.2\\DataScience\\code\\materials-fa24\\check_diff.json"

compute_difference(file1_path, file2_path, output_path)
