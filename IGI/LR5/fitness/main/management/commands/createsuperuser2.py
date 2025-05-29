from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')
        database = options.get('database')

        try:
            if not username:
                username = input("Username: ")
            if not email:
                email = input("Email address: ")
            if not password:
                password = "admin"  # Default password, change it later

            user_data = {
                'username': username,
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            }

            user = self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)

            if options.get('verbosity', 0) >= 1:
                self.stdout.write("Superuser created successfully.")

            return user

        except Exception as e:
            raise CommandError(str(e))
