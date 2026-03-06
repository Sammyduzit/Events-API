from models import User

def test_user_password_hashing():
    """Tests password hashing and checking"""

    # Arrange: Create User and set pw
    user = User(username="Frank")
    my_pw = "superpw12345"
    user.set_password(my_pw)

    #Act & assert
    assert user.check_password(my_pw) == True
    assert user.check_password("wrongpw12345") == False
    assert user.password_hash != my_pw
    assert user.password_hash is not None


def test_user_to_dict_excludes_password():
    """Tests that to_dict() never exposes the password hash"""

    #Arrange
    user = User(username="Magikarp")
    user.set_password("splash123")

    #Act
    data = user.to_dict()

    #Assert
    assert data["username"] == "Magikarp"
    assert "password" not in data
    assert "password_hash" not in data


def test_password_hashing_uses_salt():
    """Tests that hashing the same password twice produces different hashes (salt)"""

    #Arrange
    user1 = User(username="Magikarp")
    user2 = User(username="Hoppip")

    #Act
    user1.set_password("samepw123")
    user2.set_password("samepw123")

    #Assert
    assert user1.password_hash != user2.password_hash
