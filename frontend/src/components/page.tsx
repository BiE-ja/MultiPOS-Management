import { forwardRef, type ReactNode, useEffect } from 'react';

import { Box, type BoxProps } from '@mantine/core';
import { nprogress } from '@mantine/nprogress';


interface PageProps extends BoxProps {
  children: ReactNode;
  meta?: ReactNode;
  title: string;
}
export const Page = forwardRef<HTMLDivElement, PageProps>(
  ({ children, title = '', meta, ...other }, ref) => {
    useEffect(() => {
      nprogress.complete();
      return () => nprogress.start();
    }, []);

    return (
      <>
        
          <title>{`${title} - Tantana Boutik' - `}</title>
          {meta}
        

        <Box ref={ref} {...other}>
          {children}
        </Box>
      </>
    );
  }
);
