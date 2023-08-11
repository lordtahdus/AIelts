from unidecode import unidecode
import json

def remove_tone_marks(txt):
    return unidecode(txt)

def process_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]

    for item in data:
        item['completion'] = remove_tone_marks(item['completion'])

    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    input_file = "fine_tuning/train_tr_sample.jsonl"
    output_file = "fine_tuning/train_no_tone_sample.jsonl"

    process_jsonl(input_file, output_file)
    print("Conversion complete.")           