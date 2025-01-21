import axios from 'axios';

export async function LoginService(username, password) {
    try {

        const { data } = await axios.post('http://localhost:8080/api/users/login', {
            username,
            password,
        });

        window.localStorage.setItem('token', data.access_token);
        window.localStorage.setItem('refreshToken', data.refresh_token);

        return data;
    } catch (error) {
        console.error('Failed to fetch:', error);
    }
}

export async function SignupService(username, password) {
    const { data } = await axios.post('http://localhost:8080/api/v1/users/signup', {
        username,
        password,
    });

    return data;
}