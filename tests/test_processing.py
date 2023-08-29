import pytest
from constants.skills_list import reverse_aliases

from tests.test_helpers import read_sample_html, setup_mock_ner_model, validate_result


def test_extract_job_data_normal_case():
    mock_model, processor = setup_mock_ner_model([('python', 'LANGUAGE')])
    result = processor.extract_job_data(read_sample_html('./html_templates/normal_case.html'))
    validate_result(result, "Software Developer", "must know python", [('python', 'LANGUAGE')])


def test_extract_job_data_missing_h1_tag():
    mock_model, processor = setup_mock_ner_model([('python', 'LANGUAGE'), ('java', 'LANGUAGE')])
    result = processor.extract_job_data(read_sample_html('./html_templates/missing_h1_tag.html'))
    validate_result(result, "", "experience in python and java required.",
                    [('python', 'LANGUAGE'), ('java', 'LANGUAGE')])


def test_extract_job_data_empty_strings():
    mock_model, processor = setup_mock_ner_model([])
    result = processor.extract_job_data(read_sample_html('./html_templates/empty_tags.html'))
    validate_result(result, "", "", [])


def test_extract_job_data_multiple_entities():
    mock_model, processor = setup_mock_ner_model([('python', 'LANGUAGE'), ('java', 'LANGUAGE'), ('docker', 'TOOL')])
    result = processor.extract_job_data(read_sample_html('./html_templates/multiple_entities.html'))
    validate_result(result, "Data Engineer", "experience in python and java required along with docker.",
                    [('python', 'LANGUAGE'), ('java', 'LANGUAGE'), ('docker', 'TOOL')])


def test_extract_job_data_different_tags():
    mock_model, processor = setup_mock_ner_model([])
    result = processor.extract_job_data(read_sample_html('./html_templates/different_tags.html'))
    validate_result(result, "", "", [])


def test_extract_job_data_repeated_skills():
    mock_model, processor = setup_mock_ner_model(
        [('react.js', 'LIBRARY'), ('typescript', 'LANGUAGE'), ('javascript', 'LANGUAGE')])
    result = processor.extract_job_data(read_sample_html('./html_templates/repeated_skills.html'))
    validate_result(result, "Frontend Developer", "must know react, typescript, javascript and js",
                    [('react.js', 'LIBRARY'), ('typescript', 'LANGUAGE'), ('javascript', 'LANGUAGE')])


def test_entities_to_standard():
    mock_model, processor = setup_mock_ner_model(
        [('amazon web services', 'PLATFORM'), ('typescript', 'LANGUAGE'), ('javascript', 'LANGUAGE'),
         ('vue', 'LIBRARY')])  # Mock model will return these entities
    result = processor.extract_job_data(read_sample_html('./html_templates/repeated_skills.html'))

    # Transform the mock entities into their standard forms using reverse_aliases
    expected_skills = {(reverse_aliases.get(ent_text, ent_text), ent_label)
                       for ent_text, ent_label in
                       [('amazon web services', 'PLATFORM'), ('typescript', 'LANGUAGE'), ('javascript', 'LANGUAGE'),
                        ('vue', 'LIBRARY')]}

    assert set(result['skills']) == expected_skills


# Test for non-English text
def test_non_english_text():
    mock_model, processor = setup_mock_ner_model([('python', 'LANGUAGE')])
    result = processor.extract_job_data(read_sample_html('./html_templates/non_english.html'))
    validate_result(result, "Desarrollador de Software", "debe saber python", [('python', 'LANGUAGE')])


# Test to ensure return types are consistent
def test_return_types():
    mock_model, processor = setup_mock_ner_model([('python', 'LANGUAGE')])
    result = processor.extract_job_data(read_sample_html('./html_templates/normal_case.html'))
    assert isinstance(result, dict)
    assert all(isinstance(value, (str, list)) for value in result.values())


# Test for special characters in job titles or descriptions
def test_special_characters():
    mock_model, processor = setup_mock_ner_model([('python', 'LANGUAGE')])
    result = processor.extract_job_data(read_sample_html('./html_templates/special_character.html'))
    validate_result(result, "Software@Dev", "must k!now python", [('python', 'LANGUAGE')])
