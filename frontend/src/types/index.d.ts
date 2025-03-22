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
