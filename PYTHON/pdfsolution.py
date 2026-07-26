import pypdf
import os

merger = pypdf.PdfWriter()

files = [file for file in os.listdir() if file.endswith(".pdf")]

for pdf in files:
  
    if pdf != "merged-pdf.pdf":
        merger.append(pdf)
        print(f"Merged: {pdf}")

merger.write("merged-pdf.pdf")
merger.close()
print("Success! Sab PDFs merge ho gayi hain.")
