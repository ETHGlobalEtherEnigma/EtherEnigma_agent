// ChatComponent.tsx
'use client'

import React, { useState } from 'react';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

const ChatComponent: React.FC = () => {
    const [input, setInput] = useState<string>('');
    const [messages, setMessages] = useState<Message[]>([]);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInput(event.target.value);
    };

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault(); // Prevent form submission

        // Prepare the message payload
        const newMessage: Message = {
            role: 'user',
            content: input,
        };

        // Update local state with the new user message
        setMessages((prevMessages) => [...prevMessages, newMessage]);

        // Send the message to the backend
        try {
            const response = await fetch('http://localhost:9000/api/gpt/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ messages: [...messages, newMessage] }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            //console.log(data.messages)
            // Update state with the AI response
            setMessages((prevMessages) => [...prevMessages, data.messages]);
        } catch (error) {
            console.error('Error:', error);
        }

        // Clear input field
        setInput('');
    };

    return (
        <div>
            <h1>Chat</h1>
            <div style={{ border: '1px solid #ccc', padding: '10px', height: '300px', overflowY: 'scroll' }}>
                {messages.map((msg, index) => (
                    <div key={index}>
                        <strong>{msg.role === 'user' ? 'User' : 'AI'}:</strong> {msg.content}
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={input}
                    onChange={handleInputChange}
                    placeholder="Type your message..."
                    style={{ width: '80%' }}
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
};

export default ChatComponent;