import spacy

from unittest.mock import Mock
from scraper.scraping.data_processor import DataProcessor

# Helper function to read HTML templates
def read_sample_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Helper function to set up the mock model
def setup_mock_ner_model(mock_ents):
    mock_model = Mock()
    mock_doc = Mock()
    mock_ents = [Mock(text=text, label_=label) for text, label in mock_ents]
    mock_doc.ents = mock_ents
    mock_model.return_value = mock_doc
    processor = DataProcessor(mock_model)
    return mock_model, processor


# Helper function to validate the result
def validate_result(result, title, description, skills):
    # Convert all skill entities to tuples for consistency
    skills = [tuple(skill) if isinstance(skill, list) else skill for skill in skills]

    expected_output = {
        'title': title,
        'description': description,
        'skills': sorted(skills)
        }
    result['skills'] = sorted(result['skills'], key=lambda x: str(x))
    assert result == expected_output


# loads the training model
def load_trained_model(model_path):
    return spacy.load(model_path)