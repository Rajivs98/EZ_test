from nanoid import generate


def generate_otp():
    return generate("1234567890", 6)