import { Request, Response } from "express";
import jwt from "jsonwebtoken";
import { AdminToken } from "../types";
import mongoose from "mongoose";
import Stock from "../models/stockData.model";

export const getAdminToken = async (req: Request, res: Response) => {
    try {
        const { password }: AdminToken = req.body;
        const adminPassword = process.env.ADMIN_PASSWORD!;

        if (password !== adminPassword) {
            res.status(401).json({ error: "Invalid Admin Credentials" });
            return;
        }

        const payload = {
            adminPassword,
        };

        const token = jwt.sign(payload, process.env.JWT_SECRET!, { expiresIn: "5h" });
        res.status(200).json(token);
    } catch (error) {
        console.log("Error in getting Admin Token", error);
        res.status(500).json({ error: "Internal Server error" });
    }
}

export const populateDummyStock = async (req: Request, res: Response) => {
    try {
        const userId = req.params.id;

        if (!mongoose.Types.ObjectId.isValid(userId)) {
            res.status(400).json({ message: "Invalid user ID" });
            return;
        }

        const dummyStocks = [
            { stock: "AAPL", holding: Math.floor(Math.random() * 100) },
            { stock: "TSLA", holding: Math.floor(Math.random() * 100) },
            { stock: "GOOGL", holding: Math.floor(Math.random() * 100) },
            { stock: "MSFT", holding: Math.floor(Math.random() * 100) }
        ];

        let stockRecord = await Stock.findOne({ userId });

        if (stockRecord) {
            stockRecord.stocks.push(...dummyStocks);
            await stockRecord.save();
        } else {
            stockRecord = new Stock({
                userId,
                stocks: dummyStocks
            });
            await stockRecord.save();
        }

        res.status(201).json({ message: "Dummy stock data added successfully", stockRecord });
    } catch (error) {
        console.log("Error in populateDummyStock admin controller", error);
        res.status(500).json({ message: "Internal server error" });
    }
};
