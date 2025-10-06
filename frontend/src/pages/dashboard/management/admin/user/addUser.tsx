import type {
    UserCreate,
    UserRead,
    UserUpdate,
    UserUpdateEmail,
    UserUpdateIsActive,
    UserUpdateIsOwner,
    UserUpdateIsSuperuser,
    UserUpdateLastName,
    UserUpdateName,
} from "@client/schemas";
import {
    usersCreateUserBySuperUser as addUser,
    usersUpdatedByAdmin as updateUser,
} from "@client/services/users";
import {Select} from "@components/forms";
import {FormProvider} from "@components/forms/form-provider";
import {Modal, TextInput, Button, Stack, Flex} from "@mantine/core";
import {useForm} from "@mantine/form";
import {notifications} from "@mantine/notifications";
import {HandleError} from "utilities/handleError";

type OwnerFormProps = {
    opened: boolean;
    onClose: () => void;
    onSuccess?: () => void;
    owner?: Partial<UserRead>; // pour l'édition
};

/*const Role = [
    {value: "manager", label: "Manager"},
    {value: "saler", label: "Vendeur"},
    {value: "stock-keeper", label: "Magasiner"},
];*/

const isTrue = [
    {value: "true", label: "Oui"},
    {value: "false", label: "Non"},
];

function verify(value: string) {
    if (value == "true") {
        return true;
    }
    return false;
}

export function AddUser({opened, onClose, onSuccess, owner}: OwnerFormProps) {
    const form = useForm<UserCreate>({
        initialValues: {
            name: owner?.name ?? "",
            last_name: owner?.last_name ?? "",
            email: owner?.email ?? "",
            phone: owner?.phone ?? "",
            password: "",
            created_at: owner?.created_at,
            is_active: owner?.is_active ?? true,
            is_owner: owner?.is_owner ?? true,
            is_superuser: owner?.is_superuser ?? false,
        },
        transformValues: (values) => ({
            ...values,
            is_active: verify(values.is_active as unknown as string),
            is_owner: verify(values.is_owner as unknown as string),
            is_superuser: verify(values.is_superuser as unknown as string),
        }),
    });

    const handleSubmit = form.onSubmit(async (user: UserCreate) => {
        try {
            // si "owner" a été défini au préalable, il s'agit d'une mise à jour
            if (owner != undefined) {
                // Pour éviter de mettre à jour les champs non concerné par la mise à jour
                // (mot de passe, date de création,...), on crée une nouvelle objet.
                // A noter que ces champs ont été initialisé dans "initialValues" de la "form"
                const user_update = () => ({
                    name: user.name as UserUpdateName,
                    last_name: user.last_name as UserUpdateLastName,
                    email: user.email as UserUpdateEmail,
                    is_active: user.is_active as UserUpdateIsActive,
                    is_owner: user.is_owner as UserUpdateIsOwner,
                    is_superuser: user.is_superuser as UserUpdateIsSuperuser,
                });
                await updateUser(owner.id as string, user_update as UserUpdate);
            } else await addUser(user);
            onSuccess?.();
            onClose();
            //if(user_added)
            notifications.show({
                title: "Succès",
                message: `L'utilisateur a été ${
                    owner ? "modifié" : "créé"
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
            title={owner ? "Edit Owner" : "Create Owner"}>
            <FormProvider form={form} onSubmit={handleSubmit}>
                <Stack>
                    <Flex direction={"column"} gap={4}>
                        <TextInput
                            label="Nom"
                            {...form.getInputProps("last_name")}
                        />

                        <TextInput
                            label="Prénom"
                            {...form.getInputProps("name")}
                        />
                    </Flex>
                    <TextInput label="Email" {...form.getInputProps("email")} />
                    <TextInput
                        label="Téléphone"
                        {...form.getInputProps("phone")}
                    />
                    <Select
                        label="Super utilisateur"
                        name="is_superuser"
                        data={isTrue}
                        defaultValue="Non"
                        clearable
                        {...form.getInputProps("is_superuser")}
                    />
                    <Select
                        label="Propriétaire"
                        name="is_owner"
                        data={isTrue}
                        defaultValue="Oui"
                        clearable
                        {...form.getInputProps("is_owner")}
                    />
                    <Select
                        label="Actif"
                        name="is_active"
                        data={isTrue}
                        defaultValue="Oui"
                        clearable
                        {...form.getInputProps("is_active")}
                    />

                    <Button type="submit">
                        {owner ? "Modifier" : "Créer"}
                    </Button>
                </Stack>
            </FormProvider>
        </Modal>
    );
}
