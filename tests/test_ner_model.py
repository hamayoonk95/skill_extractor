import pytest
from tests.test_helpers import load_trained_model


# This fixture will run once before executing the test cases
@pytest.fixture(scope="module")
def nlp():

    model_path = '../trained_models/epoch_35'
    return load_trained_model(model_path)

def test_skill_extraction_basic(nlp):
    description = "we are looking for someone skilled in python and java."
    doc = nlp(description)

    expected_skills = [("python", "LANGUAGE"), ("java", "LANGUAGE")]

    detected_skills = [(ent.text, ent.label_) for ent in doc.ents]

    assert set(expected_skills) == set(detected_skills)

def test_skill_extraction_no_skills(nlp):
    description = "we are hiring."
    doc = nlp(description)

    expected_skills = []

    detected_skills = [(ent.text, ent.label_) for ent in doc.ents]

    assert expected_skills == detected_skills

def test_skill_multiple_terms(nlp):
    description = "experience in c#.net is preferred otherwise java/springboot also fine." \
                  "Additionally docker, kubernetes and plus jira and agile and oop"
    doc = nlp(description)

    expected_skills = [("java", "LANGUAGE"), ("springboot", "LIBRARY"), ("docker", "TOOL"), ("kubernetes", "PLATFORM"), ("aws", "PLATFORM"), ("agile", "METHODOLOGY"), ("oop", "METHODOLOGY"), ("jira", "TOOL")]

    detected_skills = [(ent.text, ent.label_) for ent in doc.ents]

    assert set(expected_skills) == set(detected_skills)
