import json
import re
import math

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def parse_manifest(file_path):
    valid_records = []
    
    # Regex pattern matching: [Date] || Cargo_ID :: Quantity >> Destination
    pattern = re.compile(r"^\[(.*?)\]\s*\|\|\s*(.*?)\s*::\s*(\d+)\s*>>\s*(.*)$")
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
                
            match = pattern.match(line)
            if match:
                date, cargo_id, weight_str, destination = match.groups()
                weight = float(weight_str)
                
                # Business Rule 1: Multiply Weight by 1.45 if destination contains 'Sector-7'
                if "Sector-7" in destination:
                    weight *= 1.45
                
                # Business Rule 2: Round to nearest whole number
                # (Using floor(x + 0.5) to ensure exact standard midpoint rounding)
                final_weight = math.floor(weight + 0.5)
                
                # Business Rule 2: If the final weight is a prime number, discard entirely
                if is_prime(final_weight):
                    continue
                
                valid_records.append({
                    "date": date,
                    "cargo_id": cargo_id,
                    "weight_in_kg": final_weight,
                    "destination": destination
                })
                
    return valid_records

if __name__ == "__main__":
    # Ensure manifest.txt is in the same folder
    records = parse_manifest("manifest.txt")
    
    # Target naming format: Task 1 - [Your Last Name] - Parser.json
    last_name = "LABH" 
    output_filename = f"Task 1 - {last_name} - Parser.json"
    
    with open(output_filename, "w") as f:
        json.dump(records, f, indent=4)
        
    print(f"Done! Created {output_filename} with {len(records)} valid records.")