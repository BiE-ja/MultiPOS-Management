import type {UserCreate, UserRead, UserUpdate} from "@client/schemas";
import {
    usersCreateUserBySuperUser as addUser,
    usersUpdatedByAdmin as updateUser,
} from "@client/services/users";
import {Select} from "@components/forms";
import {FormProvider} from "@components/forms/form-provider";
import {
    Modal,
    TextInput,
    Button,
    Stack,
    Group,
    type StackProps,
} from "@mantine/core";
import {useForm} from "@mantine/form";
import {notifications} from "@mantine/notifications";
import {useEffect, useState} from "react";
import {HandleError} from "utilities/handleError";

interface UserFormProps extends Omit<StackProps, "children"> {
    opened: boolean;
    view?: boolean;
    onClose: () => void;
    onSuccess?: () => void;
    user?: Partial<UserRead>; // pour l'édition
}

/*const Role = [
    {value: "manager", label: "Manager"},
    {value: "saler", label: "Vendeur"},
    {value: "stock-keeper", label: "Magasiner"},
];*/

const isTrue = ["true", "false"];

function verify(value: string) {
    if (value == "true") {
        return true;
    }
    return false;
}

export function AddUser({
    opened,
    view,
    onClose,
    onSuccess,
    user,
    ...props
}: UserFormProps) {
    const form = useForm<UserCreate>({
        initialValues: {
            name: "",
            last_name: "",
            email: "",
            phone: "",
            password: "",
            created_at: undefined,
            is_active: true,
            is_owner: true,
            is_superuser: false,
        },
        transformValues: (values) => ({
            ...values,
            is_active: verify(values.is_active as unknown as string),
            is_owner: verify(values.is_owner as unknown as string),
            is_superuser: verify(values.is_superuser as unknown as string),
        }),
    });

    const [formInitialized, setFormInitialized] = useState(false);
    const [isDisabled, setIsDisabled] = useState(false);

    const enableEdition = () => {
        setIsDisabled(false);
    };

    // Si "owner" est défini,
    // on initialise les valeurs du formulaire avec les données de l'utilisateur à modifier

    useEffect(() => {
        if (!opened) {
            if (formInitialized) {
                form.reset();
                setFormInitialized(false);
            }
        } else {
            if (!formInitialized) {
                if (user) {
                    form.setValues({
                        name: user?.name ?? "",
                        last_name: user?.last_name ?? "",
                        email: user?.email ?? "",
                        phone: user?.phone ?? "",
                        created_at: user?.created_at,
                        is_active: user?.is_active ?? true,
                        is_owner: user?.is_owner ?? true,
                        is_superuser: user?.is_superuser ?? false,
                    });
                }
                setFormInitialized(true);
                setIsDisabled(view ? view : false);
            }
            //setIsDisabled(view ? !view : false);
        }
    }, [opened, formInitialized, setFormInitialized, user, view, form]);

    const handleSubmit = form.onSubmit(async (user_form: UserCreate) => {
        try {
            // si "owner" a été défini au préalable, il s'agit d'une mise à jour
            if (user) {
                // Pour éviter de mettre à jour les champs non concerné par la mise à jour
                // (mot de passe, date de création,...), on crée une nouvelle objet.
                // A noter que ces champs ont été initialisé dans "initialValues" de la "form"
                const user_update: UserUpdate = {
                    name: user_form.name,
                    last_name: user_form.last_name,
                    email: user_form.email,
                    is_active: user_form.is_active,
                    is_owner: user_form.is_owner,
                    is_superuser: user_form.is_superuser,
                };
                await updateUser(user_update);
            } else {
                // sinon création
                await addUser(user_form);
            }
            onSuccess?.();
            onClose();
            //if(user_added)
            notifications.show({
                title: "Succès",
                message: `L'utilisateur a été ${
                    user ? "modifié" : "créé"
                } avec succès`,
                color: "green",
            });
            form.reset();
        } catch (error) {
            HandleError(error);
        }
    });

    return (
        <Modal
            opened={opened}
            onClose={onClose}
            title={user ? "Edit Owner" : "Create Owner"}
            size={{base: "xs", md: "md"}}>
            {view && (
                <Button variant="default" size="xs" onClick={enableEdition}>
                    Edit...
                </Button>
            )}
            <FormProvider form={form} onSubmit={handleSubmit}>
                <Stack {...props}>
                    <Group>
                        <TextInput
                            label="Last Name"
                            {...form.getInputProps("last_name")}
                            disabled={isDisabled}
                        />

                        <TextInput
                            label="First Name"
                            {...form.getInputProps("name")}
                            disabled={isDisabled}
                        />
                    </Group>
                    <TextInput
                        label="Email"
                        {...form.getInputProps("email")}
                        disabled={isDisabled}
                    />
                    <TextInput
                        label="Phone number"
                        {...form.getInputProps("phone")}
                        disabled={isDisabled}
                    />
                    <Select
                        label="Super utilisateur"
                        name="is_superuser"
                        data={isTrue}
                        clearable
                        {...form.getInputProps("is_superuser")}
                        disabled={isDisabled}
                    />
                    <Select
                        label="Owner"
                        name="is_owner"
                        data={isTrue}
                        clearable
                        {...form.getInputProps("is_owner")}
                        disabled={isDisabled}
                    />
                    <Select
                        label="Actif"
                        name="is_active"
                        data={isTrue}
                        clearable
                        {...form.getInputProps("is_active")}
                        disabled={isDisabled}
                    />
                    {!user && (
                        <TextInput
                            label="Temporary password"
                            {...form.getInputProps("password")}
                            disabled={isDisabled}
                        />
                    )}
                    {!isDisabled && (
                        <Button type="submit">{user ? "Edit" : "Add"}</Button>
                    )}
                </Stack>
            </FormProvider>
        </Modal>
    );
}
