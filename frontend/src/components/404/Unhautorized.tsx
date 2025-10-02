import {Container, Title, Text, Button, Group} from "@mantine/core";

import classes from "./NothingFoundBackground.module.css";
import {Illustration} from "./Illustration";

export function UnhautorizedBackground() {
    return (
        <Container className={classes.root}>
            <div className={classes.inner}>
                <Illustration className={classes.image} />
                <div className={classes.content}>
                    <Title className={classes.title}>Nothing to see here</Title>
                    <Text
                        c="dimmed"
                        size="lg"
                        ta="center"
                        className={classes.description}>
                        You don't have enough privilege to acced this content.
                        If you think this is an error contact support.
                    </Text>
                    <Group justify="center">
                        <Button size="md">Take me back to home page</Button>
                    </Group>
                </div>
            </div>
        </Container>
    );
}
