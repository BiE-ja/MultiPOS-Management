import type {UserAuth} from "@client/schemas";
import {getDashboardPathForRole} from "config/roles";
import {paths} from "config/paths";

export const emailPattern = {
    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
    message: "Invalid email address",
};

export const namePattern = {
    value: /^[A-Za-z\s\u00C0-\u017F]{1,30}$/,
    message: "Invalid name",
};

export const passwordRules = (isRequired = true) => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const rules: any = {
        minLength: {
            value: 8,
            message: "Password must be at least 8 characters",
        },
    };

    if (isRequired) {
        rules.required = "Password is required";
    }

    return rules;
};

export const confirmPasswordRules = (
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    getValues: () => any,
    isRequired = true
) => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const rules: any = {
        validate: (value: string) => {
            const password = getValues().password || getValues().new_password;
            return value === password ? true : "The passwords do not match";
        },
    };

    if (isRequired) {
        rules.required = "Password confirmation is required";
    }

    return rules;
};

// to redirect user to the dashbord
export function userHome(user: UserAuth) {
    const redirect = paths.dashboard.home;
    if (user.roles.length < 1) getDashboardPathForRole(user.roles[0].name);

    return redirect;
}

// Check if user is logged in
const isLoggedIn = () => {
    return localStorage.getItem("access_token") !== null;
};

export {isLoggedIn};
