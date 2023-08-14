def extract_group_ids(filename):
    group_ids = set()
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                group_id_part = parts[0].strip()
                value_part = parts[1].strip()
                if group_id_part.startswith('"group_id"') and value_part.startswith('"'):
                    group_id = group_id_part.split('"')[1]
                    value = value_part.split('"')[1]
                    group_ids.add((group_id, value))
    
    return group_ids

def save_unique_group_ids(group_ids, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as f:
        for group_id, value in group_ids:
            f.write(f'{value}\n')

if __name__ == '__main__':
    origin_filename = 'origin_data.txt'
    output_filename = 'list.txt'
    
    extracted_group_ids = extract_group_ids(origin_filename)
    save_unique_group_ids(extracted_group_ids, output_filename)
    
    print(f"Extracted and saved {len(extracted_group_ids)} unique group IDs to {output_filename}.")
