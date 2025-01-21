import { useContext } from "react";
import { AvailableChatsSideBar } from "../components/home/AvailableChatsSideBar";
import { AuthContext } from "../contexts/AuthContext";
import { ChatContext } from "../contexts/ChatContext";
import { useNavigate } from 'react-router-dom';
import { LoadingContext } from "../contexts/LoadingContext";

export default function Home() {
    const { token } = useContext(AuthContext);
    const { setCurrentChatId, loadSelectedChatData, connect } = useContext(ChatContext);
    const { isLoading, setIsLoading } = useContext(LoadingContext);

    const navigate = useNavigate();


    const onChatSelect = async (chatId) => {
        setIsLoading(true);
        try {
            await loadSelectedChatData(chatId)
            setCurrentChatId(chatId);
            connect();
            navigate('/chat');
            setIsLoading(false);
        } catch (error) {
            console.error('Failed to load chat data:', error);
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="home-container flex">
            {isLoading ?
                <h2>Loading...</h2> :
                <>
                    <AvailableChatsSideBar
                        token={token}
                        onChatSelect={onChatSelect}
                    />
                    <div className="home-container flex center">
                        <div>
                            <h2>Home</h2>
                            <p>Welcome to the home page!</p>
                        </div>
                    </div>
                </>
            }
        </div>
    );
}