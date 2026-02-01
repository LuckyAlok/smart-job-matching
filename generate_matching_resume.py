
# Removing reportlab import

# We might not have reportlab. 
# Check if we can use FPDF or just raw text.

import base64

# Base64 for a PDF containing: "Resume. Skills: React, JavaScript, TypeScript, CSS, HTML, Node.js"
# This matches the Frontend Developer role perfectly.
# Using a dummy generated PDF base64 string that has text content.
# Since I can't generate a valid PDF with specific text easily without libraries, 
# I will use a very simple PDF structure with the text injected.

# This is a minimal PDF with the text "Skills: React, JavaScript, CSS, HTML"
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
<</Length 100>>
stream
BT
/F1 24 Tf
100 700 Td
(Resume Name: Demo User) Tj
0 -50 Td
(Skills: React, JavaScript, CSS, HTML, TypeScript) Tj
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
480
%%EOF
"""

with open("matching_resume.pdf", "wb") as f:
    f.write(pdf_content)

print("Created matching_resume.pdf")
