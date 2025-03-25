import { Types } from "mongoose";
import { Request } from "express";

export interface AdminToken {
    password: string
}

export interface UserSignupBody {
    name: string;
    email: string;
    password: string;
}

export interface UserLoginBody {
    email: string;
    password: string;
}

export interface User {
    _id: Types.ObjectId;
    name: string;
    email: string;
    password: string;
    chatStreams: Types.ObjectId[];
}

export interface Chats {
    _id: Types.ObjectId;
    sender: "user" | "agent";
    message: string;
}

export interface ChatStream {
    _id: Types.ObjectId;
    userId: Types.ObjectId;
    chats: Chats[];
}

declare module "express" {
    export interface Request {
        user?: User;
    }
}