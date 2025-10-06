import {Outlet, createRootRoute} from "@tanstack/react-router";
import {LazyPage} from "layouts/lazy-page";

import React, {Suspense} from "react";

const loadDevtools = () =>
    Promise.all([
        import("@tanstack/react-router-devtools"),
        import("@tanstack/react-query-devtools"),
    ]).then(([routerDevtools, reactQueryDevtools]) => {
        return {
            default: () => (
                <>
                    <routerDevtools.TanStackRouterDevtools />
                    <reactQueryDevtools.ReactQueryDevtools />
                </>
            ),
        };
    });

const TanStackDevtools =
    process.env.NODE_ENV === "production"
        ? () => null
        : React.lazy(loadDevtools);

const NotFound = LazyPage(() => import("pages/dashboard/notFound"));

export const Route = createRootRoute({
    component: () => (
        <>
            <Outlet />
            <Suspense>
                <TanStackDevtools />
            </Suspense>
        </>
    ),
    notFoundComponent: () => NotFound,
});
