import { notifications } from "@mantine/notifications";
import {Divider, Text, type NotificationProps} from '@mantine/core';
import { LuCheck, LuInfo, LuX } from "react-icons/lu";

export type NotificationType = 'default' | 'info' | 'success' | 'error';

export interface CustomNotificationOptions extends NotificationProps{
    type?:NotificationType;
    subtitle?: string;
    description?: string;
    autoClose?: number | false;
}

const defaultIcon: Record <NotificationType, React.ReactNode> = {
    default: '',
    info: <LuInfo size = {18}/>,
    success: <LuCheck size = {18}/>,
    error: <LuX size = {18}/>
}

export const CustomNotifications = {
    show:({
        type= 'default',
        title,
        subtitle,
        description, 
        icon,
        children : message,
        ...props   
    }: CustomNotificationOptions) => {
        // create the final message : subtitle + description
        let finalMessage: React.ReactNode = message;
        if (subtitle || description){
            finalMessage = (
                <>
                    {subtitle && (
                        <Text fw={500} size="sm" c="#fff" opacity={0.8}>{subtitle}</Text>
                    )}
                    <Divider my="xs" opacity={0.5}/>
                    {description && (
                        <Text fw={500} size="sm" c="#fff" opacity={0.7}>{description}</Text>
                    )}
                </>
            );
        }
        notifications.show({
            ...props,
            title,
            message: finalMessage,
            icon: icon??defaultIcon[type],
            color: props.color?? (type === 'error'?'red':type==='success'?'#009688':'blue'),
            autoClose: props.autoClose??(type === 'success'? 4000 : false),
        });
    },
};