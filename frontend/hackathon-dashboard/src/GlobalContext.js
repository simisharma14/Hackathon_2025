import { createContext, useContext, useState } from "react";

// Create Context
const GlobalContext = createContext();

// Global Provider Component
export const GlobalProvider = ({ children }) => {
    const [userData, setUserData] = useState({
        name: "",
        energyType: "",
        riskType: ""
    });

    return (
        <GlobalContext.Provider value={{ userData, setUserData }}>
            {children}
        </GlobalContext.Provider>
    );
};

// Custom Hook for Accessing Context
export const useGlobalContext = () => {
    return useContext(GlobalContext);
};
