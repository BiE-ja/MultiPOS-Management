import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/dashboard/admin/manage-owners')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/dashboard/admin/home"!</div>
}
