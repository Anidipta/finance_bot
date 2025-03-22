import { useState } from "react"
import toast from "react-hot-toast";
import { SignupParams } from "../types";
import { useAuthContext } from "../context/AuthContext";

const useSignup = () => {
    const [loading, setLoading] = useState(false);
    const { setAuthUser } = useAuthContext();
    const apiUrl = import.meta.env.VITE_API_URL;

    const signup = async ({
        name,
        email,
        password
    }: SignupParams) => {
        const success = handleInputErrors({
            name,
            email,
            password
        });
        if (!success) return;

        setLoading(true);
        try {
            const res = await fetch(`${apiUrl}/auth/signup`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("FR-token")}`
                },
                body: JSON.stringify({
                    name,
                    email,
                    password
                })
            });
            const data = await res.json();

            if (data.error) {
                throw new Error(data.error);
            }

            localStorage.setItem("FGPT-token", data.token);
            localStorage.setItem("FGPT-user", JSON.stringify(data));
            setAuthUser(data);

            if (data) {
                toast.success("Signed up Successfully");
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
    return { loading, signup };
}

export default useSignup;


function handleInputErrors({
    name,
    email,
    password
}: SignupParams) {
    if (!name || !email || !password) {
        toast.error("Please fill all the fields");
        return false;
    }

    if (name.length < 2) {
        toast.error("Name should be atleast 2 characters long");
        return false;
    }

    if (password.length < 6) {
        toast.error("Password should be atleast 6 characters long");
        return false;
    }

    return true;
}