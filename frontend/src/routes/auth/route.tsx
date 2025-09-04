// frontend/src/routes/auth/index.tsx

import {paths} from "config/paths";

import {createFileRoute} from "@tanstack/react-router";
import {AuthLayout} from "layouts/auth/authLayout";

export const Route = createFileRoute(paths.auth.root)({
    component: () => {
        return <AuthLayout />;
    },
});
