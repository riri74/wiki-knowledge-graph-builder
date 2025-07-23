import os
import re

def load_text(filepath):
    with open(filepath, 'r',  encoding='utf-8') as file:
        content = file.read()
        return content
    

def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)  # Remove citations like [1]
    text = re.sub(r'\([A-Za-z\s,]+(?:\d{4})\)', '', text)  # Remove (Author, 2020)
    text = re.sub(r'\^\d+', '', text)  # Remove ^12
    text = re.sub(r'(?i)\b(references|abstract|introduction|conclusion)\b\s*\n?', '', text)  # Section titles
    text = re.sub(r'^={2,}.*?={2,}$', '', text, flags=re.MULTILINE)  # Wikipedia-style headings
    text = re.sub(r'\n{2,}', '\n', text)  # Collapse multiple newlines
    return text.strip()



def save_text(text, filepath):
    with open(filepath, 'w',  encoding='utf-8') as file:
        file.write(text)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # raw files
    raw_lakshmi = os.path.normpath(os.path.join(base_dir, '..', 'data', 'raw', 'lakshmi.txt'))
    raw_ai = os.path.normpath(os.path.join(base_dir, '..', 'data', 'raw', 'ai.txt'))

    # processed files
    proc_lakshmi = os.path.normpath(os.path.join(base_dir, '..', 'data', 'processed', 'lakshmi.txt'))
    proc_ai = os.path.normpath(os.path.join(base_dir, '..', 'data', 'processed', 'ai.txt'))

    # Load -> Clean -> Save
    text1 = load_text(raw_lakshmi)
    cleaned1 = clean_text(text1)
    save_text(cleaned1, proc_lakshmi)

    text2 = load_text(raw_ai)
    cleaned2 = clean_text(text2)
    save_text(cleaned2, proc_ai)

if __name__ == '__main__':
    main()
