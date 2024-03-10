from tabula.io import read_pdf
import datetime
import csv
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def load_data_from_PDF(pdf):
    tables = read_pdf(pdf, pages='all')
    subjects = set()
    teachers = set()
    lab_rooms = set()
    df = tables[2]
    subs = df.iloc[:, 0].values
    for i in subs:
        if isinstance(i, str):
            subjects.add(i)
    teach = df.iloc[:, 1].values
    for i in teach:
        if isinstance(i, str):
            teachers.add(i)
    sub = df.iloc[:, 2].values
    for i in sub:
        if isinstance(i, str):
            if i != 'SUBJECT':
                if len(i) > 2:
                    subjects.add(i)
    teach = df.iloc[:, 3].values
    for i in teach:
        if isinstance(i, str) and i != 'STAFF':
            teachers.add(i)
    labs = df.iloc[:, 4].values
    for i in labs:
        if isinstance(i, str) and i != 'LAB':
            lab_rooms.add(i)
    subjects.add(tables[4].columns[3])
    df = tables[4]
    teach = df.iloc[:, 5].values
    for i in teach:
        if isinstance(i, str):
            teachers.add(i)
    rooms = df.iloc[:, 6].values
    for i in rooms:
        if isinstance(i, str):
            lab_rooms.add(i)
    df = tables[1]
    return subjects, lab_rooms, teachers

def make_pdf(class_name,column,table,timings):
        try: 
            export_data=[]
            csv_file = 'temp_data.csv'
            for row in range(1,len(table)+1):
                if(row==3 or row==5):
                    export_data.append(["Break"])
                l1=[timings[((row-1)%6)],str(table[row][column].label1._text)]
                l2=['',str(table[row][column].label2._text)]
                l3=['',str(table[row][column].label3._text)]
                export_data.append(l1)
                export_data.append(l2)
                export_data.append(l3)
            export_data.insert(0,['Timing','Monday','Tuesday','Wednesday','Thursday','Friday'])
            with open(csv_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for sublist in export_data:
                    writer.writerow(sublist)
            data = []
            with open(csv_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            pdf_file = f'outputs/Time_Table_{timestamp}.pdf'
            doc = SimpleDocTemplate(pdf_file, pagesize=landscape(letter))
            table = Table(data)
            table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#4bcffa'),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),  # Header row text color
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header row font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 15),  # Header row bottom padding
            ('BACKGROUND', (0, 1), (-1, -1), '#EAEAEA'),  # Other row background color
            ('GRID', (0, 0), (-1, -1), 1, '#000000'),  # Grid color
            ('GRID', (0, 0), (-1, 0), 1, '#000000'),  # Header row grid color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignment
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Other row font
            ('FONTSIZE', (0, 1), (-1, -1), 10),  # Other row font size
            ('LEFTPADDING', (0, 0), (-1, -1), 3),  # Cell left padding
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),  # Cell right padding
            ('TOPPADDING', (0, 0), (-1, -1), 3),  # Cell top padding
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),  # Cell bottom padding
            ('SPAN', (0, 7), (5, 7)),
            ('SPAN', (0, 14), (5, 14)),
            ('BACKGROUND', (0, 7), (5, 7), '#B9E9FC'),  # Break Color
            ('BACKGROUND', (0, 14), (5, 14), '#B9E9FC'),  # Break Color
            ('FONTNAME', (0, 7), (5, 7), 'Helvetica-Bold'),  # Break
            ('FONTNAME', (0, 14), (5, 14), 'Helvetica-Bold'),  
            ]))
            
            sample_style_sheet = getSampleStyleSheet()
            paragraph_1 = Paragraph("----------------------------------------"+class_name+" Time-Table"+"----------------------------------------", sample_style_sheet['Heading1'])
            doc.title='Time Table'
            doc.build([paragraph_1,table])
            return "Success"
        except Exception:
            return None

