def test__notification_email_addresses__one_owner_no_generic(client, faker):
    u = faker.get_test_user()

    s = faker.get_test_service(owners=[u], generic_recipients='')

    assert s.notification_email_addresses == [u.email]


def test__notification_email_addresses__two_owners_no_generic(client, faker):
    u = faker.get_test_user()
    u2 = faker.get_test_user()

    s = faker.get_test_service(owners=[u, u2], generic_recipients='')

    assert s.notification_email_addresses == [u.email, u2.email]


def test__notification_email_addresses__one_generic(client, faker):
    u = faker.get_test_user()

    s = faker.get_test_service(owners=[u], generic_recipients='test@example.com')

    assert s.notification_email_addresses == [u.email, 'test@example.com']


def test__notification_email_addresses__two_generic(client, faker):
    u = faker.get_test_user()

    s = faker.get_test_service(owners=[u], generic_recipients='test@example.com,hello@internet.com')

    assert s.notification_email_addresses == [u.email, 'test@example.com', 'hello@internet.com']


def test__notification_email_addresses__generic_space_delimiter(client, faker):
    u = faker.get_test_user()

    s = faker.get_test_service(owners=[u], generic_recipients='test@example.com hello@internet.com')

    assert s.notification_email_addresses == [u.email, 'test@example.com', 'hello@internet.com']


def test__notification_email_addresses__generic_semicolon_delimiter(client, faker):
    u = faker.get_test_user()

    s = faker.get_test_service(owners=[u], generic_recipients='test@example.com;hello@internet.com')

    assert s.notification_email_addresses == [u.email, 'test@example.com', 'hello@internet.com']


def test__notification_email_addresses__generic_repeated_delimiter(client, faker):
    u = faker.get_test_user()

    s = faker.get_test_service(owners=[u], generic_recipients='test@example.com; hello@internet.com')

    assert s.notification_email_addresses == [u.email, 'test@example.com', 'hello@internet.com']


def test__notification_email_addresses__generic_mixed_delimiter(client, faker):
    u = faker.get_test_user()

    s = faker.get_test_service(owners=[u], generic_recipients='test@example.com;hello@internet.com,email@email.com posh.silk.com')

    assert s.notification_email_addresses == [u.email, 'test@example.com', 'hello@internet.com', 'email@email.com', 'posh.silk.com']
