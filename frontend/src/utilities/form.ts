import { CustomNotifications } from '@components/customNotification';
import { type UseFormReturnType } from '@mantine/form';
//import { notifications } from '@mantine/notifications';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function handleFormErrors(form: UseFormReturnType<any>, errors: unknown) {
  if (!errors || typeof errors !== 'object') {
    return;
  }

  if ('formErrors' in errors && Array.isArray(errors.formErrors)) {
    errors.formErrors.forEach((error) => {
      CustomNotifications.show({ children: error, color: 'red' });
    });
  }

  if ('fieldErrors' in errors && typeof errors.fieldErrors === 'object' && errors.fieldErrors) {
    Object.entries(errors.fieldErrors).forEach(([fieldName, fieldErrors]) => {
      form.setFieldError(fieldName, fieldErrors.join(','));
    });
  }
}
