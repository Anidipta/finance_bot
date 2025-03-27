import { useState } from "react"
import toast from "react-hot-toast";
import { ChatProps } from "../types";

const useAppendChats = () => {
    const [loading, setLoading] = useState(false);
    const apiUrl = import.meta.env.VITE_API_URL;

    const append = async ({ id, sender, message }: ChatProps) => {
        const success = handleInputErrors({ id, sender, message });

        if (!success) return;

        setLoading(true);
        try {
            const res = await fetch(`${apiUrl}/chat-stream/agent-chat/${id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("FGPT-token")}`
                },
                body: JSON.stringify({ sender, message })
            });
            const data = await res.json();

            if (data.error) {
                throw new Error(data.error)
            }

            if (data) {
                return data;
            }
        } catch (error) {
            if (error instanceof Error) {
                toast.error(error.message);
                console.log(error);
            } else {
                console.log("An unknown error occurred", error);
            }
        } finally {
            setLoading(false);
        }
    }

    return { loading, append }
}

export default useAppendChats;


function handleInputErrors({ id, sender, message }: ChatProps) {
    if (!sender || !message || !id) {
        toast.error("Error in sending message");
        return false;
    }

    if (sender !== "user" && sender !== "agent") {
        toast.error("Error in sending message");
        return false;
    }

    return true;
}