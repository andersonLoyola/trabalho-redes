import { useEffect, useState } from "react";
import { LoadChatsInfo } from "../../services/ChatsService";
import { AvailableChatItem } from "./AvailableChatItem";

export function AvailableChatsSideBar({ token, onChatSelect }) {
    const [chatsInfo, setChatsInfo] = useState([]);

    useEffect(() => {
        const loadChatInfo = async () => {
            const { chats: chatsInfo } = await LoadChatsInfo(token);
            setChatsInfo(chatsInfo);
        }

        loadChatInfo();
    }, [token]);

    return (
        <div className="w-1/10 p-4 bg-gray-200 h-screen">
            <h2 className="text-xl font-bold mb-4">Available Chats</h2>
            <ul className="overflow-y-auto h-full">
                {chatsInfo.map(chat => (
                    <AvailableChatItem
                        id={chat._id}
                        key={chat._id}
                        name={chat.chat_name}
                        onChatSelect={onChatSelect}
                    />
                ))
                }
            </ul>
        </div>
    );
};