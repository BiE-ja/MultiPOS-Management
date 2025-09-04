/*import React from "react"
// Chakra imports
import {
  Box,
  Button,
  Checkbox,
  Flex,
  Field as ChakraField,
  Fieldset,
  Heading,
  Icon,
  Input,
  Stack,
  Text,
  Separator,
} from "@chakra-ui/react"

import { useForm, type SubmitHandler } from "react-hook-form"
import { FcGoogle } from "react-icons/fc"
import { Link } from "@tanstack/react-router"
import { LuLock, LuMail } from "react-icons/lu"
import useAuth from "hooks/useAuth"
import type { BodyAuthLogin as AccessToken } from "@client/schemas"
import { emailPattern, passwordRules } from "utilities/utils"
import { InputGroup } from "@components/utils/ui/input-group"
import { useColorModeValue } from "@components/utils/color-mode"
import {
  PasswordInput,
  PasswordStrengthMeter,
} from "@components/utils/ui/password-input"

export function Login() {
  const textColor = useColorModeValue("navy.700", "white")
  const textColorSecondary = "gray.400"
  const textColorDetails = useColorModeValue("navy.700", "secondaryGray.600")
  const textColorBrand = useColorModeValue("brand.500", "white")
  const googleBg = useColorModeValue("secondaryGray.300", "whiteAlpha.200")
  const googleText = useColorModeValue("navy.700", "white")
  const googleHover = useColorModeValue(
    { bg: "gray.200" },
    { bg: "whiteAlpha.300" }
  )
  const googleActive = useColorModeValue(
    { bg: "secondaryGray.300" },
    { bg: "whiteAlpha.200" }
  )
  const [visible, setVisible] = React.useState(false)

  const { loginMutation, resetError } = useAuth()
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<AccessToken>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      username: "",
      password: "",
    },
  })

  const onSubmit: SubmitHandler<AccessToken> = async (data: AccessToken) => {
    if (isSubmitting) return
    resetError()
    try {
      await loginMutation.mutateAsync(data)
    } catch {
      // handled in useAuth
    }
  }

  return (
    <Flex>
      <Flex
        maxW={{ base: "100%", md: "max-content" }}
        w="100%"
        mx={{ base: "auto", lg: "0px" }}
        me="auto"
        h="100%"
        alignItems="start"
        justifyContent="center"
        mb={{ base: "30px", md: "60px" }}
        px={{ base: "25px", md: "0px" }}
        mt={{ base: "40px", md: "14vh" }}
        flexDirection="column"
      >
        <Box me="auto">
          <Heading color={textColor} fontSize="36px" mb="10px">
            Sign In
          </Heading>
          <Text
            mb="36px"
            ms="4px"
            color={textColorSecondary}
            fontWeight="400"
            fontSize="md"
          >
            Enter your email and password to sign in!
          </Text>
        </Box>

        {/* === FORMULAIRE AVEC FIELDSET === *//*}
        <form onSubmit={handleSubmit(onSubmit)}>
          <Fieldset.Root
            size="lg"
            maxW="420px"
            background="transparent"
            borderRadius="15px"
            mt={{ base: "40px", md: "14vh" }}
            mx={{ base: "auto", lg: "unset" }}
            me="auto"
            mb={{ base: "20px", md: "auto" }}
          >
            {/* Bouton Google *//*}
            <Button
              fontSize="sm"
              me="0px"
              mb="26px"
              py="15px"
              h="50px"
              borderRadius="16px"
              bg={googleBg}
              color={googleText}
              fontWeight="500"
              _hover={googleHover}
              _active={googleActive}
              _focus={googleActive}
            >
              <Icon as={FcGoogle} w="20px" h="20px" me="10px" />
              Sign in with Google
            </Button>

            <Flex align="center" mb="25px">
              <Separator />
              <Text color="gray.400" mx="14px">
                or
              </Text>
              <Separator />
            </Flex>

            <Fieldset.Content>
              <Stack gap="4" align="flex-start" maxW="sm">
                {/* Champ email *//*}
                <ChakraField.Root invalid={!!errors.username}>
                  <ChakraField.Label
                    ms="4px"
                    fontSize="sm"
                    fontWeight="500"
                    color={textColor}
                    mb="8px"
                  >
                    Email
                  </ChakraField.Label>
                  <InputGroup startElement={<LuMail />}>
                    <Input
                      id="username"
                      {...register("username", {
                        required: "Email requis",
                        pattern: emailPattern,
                      })}
                      isRequired={true}
                      variant="auth"
                      fontSize="sm"
                      type="email"
                      placeholder="mail@simmmple.com"
                      mb="24px"
                      fontWeight="500"
                      size="lg"
                      borderRadius="16px"
                    />
                  </InputGroup>
                  <ChakraField.ErrorText>
                    {errors.username?.message}
                  </ChakraField.ErrorText>
                </ChakraField.Root>

                {/* Champ password *//*}
                <ChakraField.Root invalid={!!errors.password}>
                  <ChakraField.Label
                    ms="4px"
                    fontSize="sm"
                    fontWeight="500"
                    color={textColor}
                  >
                    Password
                  </ChakraField.Label>
                  <Stack>
                    <InputGroup startElement={<LuLock />}>
                      <PasswordInput
                        visible={visible}
                        onVisibleChange={setVisible}
                        variant="auth"
                        borderRadius="16px"
                        isRequired={true}
                        fontSize="sm"
                        placeholder="Min. 8 characters"
                        mb="24px"
                        {...register("password", passwordRules())}
                      />
                    </InputGroup>
                    <PasswordStrengthMeter value={6} />
                  </Stack>
                  <ChakraField.ErrorText>
                    {errors.password?.message}
                  </ChakraField.ErrorText>
                </ChakraField.Root>
              </Stack>
            </Fieldset.Content>

            {/* Options *//*}
            <Flex justifyContent="space-between" align="center" mb="24px">
              <ChakraField.Root display="flex" alignItems="center">
                <Checkbox
                  id="remember-login"
                  colorScheme="brandScheme"
                  me="10px"
                />
                <ChakraField.Label
                  htmlFor="remember-login"
                  mb="0"
                  fontWeight="normal"
                  color={textColor}
                  fontSize="sm"
                >
                  Keep me logged in
                </ChakraField.Label>
              </ChakraField.Root>

              <Link to="/recover-password" className="main_link">
                <Text
                  color={textColorBrand}
                  fontSize="sm"
                  w="124px"
                  fontWeight="500"
                >
                  Forgot password?
                </Text>
              </Link>
            </Flex>

            {/* Bouton submit *//*}
            <Button
              fontSize="sm"
              fontWeight="500"
              w="100%"
              h="50"
              mb="24px"
              type="submit"
              isLoading={isSubmitting}
              variant="brand"
            >
              Sign In
            </Button>
          </Fieldset.Root>
        </form>

        {/* Footer *//*}
        <Flex
          flexDirection="column"
          justifyContent="center"
          alignItems="start"
          maxW="100%"
          mt="0px"
        >
          <Text color={textColorDetails} fontWeight="400" fontSize="14px">
            Not registered yet?
            <Link to="/auth/sign-up">
              <Text color={textColorBrand} as="span" ms="5px" fontWeight="500">
                Create an Account
              </Text>
            </Link>
          </Text>
        </Flex>
      </Flex>
    </Flex>
  )
}*/

import { PiGoogleLogoDuotone as GoogleIcon, PiXLogoDuotone as XIcon } from 'react-icons/pi';

import { Anchor, Button, Divider, Group, Stack, Text, Title } from '@mantine/core';


import { LoginForm } from './login';
import { Page } from '@components/page';
import { UnderlineShape } from '@components/underline-shape';
import { Link } from '@tanstack/react-router';

export default function LoginPage() {
  return (
    <Page title="Login">
      <Stack gap="xl">
        <Stack>
          <Title order={2}>
            Tongasoa!{' '}
            <Text fz="inherit" fw="inherit" component="span" pos="relative">
              Sign in
              <UnderlineShape
                c="blue"
                left="0"
                pos="absolute"
                h="0.625rem"
                bottom="-1rem"
                w="7rem"
              />
            </Text>{' '}
            to continue.
          </Title>
          <Text fz="sm" c="dimmed">
            Mangataka anao hampiditra ny mombamomba anao. 
            Angataho amin'ny tompon'andraikitry ny toerana fiasanao izany raha tsy mbola anananao.
          </Text>
        </Stack>

        <Group grow>
          <Button leftSection={<XIcon size="1rem" />} variant="outline" color="gray">
            Login with X
          </Button>
          <Button leftSection={<GoogleIcon size="1rem" />} variant="outline" color="gray">
            Login with Google
          </Button>
        </Group>

        <Divider label="OR" labelPosition="center" />

        <LoginForm />

        <Text fz="sm" c="dimmed">
          Don&apos;t have an account?{' '}
          <Anchor fz="inherit" component={Link} to={"auth/sign-up"}>
            Register
          </Anchor>
        </Text>
      </Stack>
    </Page>
  );
}
