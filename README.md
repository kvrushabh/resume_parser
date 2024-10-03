# Resume Analyser

This project is a Resume Analyser, which parses resumes, extracts important information (like name, cobtact details, email, skills, education, location, etc.), and helps analyze the resume contents based on predefined criteria.

## Setup Instructions

Follow the steps below to set up the project on your local machine.

### 1. Create a Virtual Environment

First, create a virtual environment for the project using the following command:

```bash
python -m venv env
```
or 
```bash
python3 -m venv env
```

### 2. Activate the Virtual Environment

Activate the virtual environment:

#### Windows:
```bash
env\Scripts\activate
```

#### Ubuntu/MacOS:
```bash
source env/bin/activate
```

### 3. Install Required Packages

Install all the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

### 4. Download SpaCy Model

After installing the packages, download the SpaCy language model `en_core_web_sm` by running:

```bash
python -m spacy download en_core_web_sm
```

### 5. Modify Pyresparser Files

There are two files in Pyresparser that need to be modified for this project.

#### Modify `resume_parser.py`:

1. Navigate to the following path:
```bash
env/lib/python3.10/site-packages/pyresparser/resume_parser.py
```

2. Locate the following line:
```bash
custom_nlp = spacy.load(os.path.dirname(os.path.abspath(__file__)))
```

3. Change it to:
```bash
custom_nlp = spacy.load("en_core_web_sm")  # Use SpaCy's pre-trained model
```

#### Modify `utils.py`:

1. Navigate to the following path:
```bash
env/lib/python3.10/site-packages/pyresparser/utils.py
```

2. Replace the entire `extract_name` function with the following code:
```bash
def extract_name(nlp_text, matcher):
    '''
    Helper function to extract name from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param matcher: object of `spacy.matcher.Matcher`
    :return: string of full name
    '''
    # Assuming `cs.NAME_PATTERN` is a single pattern (a dictionary), wrap it in a list
    pattern = cs.NAME_PATTERN  # `cs.NAME_PATTERN` should be a list of dictionaries (token patterns)

    if not isinstance(pattern, list):
        raise ValueError("cs.NAME_PATTERN must be a list of dictionaries")

    matcher.add('NAME', [pattern])  # Pass the pattern wrapped in a list of lists

    # Use the matcher to find matches in the provided text
    matches = matcher(nlp_text)

    # Iterate over the matches to extract the name
    for _, start, end in matches:
        span = nlp_text[start:end]
        if 'name' not in span.text.lower():  # Ignore generic matches with 'name'
            return span.text

    return None  # Return None if no match is found
```

### 6. Database Migration

Once the changes are made, run the following command to execute the database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Running the Project Locally

To start the project on your local development server, use the following command:

```bash
python manage.py runserver
```

Open your web browser and go to http://127.0.0.1:8000/ to interact with the app.


