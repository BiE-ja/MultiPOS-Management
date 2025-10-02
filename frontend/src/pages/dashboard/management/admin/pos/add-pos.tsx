import type {AreaCreate, AreaDetails} from "@client/schemas";
import {zoneCreate, zoneUpdate} from "@client/services/zone";
import {useForm} from "@mantine/form";
import {notifications} from "@mantine/notifications";
import {HandleError} from "utilities/handleError";
import {Modal, TextInput, Button, Stack} from "@mantine/core";
import {FormProvider} from "@components/forms/form-provider";
import {type AreaUpdate} from "client/schemas/areaUpdate";

type PosFormProps = {
    opened: boolean;
    onClose: () => void;
    pos?: Partial<AreaDetails>; // pour l'édition
    ownerId?: string;
};

export function AddPos({opened, onClose, pos, ownerId}: PosFormProps) {
    const form = useForm<AreaDetails>({
        initialValues: {
            id: pos?.id ?? "",
            name: pos?.name ?? "",
            location: pos?.location ?? "",
            created_at: pos?.created_at,
            owner_id: pos?.owner_id ?? ownerId ?? "",
        },
    });

    const handleSubmit = form.onSubmit(async (pos_form: AreaCreate) => {
        try {
            if (pos) {
                const pos_updated: AreaUpdate = {
                    location: pos_form.location as string,
                    ...pos_form,
                };

                await zoneUpdate(pos.id as string, pos_updated);
            } else await zoneCreate(pos_form);

            onClose();

            notifications.show({
                title: "Succès",
                message: `Le point de vente a été ${
                    pos ? "modifié" : "créé"
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
            title={
                pos
                    ? "Modification d'un point de vente"
                    : "Création d'un point de vente"
            }>
            <FormProvider form={form} onSubmit={handleSubmit}>
                <Stack>
                    <TextInput
                        label="Nom du point de vente"
                        {...form.getInputProps("name")}
                    />
                    <TextInput
                        label="Localisation"
                        {...form.getInputProps("location")}
                    />

                    <Button type="submit">{pos ? "Modifier" : "Créer"}</Button>
                </Stack>
            </FormProvider>
        </Modal>
    );
}
