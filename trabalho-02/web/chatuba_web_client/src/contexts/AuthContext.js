import { createContext, useState } from "react";
import { decodeJwt } from 'jose';
import { LoginService, SignupService } from "../services/AuthService";
export const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [token, setToken] = useState(null);
    const [userId, setUserId] = useState('');
    const [userName, setUserName] = useState('');
    const [refreshToken, setRefreshToken] = useState(null);

    const login = async (data) => {
        try {
            const { access_token, refresh_token } = await LoginService(data.username, data.password);
            const { user_id, username } = decodeJwt(access_token);
            setToken(access_token);
            setUserId(user_id);
            setUserName(username);
            setRefreshToken(refresh_token);
        } catch (error) {
            console.trace(error);
            throw error;
        }
    }

    const signup = async (data) => {
        try {
            await SignupService(data.username, data.password); // MAYBE IMPLEMENT A LOGIN TO SEE IF IT WAS SUCCESSFUL
        } catch (error) {
            console.trace(error);
            throw error;
        }
    }

    const logoff = () => {
        setToken(null)
    }

    return (
        <AuthContext.Provider value={{ token, userId, userName, refreshToken, login, logoff, signup }}>
            {children}
        </AuthContext.Provider>
    );
}