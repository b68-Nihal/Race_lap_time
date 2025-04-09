import pandas as pd
import os
import django
from django.db import transaction

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "race_management.settings")
django.setup()

from racers.models import Racer, Heat, Transponder, HeatAssignment

# Load the correct file
df = pd.read_csv("Transponder_Assigned_Heats.csv")
df.columns = [col.strip() for col in df.columns]  # normalize spacing

@transaction.atomic
def import_heat_assignments(dataframe):
    for index, row in dataframe.iterrows():
        try:
            category = row['Category'].strip()
            group = row['Group'].strip()
            name = row['Name'].strip()
            rider_number = int(row['Rider No'])
            heat_number = int(row['Heat'])
            transponder_id = str(row['Transponder']).strip()

            racer, _ = Racer.objects.get_or_create(
                name=name,
                rider_number=rider_number,
                category=category
            )

            heat, _ = Heat.objects.get_or_create(
                category=category,
                group=group,
                heat_number=heat_number
            )

            transponder, _ = Transponder.objects.get_or_create(
                transponder_id=transponder_id
            )

            HeatAssignment.objects.get_or_create(
                heat=heat,
                racer=racer,
                transponder=transponder
            )

            print(f"✅ Assigned {name} (#{rider_number}) to Heat {heat_number} with Transponder {transponder_id}")

        except Exception as e:
            print(f"❌ Error at row {index + 2}: {e}")

# Run the import
import_heat_assignments(df)
print("🏁 All heat assignments imported successfully.")
