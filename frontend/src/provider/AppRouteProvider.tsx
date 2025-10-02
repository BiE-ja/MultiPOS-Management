// src/provider/AppRouterProvider.tsx
import {createRouter, RouterProvider} from "@tanstack/react-router";
import {useAuthContext} from "hooks/useAuthContext";
//import {useMemo} from "react";
import {routeTree} from "routeTree.gen";

const router = createRouter({routeTree});
declare module "@tanstack/react-router" {
    interface Register {
        router: typeof router;
    }
}

export default function AppRouterProvider() {
    // utilisation du context de l'authProvider
    const auth = useAuthContext();

    return <RouterProvider router={router} context={auth} />;
}
