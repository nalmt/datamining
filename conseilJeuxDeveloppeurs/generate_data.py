import csv


# Settings
data_to_ignore = ["Rank", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
lower_date = 1980

# Read the first dataset
columns_keys = None
data = []
print("Building dataset ...")

with open('DATA/vgsales.csv', mode='r') as infile:
    reader = csv.reader(infile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    for row in reader:
        if columns_keys is None:
            columns_keys = row
        else:
            dict = {}
            for index, key in enumerate(columns_keys):
                if key not in data_to_ignore:
                    dict[key] = row[index]
                    if "," in dict[key]:
                        dict[key] = "\"" + dict[key] + "\""
            data.append(dict)

# Complete first dataset using informations from the second
steam_column_keys = None
count = 0
with open('DATA/steam.csv', mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        if steam_column_keys is None:
            steam_column_keys = row
        else:
            dict = {}
            for index, key in enumerate(steam_column_keys):
                if key not in data_to_ignore:
                    dict[key] = row[index]

            # Find this game in our first dataset
            for data_elt in data:
                if data_elt["Name"].lower() == dict["name"]:
                    if data_elt["Year"] == "N/A":
                        data_elt["Year"] = dict["release_date"].split("-")[0]
        count += 1

filtered_data = filter((lambda data_row: True if data_row["Year"] != "N/A" and int(data_row["Year"]) >= lower_date else False),
              data)
data = [data_row for data_row in filtered_data]

print("Saving dataset ...")
output_file = open("DATA/data_output.csv", "w")
output_file.write(",".join(data[0].keys()))
output_file.write("\n")
for element in data:
    # write line to output file
    line = ",".join([str(val) for val in element.values()])
    output_file.write(line)
    output_file.write("\n")
output_file.close()