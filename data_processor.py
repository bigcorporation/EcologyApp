import json
from datetime import datetime
from filters import (
    filter_accuracy,
    filter_date,
    filter_latitude,
    filter_longitude,
    filter_threatstatus
)

filtered_data = []
removed_data = []

data = json.load(open("mock.json","r"))

for record in data["value"]:

    if (filter_latitude(record) and 
        filter_longitude(record) and 
        filter_accuracy(record) and 
        filter_threatstatus(record) and 
        filter_date(record)):
        filtered_data.append(record)
    else:
        removed_data.append(record)

relevant_species = [each.get("SpeciesName", "Unkown") for each in filtered_data]

irrelevant_species = [each.get("SpeciesName", "Unkown") for each in removed_data]

print(f'✅ These species observations were relevant: {sorted(relevant_species)}')
print(f'❌ These species are likely irrelevant: {sorted(irrelevant_species)}')



