import csv
from datetime import datetime

""""
[0]  -> number
[1]  -> timestamp(datetime)
[2]  -> string
[3]  -> string
[4]  -> string
[5]  -> string
[6]  -> string
[7]  -> string
[8]  -> float
[9]  -> float
[10] -> float
[11] -> string
[12] -> int
[13] -> string
[14] -> string
[15] -> string
[16] -> string
[17] -> string
[18] -> string
[19] -> string

"""

def to_sql(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"

def normalize_line(line: list[str]) -> str:
    final_string = [0 for _ in range(20)]
    print("linha 8 -> ", line[8])
    final_string[0] = int(line[0])
    final_string[1] = str(line[1]).replace('"',"").replace("'","").replace('“',"")
    final_string[2] = str(line[2]).replace('"',"").replace("'","").replace('“',"")
    final_string[3] = str(line[3]).replace('"',"").replace("'","").replace('“',"")
    final_string[4] = str(line[4]).replace('"',"").replace("'","").replace('“',"")
    final_string[5] = str(line[5]).replace('"',"").replace("'","").replace('“',"")
    final_string[6] = str(line[6]).replace('"',"").replace("'","").replace('“',"")
    final_string[7] = str(line[7]).replace('"',"").replace("'","").replace('“',"")
    final_string[8] = float(str(line[8]).replace('"',"").replace("'","").replace(',', '.').replace('“',""))
    final_string[9] = float(str(line[9]).replace('"',"").replace("'","").replace(',', '.').replace('“',""))
    final_string[10] = float(str(line[10]).replace('"',"").replace("'","").replace(',', '.').replace('“',""))
    final_string[11] = float(str(line[11]).replace("%", "").replace('"',"").replace("'","").replace(',', '.').replace('“',""))
    final_string[12] = line[12]
    final_string[13] = float(str(line[13]).replace("%", "").replace('"',"").replace("'","").replace(',', '.').replace('“',""))
    final_string[14] = float(str(line[14]).replace("%", "").replace('"',"").replace("'","").replace(',', '.').replace('“',""))
    final_string[15] = float(str(line[15]).replace("MB", "").replace("GB", "").replace("TB", "").replace("KB", "").replace('"',"").replace("'","").replace(',', '.').replace('“',""))
    final_string[16] = float(str(line[16]).replace("MB", "").replace("GB", "").replace("TB", "").replace("KB", "").replace('"',"").replace("'","").replace(',', '.').replace('“',""))
    final_string[17] = float(str(line[17]).replace("MB", "").replace("GB", "").replace("TB", "").replace("KB", "").replace('"',"").replace("'","").replace(',', '.').replace('“',""))
    final_string[18] = float(str(line[18]).replace("MB", "").replace("GB", "").replace("TB", "").replace("KB", "").replace('"',"").replace("'","").replace(',', '.').replace('“',""))
    final_string[19] = float(str(line[19]).replace("sec", "").replace("min", "").replace("h", "").replace('"',"").replace("'","").replace(',', '.').replace('“',""))


    for value in final_string:
        print(value)

    return f"({','.join(to_sql(v) for v in final_string)})"


def convert_csv_to_db(csv_path: str) -> str:
    final_insert = ""
    with open(csv_path, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        reader.line_num
        for _, line in enumerate(reader):
            line_converted = line[0].split(",")
            final_insert += normalize_line(line_converted)+", \n"

    with open("output_mdn.txt", 'w') as f:
        f.write(final_insert)

    return final_insert
CSV_PATH = "./MDN - Comparison between translation models.csv"

print(convert_csv_to_db(CSV_PATH))