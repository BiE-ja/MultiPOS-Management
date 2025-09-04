import { CustomNotifications, type NotificationType } from "@components/customNotification";
import { notifications, Notifications } from "@mantine/notifications";

import { ZodError } from "zod";


export function HandleError( payload : unknown){
    let title = 'Erreur innatendu!';
    const type: NotificationType = "error"
    const autoClose=false;
    let message= "Un erreur innatendu est survenu";

    if (payload instanceof ZodError){
        title= "Données invalides"
        message = "Les données fournies ne sont pas correctes";
    }

    notifications.show({
        title,
        message,
        color:'red',
    })
    

    
    if (payload instanceof Error)
      console.log(payload);
        
      throw payload;
}