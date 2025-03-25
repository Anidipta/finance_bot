import { Request, Response } from "express";
import User from "../models/user.model";
import bcrypt from "bcryptjs";
import generateTokenAndSetCookie from "../utils/generateTokenAndSetCookie";
import { client } from "../redis/client";
import { UserLoginBody, UserSignupBody } from "../types";

export const signup = async (req: Request, res: Response) => {
    try {
        const {
            name,
            email,
            password
        }: UserSignupBody = req.body;

        if (password.length < 6) {
            res.status(400).json({ error: "Password should be at least 6 characters long" });
            return;
        }
        if (name.length < 2) {
            res.status(400).json({ error: "Name should be at least 2 characters long" });
            return;
        }

        const sameUser = await User.findOne({ email });
        if (sameUser) {
            res.status(400).json({ error: "An User with this email exists. Try to login with this email" });
            return;
        }

        const salt = await bcrypt.genSalt(12);
        const passwordHash = await bcrypt.hash(password, salt);

        const newUser = new User({
            name,
            email,
            password: passwordHash,
        });

        if (newUser) {
            await newUser.save();

            const token = generateTokenAndSetCookie(newUser._id, res);
            const payload = {
                token,
                _id: newUser._id,
                name: newUser.name,
                email: newUser.email
            };

            await client.set(`FGPT-user:${newUser._id}`, JSON.stringify(payload));
            await client.expire(`FGPT-user:${newUser._id}`, 30 * 24 * 60 * 60);

            res.status(201)
                .header("Authorization", `Bearer ${token}`)
                .json({
                    _id: newUser._id,
                    name: newUser.name,
                    email: newUser.email,
                    chatStreams: newUser.chatStreams,
                    token
                });
        }
    } catch (error) {
        console.log("Error in Signup controller", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
}

export const login = async (req: Request, res: Response) => {
    try {
        const { email, password }: UserLoginBody = req.body;
        const user = await User.findOne({ email });
        if (!user) {
            res.status(400).json({ error: "Cannot find User" });
            return;
        }

        const isPaswordCorrect = await bcrypt.compare(password, user.password || "");
        if (!isPaswordCorrect) {
            res.status(400).json({ error: "Invalid Login Credentials" });
            return;
        }

        res.cookie("jwt", "", { maxAge: 0 });
        const token = generateTokenAndSetCookie(user._id, res);
        const payload = {
            token,
            _id: user._id,
            name: user.name,
            email: user.email
        };

        await client.set(`FGPT-user:${user._id}`, JSON.stringify(payload));
        await client.expire(`FGPT-user:${user._id}`, 30 * 24 * 60 * 60);

        res.status(200)
            .header("Authorization", `Bearer ${token}`)
            .json({
                _id: user._id,
                name: user.name,
                email: user.email,
                chatStreams: user.chatStreams,
                token
            });
    } catch (error) {
        console.log("Error in Login controller", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
}

export const logout = async (req: Request, res: Response) => {
    try {
        const userId = req.params.id;

        res.cookie("FGPT-jwt", "", { maxAge: 0 });
        await client.del(`FGPT-user:${userId}`);

        res.status(200).json({ message: "Logged out successfully" });
    } catch (error) {
        console.log("Error in Logging out", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
}