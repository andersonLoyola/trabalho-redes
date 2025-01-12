import { createContext, useContext, useState } from "react";
import { AuthContext } from "./AuthContext";
import { LoadChatInfo } from "../services/ChatsService";

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
    const { token, userId, userName } = useContext(AuthContext);
    const [chatUsers, setChatUsers] = useState({});
    const [chatMessages, setChatMessages] = useState([]);
    const [currentChatId, setCurrentChatId] = useState(null);
    const [chatType, setChatType] = useState("");
    const [socket, setSocket] = useState(null);

    const loadSelectedChatData = async (chatId) => {
        try {
            const { chat } = await LoadChatInfo(token, chatId);
            setCurrentChatId(chatId)
            setChatUsers(chat.users);
            setChatType(chat.chat_type);
            setChatMessages(chat.messages);

        } catch (error) {
            console.trace(error);
        }
    }

    const connect = async () => {
        try {
            const socket = new WebSocket('ws://localhost:9090')

            socket.onopen = () => {
                if (socket.readyState === socket.OPEN) {
                    const authMessage = JSON.stringify({
                        auth_token: token,
                        sender_id: currentChatId,
                        request_type: 'auth',

                    });
                    socket.send(authMessage);
                }
            };

            socket.onmessage = (event) => {
                const { data } = event;
                const message = JSON.parse(data);
                if (message.sender_id === userId) { message.sender = 'you' }
                setChatMessages((previousMsgs) => [...previousMsgs, message])
            }

            socket.onclose = () => {

            }
            setSocket(socket)
        } catch (error) {
            setSocket(null)
        }

    }

    const disconnect = () => {
        if (socket) {
            socket.close();
            setSocket(null);
        }
        setCurrentChatId(null);
        setChatUsers([]);
        setChatMessages([]);
    }

    const sendMessage = ({ content, attachment }) => {
        if (socket.readyState === socket.OPEN) {
            if (chatType === "DUO") {
                const data = {
                    sender_id: userId,
                    sender: userName,
                    receiver_id: chatUsers.find(user => user._id !== userId)._id,
                    request_type: "duo_message",
                    content,
                    attachment,
                }

                socket.send(JSON.stringify(data));
            } else if (chatType === "GROUP") {
                const data = {
                    sender_id: userId,
                    sender: userName,
                    chat_id: currentChatId,
                    request_type: "group_message",
                    content,
                    attachment,
                }

                socket.send(JSON.stringify(data));
            }
            // socket.send(mappedMsg);

        }
    }

    return (
        <ChatContext.Provider value={{
            chatUsers,
            chatMessages,
            currentChatId,
            connect,
            disconnect,
            sendMessage,
            setCurrentChatId,
            loadSelectedChatData,
        }}>
            {children}
        </ChatContext.Provider>
    );
};