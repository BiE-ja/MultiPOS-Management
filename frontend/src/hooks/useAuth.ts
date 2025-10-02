import {useQuery, useQueryClient} from "@tanstack/react-query";
import {useNavigate} from "@tanstack/react-router";
import {useState} from "react";

import {
    type BodyAuthLogin as AccessToken,
    type UserPublic,
} from "@client/schemas";

import {useAuthLogin} from "@client/services/auth";
import {usersAuth, usersReadMe} from "@client/services/users";
import {HandleError} from "utilities/handleError";
import {CustomNotifications} from "@components/customNotification";
import {useAuthContext} from "./useAuthContext";
import {paths} from "config/paths";

const isLoggedIn = () => {
    return localStorage.getItem("access_token") !== null;
};

const useAuth = () => {
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const {data: user} = useQuery<UserPublic | null, Error>({
        queryKey: ["currentUser"],
        queryFn: () => usersReadMe(),
        enabled: isLoggedIn(),
    });

    // Pas besoin pour mon cas car aucun n'utilisateur ne peux créer un compte seul
    // Seul le super_admin et l'user owner peut créer des utilisateurs
    /*const signUpMutation = useMutation({
    mutationFn: (data: UserRegister) => usersRegister( data ),
    onSuccess: () => {
      navigate({ to: "/login" })
    },
    onError: (err: HTTPValidationError) => {
      HandleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] })
    },
  })*/

    // utilisation du context de l'authProvider
    const {setUser, setIsAuthenticated} = useAuthContext();

    const {mutateAsync: login, isPending} = useAuthLogin();

    const loginMutation = async (data: AccessToken) => {
        try {
            const token = await login({data});
            // enregistrement du token
            localStorage.setItem("access_token", token.access_token);
            // synchronisation avec le contexte
            let me = user;
            if (me == null || me == undefined) me = await usersAuth();
            setUser(me);
            setIsAuthenticated(true);
            // redirection vers l'acceuil correspondant
            navigate({to: paths.dashboard.home});
            // Affichage d'une notification
            CustomNotifications.show({
                type: "success",
                title: "Tongasoa!",
                children: "You have successfully logged in",
            });

            await queryClient.invalidateQueries({queryKey: ["users"]});
        } catch (err) {
            HandleError(err);
            throw err;
        }
    };

    const logout = () => {
        localStorage.removeItem("access_token");
        setUser(null);
        setIsAuthenticated(false);
        navigate({to: paths.auth.login});
        CustomNotifications.show({
            type: "success",
            title: "Veloma!",
            children: "You have successfully logged out",
        });
    };

    return {
        //signUpMutation,
        loginMutation,
        logout,
        isPending,
        user,
        setIsAuthenticated,
        error,
        resetError: () => setError(null),
    };
};

export {isLoggedIn};
export default useAuth;
