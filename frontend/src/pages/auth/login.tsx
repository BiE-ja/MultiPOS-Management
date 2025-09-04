import {
  Anchor,
  Button,
  Checkbox,
  Group,
  PasswordInput,
  Stack,

  TextInput,
  type StackProps,
} from '@mantine/core';
import { isEmail, useForm } from '@mantine/form';



import {
  Link,
} from "@tanstack/react-router"

import type { BodyAuthLogin as AccessToken } from "@client/schemas"
import useAuth from "hooks/useAuth"

import { IconLock, IconUser } from '@tabler/icons-react';
import { FormProvider } from '@components/forms/form-provider';
import { handleFormErrors } from 'utilities/form';



interface LoginFormProps extends Omit<StackProps, 'children'> {
  onSuccess?: () => void;
}

export function LoginForm({ ...props }: LoginFormProps) {
  const { loginMutation,isPending, resetError } = useAuth();
  const form = useForm<AccessToken>({
      mode: 'uncontrolled',
      //initialValues: { username: 'john.doe@example.com', password: '123456789', remember: false },
      validate:  {
            username: isEmail('Invalid email'),
            password:(value) =>
              value.length < 6 ? 'Password must include at least 6 characters' : null,
          },
    });

  const handleSubmit = form.onSubmit(async (data: AccessToken) => {
    //if (isSubmitting) return
    resetError()
    try {
      await loginMutation(data)
      
    } catch (error) {
      handleFormErrors(form,error);
      // handled in useAuth
    }
  })



  return (
    <FormProvider form={form} onSubmit={handleSubmit}>
      <Stack {...props}>
        <TextInput 
          name="email" 
          label="Email" 
          required 
          placeholder ="tantana@zita.com" 
          leftSection={<IconUser size={16}/>} 
          {...form.getInputProps('username')}/>

        <PasswordInput 
          name="password" 
          label="Password" 
          required 
          leftSection={<IconLock size={16}/>} 
          {...form.getInputProps('password')}/>
          
        <Group justify="space-between">
          <Checkbox name="remember" label="Remember me" />
          <Anchor size="sm" component={Link} to={"/auth/forgot-password"}>
            Forgot password?
          </Anchor>
        </Group>
        <Button type="submit" loading={isPending}>
          Login
        </Button>
      </Stack>
    </FormProvider>
  );
}
