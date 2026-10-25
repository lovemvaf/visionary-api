with open('scripts/generate_full_qa_guide.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace unescaped double quotes inside strings
text = text.replace('[Collection("IntegrationTests")]', '[Collection(\'IntegrationTests\')]')
text = text.replace('[Collection(\\"IntegrationTests\\")]', '[Collection(\'IntegrationTests\')]')

with open('scripts/generate_full_qa_guide.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Cleaned generate_full_qa_guide.py successfully.')
