from fpdf import FPDF
import os

def generate_incident_report(incident: dict) -> dict:
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add incident details to the PDF
        pdf.cell(200, 10, txt="Incident Report", ln=True, align='C')
        pdf.ln(10)  # Add a line break

        for key, value in incident.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

        os.makedirs("reports", exist_ok=True)  # Create a directory for reports if it doesn't exist


        # Save the PDF to a file
        report_filename = f"reports/incident_report_{incident.get('incident_id', 'unknown')}.pdf"
        pdf.output(report_filename)

        return {"success": True, "report_path": os.path.abspath(report_filename)}
    except Exception as e:
        return {"success": False, "message": str(e)}
