import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from prettytable import PrettyTable
from tqdm import tqdm
import random
import csv
import gc
import psutil
from nltk import ngrams
from collections import Counter

def my_ngram(valide_name, teste_name):
    def generate_ngrams(name, n=2):
        return list(ngrams(name, n))

    def compare_names(name1, name2, n=2):
        ngrams1 = Counter(generate_ngrams(name1, n))
        ngrams2 = Counter(generate_ngrams(name2, n))
        intersection = sum((ngrams1 & ngrams2).values())
        union = sum((ngrams1 | ngrams2).values())
        del ngrams1, ngrams2
        return intersection / union if union > 0 else 0.0
    return compare_names(valide_name, teste_name)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score

def skibidi_learn(valide_name, teste_name):
    def compare_names(name1, name2):
        vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 2))
        X = vectorizer.fit_transform([name1, name2]).toarray()
        return jaccard_score(X[0], X[1], average="micro")
    return compare_names(valide_name, teste_name)

from fuzzywuzzy import fuzz

def the_fuzzz(valide_name, teste_name):
    return fuzz.ratio(valide_name, teste_name) / 100

import textdistance

def the_lengther(valide_name, test_name):
    return textdistance.jaccard(valide_name, test_name)


def monitor_memory(threshold=0.7):
    while True:
        mem = psutil.virtual_memory()
        if mem.percent > threshold * 100:
            print("Memory limit exceeded! Performing cleanup...")
            gc.collect()  # Force garbage collection
        time.sleep(1)  # Check memory every second


import threading

# Create a lock for thread-safe file writing
write_lock = threading.Lock()

def process_pair(name, to_find, good, bad):
    n = my_ngram(name, to_find)
    s = skibidi_learn(name, to_find)
    f = the_fuzzz(name, to_find)
    l = the_lengther(name, to_find)
    moyenne = (n + s + f + l) / 4
    result = {'name': name, 'to_find': to_find, 'moyenne': moyenne}
    del n, s, f, l, moyenne

    category = None
    if 0 <= moyenne < 33.7:
        category = 'no_chance'
    elif 33.7 <= moyenne < 65:
        category = 'probable'
    elif 65 <= moyenne < 100:
        category = 'valid'

    # Prepare the output row based on category
    output_row = [
        good["CT_Siret"][good['CT_Intitule'] == name].values[1],
        good["CT_Num"][good['CT_Intitule'] == name].values[1],
        good["CT_Intitule"][good['CT_Intitule'] == name].values[1],
        good["DB_NAME"][good['CT_Intitule'] == name].values[1],
        bad["CT_Siret"][bad['CT_Intitule'] == to_find].values[1],
        bad["CT_Num"][bad['CT_Intitule'] == to_find].values[1],
        bad["CT_Intitule"][bad['CT_Intitule'] == to_find].values[1],
        bad["DB_NAME"][bad['CT_Intitule'] == to_find].values[1]
    ]

    # Write to the appropriate file based on category
    with write_lock:  # Acquire the lock before writing
        with open(f'{category}.csv', mode='a', newline='') as df:
            writer = csv.writer(df)
            writer.writerow(output_row)
    del output_row
    return category, result

def main():
    all_time_start = time.time()
    good = pd.read_csv('client_good_siret.csv')
    bad = pd.read_csv('client_bad_siret.csv')
    colors = ["blue", "red", "white", "green", "yellow"]
    header = [
        "CT_Siret_Good", "CT_Num_Good", "CT_Intitule_Good", "DB_NAME_Good",
        "CT_Siret_Found", "CT_Num_Found", "CT_Intitule_Found", "DB_NAME_Found"
    ]

    for category in ['valid', 'probable', 'no_chance']:
        with open(f'{category}.csv', mode='w', newline='') as df:
            writer = csv.writer(df)
            writer.writerow(header)

    monitor_thread = threading.Thread(target=monitor_memory)
    monitor_thread.daemon = True  # Allows thread to exit when main program does
    monitor_thread.start()
    with ThreadPoolExecutor() as executor:
        future_to_pair = {
            executor.submit(process_pair, name, to_find, good, bad): (name, to_find,  good, bad)
            for name in tqdm(good['CT_Intitule'], desc="Processing good", total=len(good), colour='magenta')
            for to_find in tqdm(bad['CT_Intitule'], desc="try_match", total=len(bad), colour=random.choice(colors))
        }

        for future in tqdm(as_completed(future_to_pair), total=len(future_to_pair), desc="Finalizing Results"):
            category, result = future.result()
            name, to_find = future_to_pair[future]
            print(f"result[{result}]: {category} for {name} and {to_find}")
            del category, result

    all_time_end = time.time()
    print("timer :", all_time_end - all_time_start)
    del all_time_end, all_time_start, good, bad, colors, header

if __name__ == "__main__":
    main()
