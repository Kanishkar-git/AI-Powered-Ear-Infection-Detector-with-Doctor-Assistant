"""PDF Report Generation Service"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

def generate_pdf_report(report_data, processed_image=None):
    """Generate PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Title
    elements.append(Paragraph("AI-ASSISTED EAR INFECTION DETECTION REPORT", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Report metadata
    elements.append(Paragraph(f"<b>Report Generated:</b> {report_data['report_date']}", styles['Normal']))
    elements.append(Paragraph(f"<b>Report ID:</b> {report_data.get('report_id', 'N/A')}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Patient Information
    elements.append(Paragraph("<b>PATIENT INFORMATION</b>", styles['Heading2']))
    patient_data = [
        ['Patient ID:', report_data['patient']['id']],
        ['Name:', report_data['patient']['name']],
        ['Age:', str(report_data['patient']['age'])],
        ['Gender:', report_data['patient']['gender']],
    ]
    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(patient_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Detection Results
    elements.append(Paragraph("<b>DETECTION RESULTS</b>", styles['Heading2']))
    for infection in report_data['detection']['infections']:
        elements.append(Paragraph(
            f"• <b>{infection['name']}</b> - Confidence: {infection['confidence']}", 
            styles['Normal']
        ))
    elements.append(Spacer(1, 0.3*inch))
    
    # Analysis sections
    analysis = report_data['analysis']
    
    if analysis.get('overview'):
        elements.append(Paragraph("<b>CLINICAL OVERVIEW</b>", styles['Heading2']))
        elements.append(Paragraph(analysis['overview'], styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
    
    if analysis.get('severity'):
        elements.append(Paragraph("<b>SEVERITY ASSESSMENT</b>", styles['Heading2']))
        elements.append(Paragraph(analysis['severity'], styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
    
    # Disclaimer
    elements.append(Spacer(1, 0.3*inch))
    disclaimer = ("This AI-generated report is for clinical support only. "
                 "It does NOT provide a medical diagnosis. "
                 "Consult a qualified ENT specialist for confirmation.")
    elements.append(Paragraph(f"<b>{disclaimer}</b>", styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer