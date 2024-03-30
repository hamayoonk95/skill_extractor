# Data Extractor and NER Model

## Overview

The Data Extractor is designed to scrape job descriptions from Indeed, providing a comprehensive dataset for analyzing current job market trends and demands. Utilising a scraping algorithm, it retrieves detailed job postings which are then processed by the NER (Named Entity Recognition) model for skill extraction and categorisation.

## Data Extractor

### Prerequisites

-   Python 3.x

After installing python, install the required libraries by running the following command:
'pip install -r requirements' in the root directory.

### Configuration

Befoe running the Data Extractor, you need to set up your database connection. Create a '.env' file in the scraper directory with the following content, replacing the placeholders with your database details:

MYSQL_HOST='localhost'
MYSQL_USER='your_username'
MYSQL_PASSWORD='your_password'
DRIVER_NAME='mysql+mysqlconnector'
DATABASE_NAME='your_database_name'

### Running the Data Extractor

1. Navigate to the scraper directory: 'cd scraper'
2. Run the 'main.py' script: 'python main.py'
3. When prompted, enter the NER model's location. The latest model is located at: '../trained_models/trained_model/ner0'

This process will initiate the scraping of job descriptions from Indeed and use the NER model to extract skills from job description.

---

## NER Model

### Prerequisites

-   Python 3.x

### Running the NER Model

1. Open your terminal or command prompt.
2. Navigate to the train_ner_model directory:
   'cd train_ner_model'
3. Run the `main.py` script to start the training process:
   'python main.py'
4. The script uses training data from `../training_data/training_data.jsonl` by default. If you have new training data, update the `training_data` path in the script to your new `.jsonl` file before running.

To generate more training data, use the `generate_training_data(description):` function in `ner_trainer_utils`. This function allows you to input descriptions, which it will then convert into training data. You might need to refine this data further before it's ready for training.
