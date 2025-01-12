
import React from 'react';

export function AvailableChatItem({ id, name, onChatSelect }) {
    return (
        <div
            className="p-4 mb-2 bg-white rounded shadow cursor-pointer hover:bg-gray-100 v-screen mx-auto"
            onClick={() => onChatSelect(id)}>
            <h3>{name}</h3>
        </div>
    )
}