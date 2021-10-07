#!/usr/bin/env python3

import os
import json
import pandas as pd

with open('config.json', encoding='utf8') as config_json:
    config = json.load(config_json)

results = {"errors": [], "warnings": []}

directions = None

if not os.path.exists("secondary"):
    os.mkdir("secondary")

if not os.path.exists("output"):
    os.mkdir("output")

#try loading the timeseries.tsv as tsv
df = pd.read_csv(config['tsv'], sep='\t')
print("dumping head of the timeseries.tsv.gz");
print(df.head())

#try loading timeseries.json
try:
    with open(config['json']) as columns_json:
        columns = json.load(columns_json)

    #check to see if all columns are defined in timeseries.json
    if columns:
        for col in df:
            if not col in columns:
                results["warnings"].append("column:'%s' is not defined in timeseries.json" % col)

except json.decoder.JSONDecodeError:
    results["errors"].append("failed to parse timeseries.json")

#bypass inputs
if os.path.lexists("output/timeseries.tsv.gz"):
    os.remove("output/timeseries.tsv.gz")
os.symlink("../"+config['tsv'], "output/timeseries.tsv.gz")

if os.path.lexists("output/timeseries.json"):
    os.remove("output/timeseries.json")
os.symlink("../"+config['json'], "output/timeseries.json")

with open("product.json", "w") as fp:
    json.dump(results, fp)

if len(results["errors"]) > 0 or len(results["warnings"]) > 0:
    print(results)

print("done");
