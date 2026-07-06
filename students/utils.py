import pandas as pd
from .models import Student

def import_students_from_excel(file):
    df = pd.read_excel(file)

    for _, row in df.iterrows():
        Student.objects.get_or_create(
            name=row["Name"],
            email=row["Email"],
            phone=str(row["Phone"]),
            dob=row["Date of Birth"],
            gender=row["Gender"],
            address=row["Address"],
            course=row["Course"],
        )