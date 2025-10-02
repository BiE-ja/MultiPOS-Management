import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute(
  '/dashboard/admin/management/owners-pos-users',
)({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/dashboard/admin/management/owners-pos-users"!</div>
}
