
from database.db_setup import create_session, add_instance
# Import models after the Base has been created
from database.models.job_posting import JobPostings
from database.models.job_roles import JobRoles
from database.models.skill_types import SkillTypes
from database.models.skills import Skills
from database.models.role_skills import RoleSkills


def main():
    # create a new session
    session = create_session()

    # dummy data
    # skill_type = SkillTypes(type_name='Programming Language')
    # add_instance(session, skill_type)
    # skill = Skills(skill_name='Python', type_id=skill_type.id)
    # add_instance(session, skill)
    # role = JobRoles(role_title='FRONT Developer')
    # add_instance(session, role)
    # print(role.id)
    # role_skill = RoleSkills(role_id=role.id, skill_id=skill.id, frequency=30)
    # add_instance(session, role_skill)
    # job_posting = JobPostings(job_title='LOOOOVEOEOEOE' ,job_description='sadfasdf dfvsdfg', role_id=role.id)
    # add_instance(session, job_posting)

    session.close()

if __name__ == "__main__":
    main()