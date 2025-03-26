import { Request, Response } from "express";
import ChatStream from "../models/chatStream.model";
import User from "../models/user.model";

export const createChatStream = async (req: Request, res: Response) => {
    try {
        const userId = req.user?._id;
        const user = await User.findById(userId);
        if (!user) {
            res.status(400).json({ error: "Cannot find user" });
            return;
        }

        const newChatStream = new ChatStream({
            userId
        });

        if (newChatStream) {
            await newChatStream.save();
            user.chatStreams.push(newChatStream._id);
            await user.save();
            res.status(201).json(newChatStream);
        } else {
            res.status(400).json({ error: "Error in creating new Chat Stream" });
        }
    } catch (error) {
        console.log("Error in createChatStream controller", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
}

export const appendChats = async (req: Request, res: Response) => {
    try {
        const chatId = req.params.id;
        const { sender, message } = req.body;
        const chatStream = await ChatStream.findById(chatId);
        if (!sender || !message || (sender !== "user" && sender !== "agent")) {
            res.status(400).json({ error: "Invalid chat data received" });
            return;
        }

        if (!chatStream) {
            res.status(400).json({ error: "Error in finding Chat Stream" });
            return;
        }

        if (chatStream.chats.length === 0) {
            chatStream.header = message;
        }

        chatStream.chats.push({
            sender,
            message
        });
        await chatStream.save();

        res.status(200).json(chatStream);
    } catch (error) {
        console.log("Error in appendChats controller", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
}

export const getMyChatStreams = async (req: Request, res: Response) => {
    try {
        const userId = req.user?._id;
        if (!userId) {
            res.status(400).json({ error: "User ID is required" });
            return;
        }
        const user = await User.findById(userId);
        if (!user) {
            res.status(400).json({ error: "User not found" });
            return;
        }

        const chatStreams = await ChatStream.find({ _id: { $in: user.chatStreams } }).select("_id header createdAt");

        const formattedChatStreams = chatStreams.map(chat => ({
            id: chat._id,
            header: chat.header,
            createdAt: chat.createdAt
        }));

        res.status(200).json(formattedChatStreams);
    } catch (error) {
        console.log("Error in getMyChatStreams controller", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
}

export const getChatStreamById = async(req: Request, res: Response) => {
    try {
        const id = req.params.id;
        if(!id) {
            res.status(400).json({ error: "User ID is required" });
            return;
        }

        const chatStream = await ChatStream.findById(id);
        if (!chatStream) {
            res.status(400).json({ error: "Chat not found" });
            return;
        }

        res.status(200).json(chatStream);
    } catch (error) {
        console.log("Error in getChatStreamById controller", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
}