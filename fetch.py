import wikipedia
import os

wikipedia.set_lang("en")

page1 = wikipedia.page("Lakshmi")
page2 = wikipedia.page("Artificial Intelligence")

lakshmi_text = page1.content
ai_text = page2.content

# Define base_dir
base_dir = os.path.dirname(os.path.abspath(__file__))  # path to src/

# Normalize path
raw_path_lakshmi = os.path.normpath(os.path.join(base_dir, '..', 'data', 'raw', 'lakshmi.txt'))
raw_path_ai = os.path.normpath(os.path.join(base_dir, '..', 'data', 'raw', 'ai.txt'))

# Save lakshmi article
with open(raw_path_lakshmi, 'w', encoding='utf-8') as f:
    f.write(lakshmi_text)

# Save AI article
with open(raw_path_ai, 'w', encoding='utf-8') as f:
    f.write(ai_text)
