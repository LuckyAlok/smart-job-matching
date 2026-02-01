
# Removing reportlab import

# We might not have reportlab. 
# Check if we can use FPDF or just raw text.
# Actually, the user environment has 'PyPDF2'.
# But to create a PDF with text from scratch using PyPDF2 is not straightforward (it's mostly for manipulation).
# 
# Let's try to create a PDF using a raw valid string which is simpler and less error prone than base64 if I get the offsets right.
# But offsets are hard.

# Let's try to use a valid Base64 of a simple PDF containing "Python Developer Skills: Python, FastAPI, SQL"

import base64

# This is a base64 encoded PDF that contains: "Resume. Skills: Python, FastAPI, SQL."
# I'll use a reliable source or just a known good one.
# For now, I will try a different simple PDF base64.

pdf_content = b"""%PDF-1.7
1 0 obj
<</Type/Catalog/Pages 2 0 R>>
endobj
2 0 obj
<</Type/Pages/Kids[3 0 R]/Count 1>>
endobj
3 0 obj
<</Type/Page/Parent 2 0 R/MediaBox[0 0 595 842]/Resources<</Font<</F1 4 0 R>>>>/Contents 5 0 R>>
endobj
4 0 obj
<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>
endobj
5 0 obj
<</Length 44>>
stream
BT
/F1 24 Tf
100 700 Td
(Skills: Python, FastAPI, SQL) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000060 00000 n
0000000117 00000 n
0000000262 00000 n
0000000331 00000 n
trailer
<</Size 6/Root 1 0 R>>
startxref
426
%%EOF
"""

with open("dummy_resume.pdf", "wb") as f:
    f.write(pdf_content)

print("Created dummy_resume.pdf with text: Skills: Python, FastAPI, SQL")
