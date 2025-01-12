import axios from 'axios';

export async function LoadChatsInfo(token) {
    const { data } = await axios.get('http://localhost:8080/api/chats', {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })

    return data
};

export async function LoadChatInfo(token, chatId) {
    const { data } = await axios.get(`http://localhost:8080/api/chats/${chatId}`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })

    return data;
}