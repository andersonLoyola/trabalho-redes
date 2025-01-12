export function ChatMessageItem({ message_data }) {
    return (
        <div className="mb-2">
            <div className="text-xs text-gray-500">{message_data.sender ?? 'unknown'}:</div>
            <div className="p-2 bg-white rounded shadow">{message_data.content}</div>
        </div>
    );
}