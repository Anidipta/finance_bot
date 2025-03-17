import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const getGeminiResponse = async (message: string): Promise<string> => {
    try {
        const response = await axios.post(`${API_URL}/api/gemini`, { message });
        return response.data.response;
    } catch (error) {
        console.error("Error fetching response:", error);
        return "Sorry, something went wrong!";
    }
};