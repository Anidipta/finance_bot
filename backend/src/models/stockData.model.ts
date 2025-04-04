import mongoose from "mongoose";

const StockSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "User",
        required: true
    },
    stocks: [
        {
            stock: {
                type: String,
                required: true
            },
            holding: {
                type: Number,
                required: true
            }
        }
    ]
}, { timestamps: true });

const Stock = mongoose.model("Stock", StockSchema);
export default Stock;