from .database import add_company, add_user

def seed_database():

    add_company(name="Company_A")
    add_company(name="Company_B", parent_name="Company_A")
    add_company(name="Company_C", parent_name="Company_A")
    add_company(name="Company_D", parent_name="Company_B")
    add_company(name="Company_E", parent_name="Company_B")
    add_company(name="Company_F", parent_name="Company_C")

    add_user(username="user1", company_name="Company_A")
    add_user(username="user2", company_name="Company_B")
    add_user(username="user3", company_name="Company_C")
    add_user(username="user4", company_name="Company_D")
    add_user(username="user5", company_name="Company_E")
    add_user(username="user6", company_name="Company_F")

