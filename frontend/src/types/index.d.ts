export interface SignupParams {
    name: string;
    email: string;
    password: string;
}

export interface LoginParams {
    email: string;
    password: string;
}

export interface AuthUser {
    uid: string;
    name: string;
    email: string;
    chatStreams: string[];
}

export interface AuthContextType {
    authUser: AuthUser | null;
    setAuthUser: React.Dispatch<React.SetStateAction<AuthUser | null>>;
}

export interface AuthContextProviderProps {
    children: ReactNode;
}

export interface ChatHistory {
    id: string;
    header: string;
    createdAt: string;
}

export interface ChatProps {
    id: string;
    sender: "user" | "agent";
    message: string;
}

export interface Chats {
    sender: "user" | "agent";
    message: string;
    _id: string;
}

export interface Messages {
    _id: string;
    userId: string;
    chats: Chats[];
    header: string;
    createdAt: string;
    updatedAt: string;
}