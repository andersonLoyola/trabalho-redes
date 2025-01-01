class LoginHandler {
    #username;
    #password;
    #errors;

    constructor(username, password) {
        this.#username = username;
        this.#password = password;
        this.#errors = [];
    }

    #validate = () => {
        if (!this.#username.replaceAll(' ', '').length()) {
            this.#errors.unshift('Username cannot be empty');
        }

        if (!this.#password.replaceAll(' ', '').length()) {
            this.#errors.unshift('password cannot be empty');
        }

        if (!this.#username.length() > 6) {
            this.#errors.unshift('Username length too small');
        }

        if (!this.#password.length()) {
            this.#errors.unshift('password too small');
        }
    }

    performLogin = async () => {
        try {
            this.#validate();
            if (this.#errors.length) {
                const error = this.#errors.shift()
                console.error(error);
                throw new Error(error);
            }

            await fetch('http://localhost:8080/api/login', {
                'headers': {
                    'Content-type': 'application/json',
                },
                'body': JSON.stringify({
                    username: this.#username,
                    password: this.#password,
                }),
                'method': 'POST'
            });
        } catch (error) {
            this.#errors.unshift(error.message);
            throw error;
        }
    }
}
/** */