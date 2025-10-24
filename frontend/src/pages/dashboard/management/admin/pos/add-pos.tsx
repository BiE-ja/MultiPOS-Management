import type {AreaCreate, AreaDetails} from "@client/schemas";
import {zoneCreate, zoneUpdate} from "@client/services/zone";
import {useForm} from "@mantine/form";
import {notifications} from "@mantine/notifications";
import {HandleError} from "utilities/handleError";
import {Modal, TextInput, Button, Stack} from "@mantine/core";
import {FormProvider} from "@components/forms/form-provider";
import {type AreaUpdate} from "client/schemas/areaUpdate";
import {useEffect, useState} from "react";

type PosFormProps = {
    opened: boolean;
    onClose: () => void;
    onSuccess?: () => void;
    pos?: Partial<AreaDetails>; // pour l'édition
    ownerId?: string;
};

export function AddPos({
    opened,
    onClose,
    onSuccess,
    pos,
    ownerId,
}: PosFormProps) {
    const form = useForm<AreaDetails>({
        initialValues: {
            id: "",
            name: "",
            location: "",
            state: "active",
            created_at: undefined,
        },
    });

    const [formInitialized, setFormInitialized] = useState(false);
    // remplir le formulaire si "pos" est défini (édition)
    // Réinitialiser le formulaire lorsque la modale est fermée
    useEffect(() => {
        if (!opened) {
            if (formInitialized) setFormInitialized(false);
        } else {
            if (!formInitialized) {
                if (pos) form.setValues({...pos});
                setFormInitialized(true);
            }
        }
    }, [opened, formInitialized, pos, setFormInitialized, form]);

    // gestion de la soumission du formulaire

    const handleSubmit = form.onSubmit(async (pos_form: AreaCreate) => {
        try {
            // si "pos" a été défini au préalable, il s'agit d'une mise à jour
            if (pos) {
                const pos_updated: AreaUpdate = {
                    location: pos_form.location as string,
                    ...pos_form,
                };

                await zoneUpdate(pos.id as string, pos_updated);
            } else {
                // sinon création
                pos_form.owner_id = ownerId;
                await zoneCreate(pos_form);
            }
            onSuccess?.();
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
            }
            size="md">
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
