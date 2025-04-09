import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "race_management.settings")
django.setup()

from racers.models import Racer, Group

df = pd.read_excel("Race_Entry_List.xlsx")

for index, row in df.iterrows():
    try:
        name = row["Name"]
        rider_number = str(row["Rider No"]).strip()
        category = row["Category"].strip()
        group_name = row["Group"].strip()

        # Get or create the Racer
        racer, created = Racer.objects.get_or_create(
            name=name,
            rider_number=rider_number,
            category=category,
        )

        # Get or create the Group
        group, _ = Group.objects.get_or_create(
            name=group_name,
            category=category,
        )

        # Add the Racer to the Group
        group.racers.add(racer)

        print(f"✅ Added {name} ({rider_number}) to Group {group_name} - {category}")

    except Exception as e:
        print(f"❌ Error at row {index + 2}: {e}")

print("\n🏁 Racer import completed.")
