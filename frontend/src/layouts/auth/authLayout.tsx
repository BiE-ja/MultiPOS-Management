import { PiArrowLeft as GoBackIcon } from 'react-icons/pi';

import { Box, Button, Center, Flex, Image, SimpleGrid, Text, Title } from '@mantine/core';
import demoImg from '@/assets/app-demo.webp';
import { Outlet, useNavigate } from '@tanstack/react-router';
import { Logo } from '@components/logo';

export function AuthLayout() {
  const navigate = useNavigate();

  return (
    
      <SimpleGrid mih="100vh" p="md" cols={{ base: 1, lg: 2 }}>
        <Flex direction="column" align="flex-start">
          <Button
            c="inherit"
            variant="subtle"
            leftSection={<GoBackIcon size="1rem" />}
            onClick={() => navigate({to:"/"})}
          >
            Hiverina
          </Button>

          <Center flex={1} w="100%">
            <Box maw="25rem">
              <Logo size="3rem" display="block" c="var(--mantine-primary-color-filled)" mb="xl" />
              <Outlet />
            </Box>
          </Center>
        </Flex>

        <Center
          ta="center"
          p="4rem"
          bg="var(--mantine-color-default-hover)"
          display={{ base: 'none', lg: 'flex' }}
          style={{ borderRadius: 'var(--mantine-radius-md)' }}
        >
          <Box maw="40rem">
            <Title order={2}>Fitaovana tsotra ahafahanao mitantana ny tsenanao.</Title>
            <Text my="lg" c="dimmed">
              Adinoy manomboka androany ireo fotoana very sy lany amin'ny fitantanana ny tsena.
              Mifantoha bebe kokoa amin'ny fampandrosoana ny raharahanao ny fotoanao.
              Hanamora ny fomba fitantananao ny fampiasana an'ity vokatra ity.
            </Text>

            <Image src={demoImg} alt="Demo" />
          </Box>
        </Center>
      </SimpleGrid>
    
  );
}