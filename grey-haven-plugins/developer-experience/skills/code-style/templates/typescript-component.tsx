// Example React Component Template
// Copy and adapt this for new Grey Haven components

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Button } from "~/lib/components/ui/button";
import { Card } from "~/lib/components/ui/card";
import { queryClient } from "~/lib/query-client";

// 1. Define your types/interfaces
interface MyComponentProps {
  id: string;
  onUpdate?: (data: MyData) => void;
}

interface MyData {
  id: string;
  name: string;
  created_at: Date; // snake_case for database fields
  is_active: boolean;
}

// 2. Component (default export for routes)
export default function MyComponent({ id, onUpdate }: MyComponentProps) {
  // 3. State management
  const [isEditing, setIsEditing] = useState(false);

  // 4. Queries with TanStack Query
  const { data, isLoading, error } = useQuery(
    {
      queryKey: ["myData", id],
      queryFn: async () => {
        // Replace with your API call
        const response = await fetch(`/api/data/${id}`);
        return response.json();
      },
      staleTime: 60000, // 1 minute - Grey Haven default
    },
    queryClient,
  );

  // 5. Event handlers
  const handleSave = async () => {
    // Replace with your save logic
    console.log("Saving...");
    setIsEditing(false);
    onUpdate?.(data);
  };

  // 6. Conditional renders
  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error loading data</div>;
  }

  if (!data) {
    return <div>No data found</div>;
  }

  // 7. Main render
  return (
    <Card className="p-6">
      <h2 className="mb-4 text-2xl font-bold">{data.name}</h2>

      {isEditing ? (
        <div className="space-y-4">
          {/* Edit mode UI */}
          <Button onClick={handleSave}>Save</Button>
          <Button variant="outline" onClick={() => setIsEditing(false)}>
            Cancel
          </Button>
        </div>
      ) : (
        <div className="space-y-2">
          {/* View mode UI */}
          <p>Status: {data.is_active ? "Active" : "Inactive"}</p>
          <Button onClick={() => setIsEditing(true)}>Edit</Button>
        </div>
      )}
    </Card>
  );
}
