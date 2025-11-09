// Grey Haven Studio - Custom Query Hook Template
// Copy this template for reusable query logic

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
// TODO: Import your server functions
// import { getResource, updateResource } from "~/lib/server/functions/resources";

// TODO: Update hook name and parameter types
export function useResource(resourceId: string, tenantId: string) {
  const queryClient = useQueryClient();

  // Query for fetching data
  const query = useQuery({
    queryKey: ["resource", resourceId], // Include resourceId in key
    queryFn: () => getResource(resourceId, tenantId),
    staleTime: 60000, // Grey Haven default: 1 minute
  });

  // Mutation for updating data
  const updateMutation = useMutation({
    mutationFn: (data: ResourceUpdate) => updateResource(resourceId, data, tenantId),
    onSuccess: (updatedResource) => {
      // Update cache with new data
      queryClient.setQueryData(["resource", resourceId], updatedResource);
    },
  });

  // Return simplified interface
  return {
    resource: query.data,
    isLoading: query.isLoading,
    error: query.error,
    update: updateMutation.mutate,
    isUpdating: updateMutation.isPending,
  };
}

// Usage in component:
// const { resource, isLoading, update, isUpdating } = useResource(id, tenantId);
