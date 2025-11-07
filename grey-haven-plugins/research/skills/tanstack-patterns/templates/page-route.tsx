// Grey Haven Studio - Page Route Template
// Copy this template for any page route

import { createFileRoute } from "@tanstack/react-router";
// TODO: Import your server functions
// import { getPageData } from "~/lib/server/functions/page";

// TODO: Update route path to match your file location
export const Route = createFileRoute("/_authenticated/page")({
  // Loader fetches data on server before rendering
  loader: async ({ context }) => {
    const tenantId = context.session.tenantId;
    // TODO: Replace with your data fetching
    // return await getPageData(tenantId);
    return { data: "Replace me" };
  },
  component: PageComponent,
});

function PageComponent() {
  const data = Route.useLoaderData(); // Type-safe loader data

  return (
    <div>
      {/* TODO: Build your page UI */}
      <h1 className="text-2xl font-bold">Page Title</h1>
      <div>{JSON.stringify(data)}</div>
    </div>
  );
}
