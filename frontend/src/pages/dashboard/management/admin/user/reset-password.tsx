import type {UserUpdate} from "@client/schemas";
import {useForm} from "@mantine/form";
import {Button, Modal, Stack, TextInput, type StackProps} from "@mantine/core";
import {FormProvider} from "@components/forms/form-provider";
import {useEffect, useState} from "react";
import {usersUpdatedByAdmin} from "@client/services/users";
import {notifications} from "@mantine/notifications";
import {HandleError} from "utilities/handleError";

interface ResetPasswordModalProps extends Omit<StackProps, "children"> {
    opened: boolean;
    onClose: () => void;
    onSuccess?: () => void;
    user?: Partial<UserUpdate>; // pour l'édition
}

export function ResetPasswordModal({
    user,
    opened,
    onClose,
    onSuccess,
    ...props
}: ResetPasswordModalProps) {
    const form = useForm<Partial<UserUpdate>>({
        mode: "uncontrolled",
        validate: {
            password: (value) =>
                value?.length
                    ? value.length < 6
                        ? "Password must include at least 6 characters"
                        : null
                    : null,
        },
    });
    const [formInitialized, setFormInitialized] = useState(false);

    useEffect(() => {
        if (!opened) {
            if (formInitialized) setFormInitialized(false);
        } else {
            if (!formInitialized) {
                if (user) {
                    form.setValues({
                        password: "",
                    });
                    setFormInitialized(true);
                }
            }
        }
    }, [opened, formInitialized, setFormInitialized, user, form]);

    const handleSubmit = form.onSubmit(async (values) => {
        try {
            if (user) {
                user.password = values.password;
                user.is_password_reinitialized = true;
                await usersUpdatedByAdmin(user);

                onSuccess?.();
                onClose();
                //if(user_added)
                notifications.show({
                    title: "Succès",
                    message: "Mot de passe réinitialisé avec succès.",
                    color: "green",
                });
            }

            form.reset();
        } catch (error) {
            HandleError(error);
        }
    });

    return (
        <Modal
            opened={opened}
            onClose={onClose}
            title="Reset Password Confirmation">
            <FormProvider form={form} onSubmit={handleSubmit}>
                <Stack {...props}>
                    <TextInput
                        label="Temporary Password"
                        {...form.getInputProps("password")}
                    />
                    <Button type="submit">Reset Password</Button>
                </Stack>
            </FormProvider>
        </Modal>
    );
}
