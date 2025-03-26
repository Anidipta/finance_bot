import express from "express";
import verifyToken from "../middlewares/auth.middleware";
import { appendChats, createChatStream, getChatStreamById, getMyChatStreams } from "../controllers/chatStream.controller";

const router = express.Router();

router.post("/create-stream", verifyToken, createChatStream);
router.post("/agent-chat/:id", verifyToken, appendChats);
router.get("/my-chats", verifyToken, getMyChatStreams);
router.get("/get-chat/:id", verifyToken, getChatStreamById);

export default router;