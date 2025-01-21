import { useContext, useEffect, useRef, useState } from "react";
import { ChatContext } from "../contexts/ChatContext";
import { ChatMessageItem } from "../components/chats/ChatMessageItem";
import { ChatSideBar } from "../components/chats/ChatSideBar";

export function Chat() {
    const [message, setMessage] = useState("");
    const [attachment, setAttachment] = useState(null);
    const inputRef = useRef(null)

    const {
        connect,
        chatUsers,
        sendMessage,
        chatMessages,
        disconnect,
    } = useContext(ChatContext);


    const onSendMessage = () => {
        const trimmedMessage = message.trim();
        if (trimmedMessage || attachment) {
            const msg = {
                content: trimmedMessage,
                attachment: attachment,
            }

            sendMessage(msg);
        }
        setAttachment(null);
        setMessage("");
    }


    const handleAttachClick = () => {
        inputRef.current.onchange = (e) => { console.log(e.target.value) } // fk me
        inputRef.current.click();
    }

    const handleAttachmentChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');
                const attachment = {
                    file_name: file.name,
                    file_type: file.type,
                    file_size: file.size,
                    file_data: base64String,
                }
                setAttachment(attachment);
                inputRef.current.onchange = (e) => { console.log(e.target.value) } // fk me

            };
            reader.readAsDataURL(file);
        }
    }

    return (
        <div className="flex h-screen">
            <ChatSideBar users={chatUsers} onDisconnect={() => { }} />
            <div className="flex-1 flex flex-col">
                <div className="flex-1 p-4 overflow-y-auto bg-gray-100">
                    {chatMessages.map((msg, index) => (
                        <ChatMessageItem key={index} message_data={msg} />
                    ))}
                </div>
                <div className="p-4 bg-white flex items-center">
                    <input
                        type="text"
                        className="flex-1 p-2 border rounded mr-2"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="Type your message..."
                    />
                    <input
                        style={{ display: 'none' }}
                        ref={inputRef}
                        title="attach"
                        onChange={handleAttachmentChange}
                        type="file"
                    />
                    <button
                        className="p-2 bg-blue-500 text-white rounded mr-2"
                        onClick={handleAttachClick}
                    >
                        Attach
                    </button>
                    <button
                        className="p-2 bg-blue-500 text-white rounded"
                        onClick={onSendMessage}
                    >
                        Send
                    </button>
                </div>
            </div>

        </div>
    );

}