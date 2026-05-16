import PyPDF4
import json
pdf_file = open('FORM16.pdf', 'rb')
pdf_reader = PyPDF4.PdfFileReader(pdf_file)

text = ''
for page in pdf_reader.pages:
    text += page.extractText()

# keyword = 'PAN of the Employee'

lines = text.split('\n')
# filtered_lines = {line for line in lines if keyword in line}

# for line in filtered_lines:
#     print(line)

employer_name = ' '.join(lines[5:10])
employee_name = ' '.join(lines[12:15])

# print(lines[4], '-----',employer_name)   
# print(lines[11], '----------', employee_name)   

# print(lines[15] ,'-------', lines[16])  
# print(lines[17] ,'-------', lines[18])  
# print(lines[19], '------', lines[20])   

# print(lines[38], '------', lines[64])   
# print(lines[40], '------', lines[65])  
# print(lines[42], '------', lines[66])   
 

# print(lines.index('158592.00'))

d = {

    lines[4]:employer_name,
    lines[11]:employee_name,

    lines[15]:lines[16],
    lines[17]:lines[18],
    lines[19]:lines[20],

    lines[38]:lines[64],
    lines[40]:lines[65],
    lines[42]:lines[66],
}
# print((d))

json_string = json.dumps(d)
print((json_string))

pdf_file.close()
