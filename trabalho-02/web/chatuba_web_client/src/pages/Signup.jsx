import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import { LoadingContext } from '../contexts/LoadingContext';

export default function Signup() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const { signup } = useContext(AuthContext);
    const { isLoading, setIsLoading } = useContext(LoadingContext);

    const navigate = useNavigate();

    async function SignupHandler() {
        setIsLoading(true);
        try {
            await signup({ username, password });
            navigate('/login');
        } catch (error) {
            console.error('Failed to create user:', error);
        } finally {
            setIsLoading(false);
        }
    };

    function loginHandler() {
        navigate('/login')
    }

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            {isLoading ? (<h2> Loading...</h2>) :
                (<div className="w-full max-w-md p-8 space-y-6 bg-white rounded shadow-md">
                    <h2 className="text-2xl font-bold text-center">Signup</h2>
                    <input
                        type="text"
                        id="username"
                        placeholder="Username"
                        className='w-full px-3 py-2 border rounded'
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                    />

                    <input
                        type="password"
                        id="password"
                        placeholder="Password"
                        className='w-full px-3 py-2 border rounded'
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                    />

                    <button
                        className='w-full px-3 py-2 text-white bg-blue-500 rounded hover:bg-blue-700'
                        onClick={SignupHandler}
                    >
                        signup
                    </button>
                    <button
                        className='w-full px-3 py-2 text-white bg-blue-500 rounded hover:bg-blue-700'
                        onClick={loginHandler}
                    >
                        login
                    </button>
                </div>)
            }
        </div>
    );
};
