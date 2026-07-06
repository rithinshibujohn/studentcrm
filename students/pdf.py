from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from .models import Student

def generate_student_pdf(response):

    pdf = SimpleDocTemplate(response)

    data = [
        [
            "Name",
            "Email",
            "Phone",
            "Course",
            "Gender",
        ]
    ]

    students = Student.objects.all()

    for student in students:

        data.append([
            student.name,
            student.email,
            student.phone,
            student.course,
            student.gender,
        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#4e73df")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,0),10),

    ]))

    pdf.build([table])