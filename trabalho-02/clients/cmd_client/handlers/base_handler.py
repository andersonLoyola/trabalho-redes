import sys

class BaseHandler:

    def handle_error(self, error):
        print(f"ERROR: {error}")
        print("""
        do you wish to continue?
            (y) yes
            (n) no
        """)
        choice = input('> ')
        if choice == 'y':
            return True
        else:
            sys.exit()
                
