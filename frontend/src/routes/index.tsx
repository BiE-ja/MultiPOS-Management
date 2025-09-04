
import {  createFileRoute, redirect } from "@tanstack/react-router"


import { paths } from "../config/paths"
import { isLoggedIn } from "hooks/useAuth"


export const Route = createFileRoute(paths.index.root)({
  component: () => null,
  beforeLoad: async () => {
    if (!isLoggedIn()) {
      throw redirect({
        to: paths.auth.login,
      });
    }
  },
});

