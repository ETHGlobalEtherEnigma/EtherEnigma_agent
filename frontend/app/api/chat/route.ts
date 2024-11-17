// pages/api/chat.ts

import type { NextApiRequest, NextApiResponse } from 'next';

interface Message {
    role: 'user' | 'ai';
    content: string;
}

interface ChatRequest {
    messages: Message[];
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'POST') {
        console.log("Got a POST request.")
        const { messages }: ChatRequest = req.body;

        // Check if there are messages and get the last user's message
        if (messages && messages.length > 0) {
            const userMessage = messages[messages.length - 1];

            // Respond with the same message as an AI response
            res.status(200).json({
                messages: [
                    ...messages,
                    { role: 'ai', content: userMessage.content } // Echoing back the user's message
                ]
            });
        } else {
            res.status(400).json({ error: 'No messages provided' });
        }
    } else {
        // Handle any other HTTP method
        res.setHeader('Allow', ['POST']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}