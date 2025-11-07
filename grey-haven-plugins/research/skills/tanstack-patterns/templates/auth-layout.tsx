// Grey Haven Studio - Protected Route Layout Template
// Copy this template for _authenticated/_layout.tsx

import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";
import { Header } from "~/lib/components/layout/Header";
import { Sidebar } from "~/lib/components/layout/Sidebar";
import { getSession } from "~/lib/server/functions/auth";

// TODO: Update route path to match your file location
export const Route = createFileRoute("/_authenticated/_layout")({
  // Auth check runs before loading
  beforeLoad: async ({ context }) => {
    const session = await getSession();

    // Redirect to login if not authenticated
    if (!session) {
      throw redirect({
        to: "/auth/login",
        search: {
          redirect: context.location.href, // Save redirect URL
        },
      });
    }

    // Make session available to child routes
    return { session };
  },
  component: AuthenticatedLayout,
});

function AuthenticatedLayout() {
  const { session } = Route.useRouteContext();

  return (
    <div className="flex min-h-screen">
      {/* TODO: Update layout structure */}
      <Sidebar user={session.user} />
      <div className="flex-1">
        <Header user={session.user} />
        <main className="p-6">
          <Outlet /> {/* Child routes render here */}
        </main>
      </div>
    </div>
  );
}
