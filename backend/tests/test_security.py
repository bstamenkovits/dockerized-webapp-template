from core.security import hash_password, verify_password


def test_hash_password_is_not_plaintext():
    """Test that the hashed password is not the plaintext password."""
    hashed = hash_password("s3cret-pass")
    assert hashed != "s3cret-pass"


def test_hash_password_is_salted():
    """Test that hashing the same password twice yields different hashes (random salt)."""
    assert hash_password("s3cret-pass") != hash_password("s3cret-pass")


def test_verify_password_accepts_correct_password():
    """Test that verify_password evaluates to True for a correct password."""
    hashed = hash_password("s3cret-pass")

    assert verify_password(hashed, "s3cret-pass") is True


def test_verify_password_rejects_wrong_password():
    """Test that verify_password evaluates to False for a wrong password."""
    hashed = hash_password("s3cret-pass")

    assert verify_password(hashed, "wrong-pass") is False
