import pandas as pd
from .models import Disease

def import_diseases():
    file = "diseases.xlsx"

    data = pd.read_excel(file)

    print("Total diseases found:", len(data))

    for _, row in data.iterrows():
        Disease.objects.create(
            name=str(row['name']),
            symptoms=str(row['symptoms']),
            precaution=str(row['precaution'])
        )

    print("All diseases imported successfully")
