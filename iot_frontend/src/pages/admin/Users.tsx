import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import axios from "axios";
import { useEffect, useState } from "react";
import { CreateUserDialog } from "@/components/custom/createUser";
import { Trash2, UserRoundPen } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface user {
  id: string;
  verified?: boolean;
  active?: boolean;
  admin?: boolean;
  super_user?: boolean;
  email: string;
  name?: string;
  surname?: string;
  last_login?: Date | null;
  created_on?: Date | null;
}

const apiUrl = import.meta.env.VITE_APP_API_URL;

export function Users() {
  const [users, setUsers] = useState<user[]>([] as user[]);

  useEffect(() => {
    axios
      .get(`${apiUrl}/user`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token_local")}`,
        },
      })
      .then(function (response) {
        if (response.data) {
          setUsers(response.data);
        }
      })
      .catch(function (error) {
        console.log(error, "error");
      });
  }, []);

  return (
    <>
      <div className="flex items-center">
        <h1 className="text-lg font-semibold md:text-2xl mr-auto">Users</h1>
        <CreateUserDialog />
      </div>
      <div className="flex flex-1 rounded-lg border shadow-sm">
        <div className="flex flex-col items-center gap-1 text-center w-full">
          <Table>
            <TableCaption>users</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead className="border-r">Email</TableHead>
                <TableHead className="border-r">Name</TableHead>
                <TableHead className="border-r">Surname</TableHead>
                <TableHead className="border-r">Created</TableHead>
                <TableHead className="border-r">Last Logged In</TableHead>
                <TableHead className="border-r">Tags</TableHead>
                <TableHead className="">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {users?.map((user) => (
                <TableRow className="text-left">
                  <TableCell className="font-medium">{user.email}</TableCell>
                  <TableCell>{user.name}</TableCell>
                  <TableCell>{user.surname}</TableCell>
                  <TableCell>
                    {user.created_on
                      ? new Date(user.created_on!).toLocaleDateString()
                      : ""}
                  </TableCell>
                  <TableCell>
                    {user.last_login
                      ? new Date(user.last_login!).toLocaleDateString()
                      : ""}
                  </TableCell>
                  <TableCell>
                        {user.admin && <Badge className="mr-2">Admin</Badge>}
                        {user.super_user && <Badge variant="secondary">Superuser</Badge>}
                  </TableCell>
                  <TableCell className="flex p-0 px-4 gap-2">
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Trash2 className="cursor-pointer my-4 h-8 w-8 p-1 hover:bg-red-200 hover:text-red-600 rounded" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Delete user</p>
                        </TooltipContent>
                      </Tooltip>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <UserRoundPen className="cursor-pointer my-4 h-8 w-8 p-1 hover:bg-blue-200 hover:text-blue-600 rounded" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Edit user</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </>
  );
}
