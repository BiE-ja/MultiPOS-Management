import {
  MutationCache,
  QueryCache,
  QueryClient,
  QueryClientProvider
} from "@tanstack/react-query"
import { StrictMode } from 'react';
import {RouterProvider, createRouter} from "@tanstack/react-router"

import { CustomProvider } from "provider/CustomProvider";

import { isAxiosError } from "axios";

import ReactDOM from "react-dom/client";
import { routeTree } from "routeTree.gen";
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';



const handleApiError = (error: Error) => {
  if  (isAxiosError(error)){
    const status = error.response?.status;
    if (status === 401 || status === 403){
      localStorage.removeItem("access_token");
      if(!window.location.pathname.startsWith("/login")){
        window.location.href="/login";
      }
    }
  }
}
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: handleApiError,
  }),
  mutationCache: new MutationCache({
    onError: handleApiError,
  }),
})

const router = createRouter({ routeTree })
declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router
  }
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <CustomProvider>
      <QueryClientProvider client={queryClient}>
         <RouterProvider router={router} />
      </QueryClientProvider>
    </CustomProvider>
  </StrictMode>,
)