from pathlib import Path
import pandas as pd

base_dir = Path(__file__).parents[2]
train_data = pd.read_csv(base_dir / './data/olympic_data.csv')
events = pd.read_csv(base_dir / './data/summerOly_programs.csv', encoding='latin1')
athletes = pd.read_csv(base_dir / './data/summerOly_athletes.csv')
medals = pd.read_csv(base_dir / './data/summerOly_medal_counts.csv')
hosts = pd.read_csv(base_dir / './data/summerOly_hosts.csv')

def train_dataset():
    return train_data

def events_dataset():
    return events

def athletes_dataset():
    return athletes

def medals_dataset():
    return medals

def hosts_dataset():
    return hosts

def get_base():
    return base_dir