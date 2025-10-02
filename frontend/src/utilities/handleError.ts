import {notifications} from "@mantine/notifications";

import {ZodError} from "zod";

export function HandleError(payload: unknown) {
    let title = "Erreur innatendu!";

    let message = "Une erreur innatendu est survenu";

    if (payload instanceof ZodError) {
        title = "Données invalides";
        message = "Les données fournies ne sont pas correctes";
    }

    notifications.show({
        title,
        message,
        color: "red",
    });

    if (payload instanceof Error) console.log(payload);

    throw payload;
}
