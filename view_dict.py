import json

def load_dict(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_keys(file_a, file_b):
    dict_a = load_dict(file_a)
    dict_b = load_dict(file_b)
    
    keys_a = set(dict_a.keys())
    keys_b = set(dict_b.keys())
    
    diff_keys = keys_a - keys_b
    
    print("Keys in A but not in B:", diff_keys)

# Thay 'a.json' và 'b.json' bằng đường dẫn thực tế của bạn
compare_keys(r"C:\Users\HUNG\Downloads\demo_view\demo_view_dir\docs_demo.json", r"C:\Users\HUNG\Downloads\demo_view\demo_view_dir\edu_dict_demo.json")
