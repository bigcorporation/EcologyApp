import json
import random
from datetime import datetime, timedelta

species_names = [
    "Pseudomys novaehollandiae",
    "Petrogale penicillata",
    "Litoria aurea",
    "Petaurus norfolcensis",
    "Dasyurus maculatus",
    "Thylacinus cynocephalus",
    "Vombatus ursinus",
    "Phascolarctos cinereus",
    "Macropus rufus",
    "Potorous tridactylus"
]

observers = [
    "John Smith",
    "FieldTech Services",
    "Alice Nguyen",
    "Bob Lee",
    "Jane Doe",
    "Wildlife Survey Team",
    "David Chen",
    "Laura Kim",
    "National Parks Service",
    "Emma Brown"
]

threat_statuses = [
    "Endangered",
    "Vulnerable",
    "Least Concern",
    "Near Threatened",
    "Critically Endangered"
]

def random_date(start_year=2018, end_year=2023):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_record():
    lat = round(random.uniform(-37.0, -28.0), 6)
    lon = round(random.uniform(150.0, 154.0), 6)
    return {
        "SpeciesName": random.choice(species_names),
        "Latitude": lat,
        "Longitude": lon,
        "DateObserved": random_date(),
        "Accuracy": random.randint(5, 100),
        "Observer": random.choice(observers),
        "ThreatStatus": random.choice(threat_statuses)
    }

mock_data = {
    "@odata.context": "https://mock.bionet.local/odata/$metadata#SpeciesSightings_CoreData",
    "value": [generate_record() for _ in range(200)]
}

with open("mock.json", "w") as f:
    json.dump(mock_data, f, indent=2)

print("Generated mock.json with 200 records.")