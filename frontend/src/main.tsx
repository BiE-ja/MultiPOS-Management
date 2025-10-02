import {
    MutationCache,
    QueryCache,
    QueryClient,
    QueryClientProvider,
} from "@tanstack/react-query";
import {StrictMode} from "react";

import {CustomProvider} from "provider/CustomProvider";

import {isAxiosError} from "axios";

import ReactDOM from "react-dom/client";
import "@mantine/core/styles.css";

import AppRouterProvider from "provider/AppRouteProvider";

const handleApiError = (error: Error) => {
    if (isAxiosError(error)) {
        const status = error.response?.status;
        if (status === 401 || status === 403) {
            localStorage.removeItem("access_token");
            if (!window.location.pathname.startsWith("/login")) {
                window.location.href = "/login";
            }
        }
    }
};
const queryClient = new QueryClient({
    queryCache: new QueryCache({
        onError: handleApiError,
    }),
    mutationCache: new MutationCache({
        onError: handleApiError,
    }),
});

/*const router = createRouter({routeTree});
declare module "@tanstack/react-router" {
    interface Register {
        router: typeof router;
    }
}

export default function AppRouterProvider() {
    const auth = useAuth();

    return <RouterProvider router={router} context={{auth}} />;
}*/

ReactDOM.createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <CustomProvider>
            <QueryClientProvider client={queryClient}>
                <AppRouterProvider />
            </QueryClientProvider>
        </CustomProvider>
    </StrictMode>
);
