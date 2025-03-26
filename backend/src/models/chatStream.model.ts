import mongoose from "mongoose";

const ChatStreamSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Users",
        required: true
    },
    header: {
        type: String,
        min: 1
    },
    chats: [
        {
            sender: {
                type: String,
                enum: ["user", "agent"],
                required: true
            },
            message: {
                type: String,
                required: true
            }
        }
    ]
}, { timestamps: true });

const ChatStream = mongoose.model("ChatStream", ChatStreamSchema);
export default ChatStream;