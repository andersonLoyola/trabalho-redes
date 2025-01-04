import sys

class BaseHandler:

    def handle_error(self, error, flow_name):
        print(f"""
            ERROR: {error} WHEN {flow_name}
            do you witsh to continue?
                (y) yes
                (n) no
        """)
        choice = input('>: ')
        if choice == 'y':
            return True
        else:
            sys.exit()
                
