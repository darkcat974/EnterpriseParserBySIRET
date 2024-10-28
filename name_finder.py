import random
import time
from prettytable import PrettyTable
from tqdm import tqdm
import csv

bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]'

def phonetic_misspell(name):
    """Phonetically misspell a given name."""
    misspellings = {
        'a': ['e', 'i', 'o'],
        'e': ['a', 'i', 'y'],
        'i': ['e', 'y', 'a'],
        'o': ['a', 'u', 'e'],
        'u': ['o', 'y', 'a'],
        'c': ['k', 's'],
        's': ['z', 'c'],
        'y': ['i', 'e'],
        'h': [''],
        'l': ['r', 'u'],
        'r': ['l', 'w'],
        'n': ['m'],
        't': ['d', 'c']
    }
    
    # Randomly decide to apply a phonetic change
    new_name = list(name)
    for idx, char in enumerate(name):
        if char in misspellings and random.random() < 0.3:  # 30% chance to misspell
            new_name[idx] = random.choice(misspellings[char]) if misspellings[char] else char

    return ''.join(new_name)

def length_misspell(name):
    # Decide randomly whether to shorten or lengthen the name
    if random.choice([True, False]):  # Randomly choose to shorten or lengthen
        if len(name) > 1:  # Ensure we don't shorten names to empty strings
            # Remove a random character
            index_to_remove = random.randint(0, len(name) - 1)
            name = name[:index_to_remove] + name[index_to_remove + 1:]
    else:
        # Add a random character (for simplicity, just append a random letter)
        random_char = random.choice('abcdefghijklmnopqrstuvwxyz')
        index_to_insert = random.randint(0, len(name))  # Insert at a random position
        name = name[:index_to_insert] + random_char + name[index_to_insert:]
    return name

def brut_force(valide_names, teste_names):
    res = []
    table = PrettyTable()
    table.field_names = ["Valid Name", "Misspelled Name", "Similarity Score"]

    def generate_ngrams(name, n=2):
        """Generate n-grams from a given name."""
        return [name[i:i+n] for i in range(len(name) - n + 1)]

    def compare_names(name1, name2, n=2):
        """Compare two names using n-grams and return similarity score."""
        ngrams1 = set(generate_ngrams(name1, n))
        ngrams2 = set(generate_ngrams(name2, n))
        intersection = ngrams1.intersection(ngrams2)
        union = ngrams1.union(ngrams2)
        if not union:  # Avoid division by zero
            return 0.0
        similarity_score = len(intersection) / len(union)
        return similarity_score

    for valid, name in tqdm(zip(valide_names, teste_names),
                                total=len(valide_names),
                                bar_format=bar_format,
                                colour='blue'):
        similarity = compare_names(valid, name)
        res.append(similarity)
        table.add_row([valid, name, f"{similarity:.2%}"])  # Format as percentage
    return res

import nltk
from nltk import ngrams
from collections import Counter

def my_ngram(valide_names, teste_names):
    res = []
    table = PrettyTable()
    table.field_names = ["Valid Name", "Misspelled Name", "Similarity Score"]
    def generate_ngrams(name, n=2):
        return list(ngrams(name, n))

    def compare_names(name1, name2, n=2):
        ngrams1 = Counter(generate_ngrams(name1, n))
        ngrams2 = Counter(generate_ngrams(name2, n))
        
        intersection = sum((ngrams1 & ngrams2).values())
        union = sum((ngrams1 | ngrams2).values())
        
        return intersection / union if union > 0 else 0.0

    for valid, name in tqdm(zip(valide_names, teste_names),
                                total=len(valide_names),
                                bar_format=bar_format,
                                colour='white'):
        similarity = compare_names(valid, name)
        res.append(similarity)
        table.add_row([valid, name, f"{similarity:.2%}"])  # Format as percentage
    return res

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score

def skibidi_learn(valide_names, teste_names):
    res = []
    table = PrettyTable()
    table.field_names = ["Valid Name", "Misspelled Name", "Similarity Score"]
    def compare_names(name1, name2):
        vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 2))
        X = vectorizer.fit_transform([name1, name2]).toarray()
        return jaccard_score(X[0], X[1], average="micro")

    for valid, name in tqdm(zip(valide_names, teste_names),
                                total=len(valide_names),
                                bar_format=bar_format,
                                colour='red'):
        similarity = compare_names(valid, name)
        res.append(similarity)
        table.add_row([valid, name, f"{similarity:.2%}"])  # Format as percentage
    return res

from fuzzywuzzy import fuzz

def the_fuzzz(valide_names, teste_names):
    res = []
    table = PrettyTable()
    table.field_names = ["Valid Name", "Misspelled Name", "Similarity Score"]
    for valid, name in tqdm(zip(valide_names, teste_names),
                                total=len(valide_names),
                                bar_format=bar_format,
                                colour='yellow'):
        similarity = fuzz.ratio(valid, name) / 100
        res.append(similarity)
        table.add_row([valid, name, f"{similarity:.2%}"])  # Format as percentage
    return res

import textdistance

def the_lengther(names, misspells):
    res = []
    table = PrettyTable()
    table.field_names = ["Valid Name", "Misspelled Name", "Similarity Score"]
    for valid, name in tqdm(zip(names, misspells),
                                total=len(names),
                                bar_format=bar_format,
                                colour='green'):
        similarity = textdistance.jaccard(valid, name)
        res.append(similarity)
        table.add_row([valid, name, f"{similarity:.2%}"])  # Format as percentage

    return res

def overall_stats(names, misspelled_names, res_brut, res_ngram, res_skibidi, res_fuzzz, res_lengther):
    # Initialiser une liste pour stocker les moyennes
    moyennes = []
    table = PrettyTable()
    table.field_names = ["Valid Name", "Misspelled Name", "Similarity Score"]
    with open('results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Valid Name', 'Misspelled Name', 'Overall', 'Brut-Force', 'N-Gram', 'Skibidi', 'Fuzzy', 'Lengther'])
        # Boucler à travers les résultats de chaque programme
        for valid, name, b, n, s, f, l in tqdm(zip(names, misspelled_names, res_brut, res_ngram, res_skibidi, res_fuzzz, res_lengther), 
                                total=len(names),
                                bar_format=bar_format,
                                colour='magenta'):
            # Calculer la moyenne pour chaque ensemble de résultats
            moyenne = (b + n + s + f + l) / 5
            moyennes.append(moyenne)
            table.add_row([valid, name, f"{moyenne:.2%}"])  # Format as percentage
            writer.writerow([valid, name, f"{moyenne:.2%}", f"{b:.2%}", f"{n:.2%}", f"{s:.2f}", f"{f:.2%}", f"{l:.2%}"])
    return moyennes

def main():
    all_time_start = time.time()
    names = [
        "Emma", "Liam", "Olivia", "Noah", "Ava",
        "Oliver", "Sophia", "Elijah", "Isabella", "Lucas",
        "Mia", "Mason", "Amelia", "Logan", "Harper",
        "Ethan", "Evelyn", "Aiden", "Abigail", "James",
        "Ella", "Jacob", "Scarlett", "Michael", "Grace",
        "Alexander", "Chloe", "Daniel", "Lily", "Henry",
        "Aria", "Jackson", "Zoe", "Sebastian", "Stella",
        "Jack", "Hazel", "Samuel", "Layla", "David",
        "Ellie", "Joseph", "Natalie", "Charles", "Aurora",
        "Thomas", "Hannah", "Gabriel", "Lucy", "Caleb",
        "Brooklyn", "Isaiah", "Savannah", "Anthony", "Bella",
        "Christopher", "Claire", "Joshua", "Skylar", "Andrew",
        "Mila", "Christian", "Peyton", "Jonathan", "Lydia",
        "Dylan", "Ruby", "Levi", "Arianna", "Isaac",
        "Alice", "Lincoln", "Maya", "Charles", "Samantha",
        "Luke", "Victoria", "Owen", "Penelope", "Wyatt",
        "Serenity", "Hunter", "Caroline", "Adam", "Nova",
        "Julian", "Gianna", "Jaxon", "Everly", "Eli",
        "Faith", "Nicholas", "Kinsley", "Colton", "Lydia",
        "Weston", "Quinn", "Miles", "Ivy", "Asher"
    ]

    # Generate randomly misspelled names with both phonetic and length alterations
    misspelled_names = [
        length_misspell(phonetic_misspell(name)) for name in names
    ]

    print("------------------------------------brute force------------------------------------------")
    start_brut = time.time()
    res_brut = brut_force(names, misspelled_names)
    finish_brut = time.time()
    print("------------------------------------brute force------------------------------------------")
    print("---------------------------------------ngram---------------------------------------------")
    start_ngram = time.time()
    res_ngram = my_ngram(names, misspelled_names)
    finish_ngram = time.time()
    print("---------------------------------------ngram---------------------------------------------")
    print("---------------------------------------skibidy---------------------------------------------")
    start_skibidy = time.time()
    res_skibidi = skibidi_learn(names, misspelled_names)
    finish_skibidy = time.time()
    print("---------------------------------------skibidy---------------------------------------------")
    print("---------------------------------------fuzzz---------------------------------------------")
    start_fuzzz = time.time()
    res_fuzzz = the_fuzzz(names, misspelled_names)
    finish_fuzzz = time.time()
    print("---------------------------------------fuzzz---------------------------------------------")
    print("---------------------------------------lengther---------------------------------------------")
    start_lengther = time.time()
    res_lengther = the_lengther(names, misspelled_names)
    finish_lengther = time.time()
    print("---------------------------------------lengther---------------------------------------------")
    overall_stats(names, misspelled_names, res_brut, res_ngram, res_skibidi, res_fuzzz, res_lengther)
    all_time_end = time.time()
    print(f"timer bruteforce : {finish_brut - start_brut}")
    print(f"timer ngram : {finish_ngram - start_ngram}")
    print(f"timer skibidy : {finish_skibidy - start_skibidy}")
    print(f"timer fuzzz : {finish_fuzzz - start_fuzzz}")
    print(f"timer lengther : {finish_lengther - start_lengther}")
    print(f"finished in {all_time_end - all_time_start}sec")

if __name__ == "__main__":
    exit(main())
