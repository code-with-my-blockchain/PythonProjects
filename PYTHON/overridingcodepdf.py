import PyPDF2
import os

merger = PyPDF2.PdfWriter()

files = [file for file in os.listdir() if file.endswith(".pdf")]

for pdf in files:
    merger.append(pdf)
    print(f"{pdf} has been added!")

merger.write("My_Merged_File.pdf")
merger.close()

print("Congratulations! your files has been merged successfully.")