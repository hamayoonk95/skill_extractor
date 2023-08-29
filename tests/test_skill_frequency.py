from collections import Counter


def test_skill_frequency():
    mock_processed_jobs_list = [
        {'title': 'Job 1', 'description': 'desc 1', 'skills': [['Java', 'LANGUAGE'], ['Python', 'LANGUAGE']]},
        {'title': 'Job 2', 'description': 'desc 2', 'skills': [['Python', 'LANGUAGE']]},
        {'title': 'Job 3', 'description': 'desc 3', 'skills': [['Java', 'LANGUAGE'], ['JavaScript', 'LANGUAGE'], ['aws', 'PLATFORM']]},
        {'title': 'Job 4', 'description': 'desc 4',
         'skills': [['Java', 'LANGUAGE'], ['JavaScript', 'LANGUAGE'], ['Python', 'LANGUAGE'], ['aws', 'PLATFORM']]}
        ]

    actual_skill_frequency = Counter()

    for processed_job in mock_processed_jobs_list:
        skills = processed_job['skills']
        for skill, _ in skills:
            actual_skill_frequency[skill] += 1

    expected_skill_frequency = {'Java': 3, 'Python': 3, 'JavaScript': 2, 'aws': 2}

    assert actual_skill_frequency == expected_skill_frequency
