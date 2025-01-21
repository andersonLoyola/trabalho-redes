export function ChatSideBar({ users, onDisconnect }) {
    return (
        <div className="w-1/4 p-4 flex flex-col justify-between h-full">
            <div>
                <h2 className="text-xl font-bold mb-6">Connected Users</h2>
                <ul>
                    {users.map((user) => (
                        <li key={user._id} className="mb-4">
                            <div>
                                {user.username}
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
            <button
                className="w-full bg-red-500 text-white py-2 px-4 rounded mt-auto"
                onClick={onDisconnect()}
            >
                Disconnect
            </button>
        </div>
    );
}