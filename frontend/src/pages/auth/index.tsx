import {
    PiGoogleLogoDuotone as GoogleIcon,
    PiXLogoDuotone as XIcon,
} from "react-icons/pi";

import {
    Anchor,
    Button,
    Divider,
    Group,
    Stack,
    Text,
    Title,
} from "@mantine/core";

import {LoginForm} from "./login";
import {Page} from "@components/page";
import {UnderlineShape} from "@components/underline-shape";
import {Link} from "@tanstack/react-router";

export default function LoginPage() {
    return (
        <Page title="Login">
            <Stack gap="xl">
                <Stack>
                    <Title order={2}>
                        Tongasoa!{" "}
                        <Text
                            fz="inherit"
                            fw="inherit"
                            component="span"
                            pos="relative">
                            Sign in
                            <UnderlineShape
                                c="blue"
                                left="0"
                                pos="absolute"
                                h="0.625rem"
                                bottom="-1rem"
                                w="7rem"
                            />
                        </Text>{" "}
                        to continue.
                    </Title>
                    <Text fz="sm" c="dimmed">
                        Mangataka anao hampiditra ny mombamomba anao. Angataho
                        amin'ny tompon'andraikitry ny toerana fiasanao izany
                        raha tsy mbola anananao.
                    </Text>
                </Stack>

                <Group grow>
                    <Button
                        leftSection={<XIcon size="1rem" />}
                        variant="outline"
                        color="gray">
                        Login with X
                    </Button>
                    <Button
                        leftSection={<GoogleIcon size="1rem" />}
                        variant="outline"
                        color="gray">
                        Login with Google
                    </Button>
                </Group>

                <Divider label="OR" labelPosition="center" />

                <LoginForm />

                <Text fz="sm" c="dimmed">
                    Don&apos;t have an account?{" "}
                    <Anchor fz="inherit" component={Link} to={"auth/sign-up"}>
                        Register
                    </Anchor>
                </Text>
            </Stack>
        </Page>
    );
}
