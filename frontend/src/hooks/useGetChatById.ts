import { useState } from "react"
import toast from "react-hot-toast";

const useGetChatById = () => {
    const [loading, setLoading] = useState(false);
    const apiUrl = import.meta.env.VITE_API_URL;

    const chat = async (id: string) => {
        setLoading(true);
        console.log(id);
        try {
            const res = await fetch(`${apiUrl}/chat-stream/get-chat/${id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("FGPT-token")}`
                },
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

    return { loading, chat }
}

export default useGetChatById;