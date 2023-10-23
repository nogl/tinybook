from app import models

if __name__ == '__main__':
    new_user = models.User(username='J', email='MisCoJones')
    print(new_user)
    print(new_user.get_validations_errors())

    new_user2 = models.User(username='Jonnnnnnnnn', email='MisCoJones')
    print(new_user2)
    print(new_user2.get_validations_errors())

    new_user3 = models.User(username='Jont_The_withc', email='mail@empresa.com')
    print(new_user3)
    print(new_user3.get_validations_errors())

