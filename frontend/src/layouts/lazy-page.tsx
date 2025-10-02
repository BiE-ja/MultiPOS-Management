import { LoadingScreen } from '@components/loading-screen';
import { type ComponentType, type ElementType, Suspense, lazy } from 'react';


const Loadable = (Component: ElementType) => (props: any) => (
  <Suspense fallback={<LoadingScreen />}>
    <Component {...props} />
  </Suspense>
);

export function LazyPage(callback: () => Promise<{ default: ComponentType<any> }>) {
  const Component = Loadable(lazy(callback));
  return <Component />;
}
