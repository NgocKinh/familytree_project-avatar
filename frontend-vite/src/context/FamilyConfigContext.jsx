import React, {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import { makeApiUrl } from "../api/apiConfig";
import defaultFamilyConfig from "../config/familyConfig";


const FamilyConfigContext = createContext(defaultFamilyConfig);


export function FamilyConfigProvider({ children }) {
  const [familyConfig, setFamilyConfig] = useState(defaultFamilyConfig);

  useEffect(() => {
    let active = true;

    fetch(makeApiUrl("/setup/config"))
      .then((response) => {
        if (!response.ok) {
          throw new Error("Could not load family configuration");
        }

        return response.json();
      })
      .then((data) => {
        if (active) {
          setFamilyConfig({
            ...defaultFamilyConfig,
            ...data,
          });
        }
      })
      .catch((error) => {
        console.error("L?i t?i c?u h?nh d?ng h?:", error);
      });

    return () => {
      active = false;
    };
  }, []);

  return (
    <FamilyConfigContext.Provider value={familyConfig}>
      {children}
    </FamilyConfigContext.Provider>
  );
}


export function useFamilyConfig() {
  return useContext(FamilyConfigContext);
}
