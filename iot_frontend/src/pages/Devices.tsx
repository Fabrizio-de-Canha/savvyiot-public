"use client";

import axios from "axios";
import { useEffect, useRef, useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { WifiStrength } from "@/components/custom/wifiStrength";
import { Maximize2 } from "lucide-react";
import moment from "moment";
import { MachineDialog } from "@/components/custom/MachineDialog";
import { Pie, PieChart } from "recharts";

import {
  ChartConfig,
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

export interface device {
  mac_id: string;
  active?: boolean;
  name?: string;
  created_on?: Date | null;
  last_reported?: Date | null;
  last_booted?: Date | null;
  rssi?: number;
  firmware_version?: number;
  time_difference?: string;
  minute_difference?: number;
  isUpdated?: boolean; // New field to track if device has been updated
}

enum deviceHealthCategories {
  healthy = "healthy",
  idle = "idle",
  non_reporter = "non_reporter",
  non_reporter_day = "non_reporter_day",
}

interface deviceHealth {
  description: deviceHealthCategories;
  count: number;
  fill?: string;
}

const chartConfig = {
  count: {
    label: "Count",
  },
  healthy: {
    label: "Healthy",
    color: "hsl(var(--chart-1))",
  },
  idle: {
    label: "Idle",
    color: "hsl(var(--chart-2))",
  },
  non_reporter: {
    label: "Non-Reporter <24h",
    color: "hsl(var(--chart-3))",
  },
  non_reporter_day: {
    label: "Non-Reporter >24h",
    color: "hsl(var(--chart-4))",
  },
} satisfies ChartConfig;

export function Devices() {
  const [devices, setDevices] = useState<device[]>([] as device[]);
  const [healthSummary, setHealthSummary] = useState<deviceHealth[]>(
    [] as deviceHealth[]
  );

  const devicesRef = useRef(devices); 

  useEffect(() => {
    axios
      .get("http://localhost:8000/devices", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token_local")}`,
        },
      })
      .then(function (response) {
        if (response.data) {
          const updatedDevices: device[] = response.data.map(
            (device: device) => ({
              ...device,
              time_difference: device.last_reported
                ? getTimeDifference(device.last_reported)
                : "Never",
              minute_difference: device.last_reported
                ? getTimeDifferenceMinutes(device.last_reported)
                : -1,
            })
          );

          setDevices(
            updatedDevices.sort(function (a: device, b: device) {
              if (a.name! < b.name!) {
                return -1;
              }
              if (a.name! > b.name!) {
                return 1;
              }
              return 0;
            })
          );

          updateHealthSummary(updatedDevices);
        }
      })
      .catch(function (error) {
        console.log(error, "error");
      });

    const ws = new WebSocket(
      `ws://localhost:8000/updates/ws?token=${localStorage.getItem(
        "token_local"
      )}`
    );

    ws.onmessage = (event) => {
      const newDeviceData = JSON.parse(event.data) as device;
      const { last_reported } = newDeviceData;

      if (last_reported) {
        newDeviceData.time_difference = getTimeDifference(last_reported);
        newDeviceData.minute_difference =
          getTimeDifferenceMinutes(last_reported);
      }

      newDeviceData.isUpdated = true;

      // Update devices state with new data, replacing the device if it exists or adding it if new
      setDevices((prevDevices) => {
        const existingDeviceIndex = prevDevices.findIndex(
          (device) => device.mac_id === newDeviceData.mac_id
        );

        if (existingDeviceIndex !== -1) {
          // Replace existing device
          const updatedDevices = [...prevDevices];
          updatedDevices[existingDeviceIndex] = newDeviceData;
          return updatedDevices;
        } else {
          // Add new device
          return [...prevDevices, newDeviceData];
        }
      });

      // Remove the update flag after 1 second
      setTimeout(() => {
        setDevices((prevDevices) =>
          prevDevices.map((device) =>
            device.mac_id === newDeviceData.mac_id
              ? { ...device, isUpdated: false }
              : device
          )
        );
      }, 1000);
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };
  }, []);

  // Live time updating logic
  useEffect(() => {

    const intervalId = setInterval(() => {
      setDevices((prevDevices) =>
        prevDevices.map((device) => {
          if (device.last_reported) {
            const timeString = getTimeDifference(device.last_reported);
            const minuteDifference = getTimeDifferenceMinutes(
              device.last_reported
            );

            return {
              ...device,
              time_difference: timeString,
              minute_difference: minuteDifference,
            };
          }
          return device;
        })
      );
    }, 1000); // Update every 1 seconds (1 minute)

    return () => clearInterval(intervalId); // Cleanup interval on component unmount
  }, []);

  function getTimeDifference(date: Date) {
    var now = moment(new Date().toISOString());
    var end = moment(date + "Z");
    var duration = moment.duration(now.diff(end));

    if (duration.asDays() > 1) {
      return duration.asDays().toFixed() + " Days ago";
    }

    if (duration.asHours() > 1) {
      return duration.asHours().toFixed() + " Hours ago";
    }

    if (duration.asMinutes() > 1) {
      return duration.asMinutes().toFixed() + " Minutes ago";
    }

    if (duration.asSeconds() > 1) {
      return duration.asSeconds().toFixed() + " Seconds ago";
    }
  }

  function getTimeDifferenceMinutes(date: Date) {
    var now = moment(new Date().toISOString());
    var end = moment(date + "Z");
    var duration = moment.duration(now.diff(end));

    return duration.asMinutes();
  }

  // Function to update health summary
  const updateHealthSummary = (devices: device[]) => {
    const healthyCount = devices.filter(
      (d) => d.minute_difference !== undefined && d.minute_difference < 35
    ).length;
    const idleCount = devices.filter(
      (d) =>
        d.minute_difference !== undefined &&
        d.minute_difference >= 35 &&
        d.minute_difference < 240
    ).length;
    const nonReporterCount = devices.filter(
      (d) =>
        d.minute_difference !== undefined &&
        d.minute_difference >= 240 &&
        d.minute_difference < 1440
    ).length;
    const nonReporterDayCount = devices.filter(
      (d) => d.minute_difference !== undefined && d.minute_difference >= 1440
    ).length;

    const summary: deviceHealth[] = [
      {
        description: deviceHealthCategories.healthy,
        count: healthyCount,
        fill: "rgb(134 239 172)",
      },
      {
        description: deviceHealthCategories.idle,
        count: idleCount,
        fill: "rgb(254 249 195)",
      },
      {
        description: deviceHealthCategories.non_reporter,
        count: nonReporterCount,
        fill: "rgb(254 226 226)",
      },
      {
        description: deviceHealthCategories.non_reporter_day,
        count: nonReporterDayCount,
        fill: "rgb(252 165 165)",
      },
    ];
    
    const filteredSummary = summary.filter((item) => item.count > 0);

    setHealthSummary(filteredSummary);
  };

  useEffect(() => {
    
    // Set interval to update healthSummary every 2 minutes (120,000 ms)
    const intervalId = setInterval(() => {
      updateHealthSummary(devicesRef.current);
    }, 5000); // 2 minutes in milliseconds

    // Cleanup the interval when the component is unmounted
    return () => clearInterval(intervalId);
    
  }, []); // Optional: if `devices` changes dynamically, this will still trigger the update

  useEffect(() => {
    devicesRef.current = devices;
  }, [devices]);

  return (
    <div className="flex flex-col h-full gap-4">
      <div className="flex">
        <h1 className="text-lg font-semibold md:text-2xl">Device Summary</h1>
      </div>
      <div className="flex flex-row w-full justify-center">
        <ChartContainer
          config={chartConfig}
          className="min-h-[150px] aspect-auto w-full lg:min-h-[250px]"
        >
          <PieChart>
            <ChartTooltip
              content={<ChartTooltipContent nameKey="description" hideLabel />}
            />
            <Pie
              data={healthSummary}
              dataKey="count"
              labelLine={false}
              label={({ payload, ...props }) => {
                return (
                  <text
                    cx={props.cx}
                    cy={props.cy}
                    x={props.x}
                    y={props.y}
                    textAnchor={props.textAnchor}
                    dominantBaseline={props.dominantBaseline}
                    fill="hsla(var(--foreground))"
                  >
                    {`${
                      chartConfig[
                        payload.description as keyof typeof chartConfig
                      ]?.label
                    } (${payload.count})`}
                  </text>
                );
              }}
              nameKey="description"
            />
          </PieChart>
        </ChartContainer>
      </div>

      <div className="flex items-center">
        <h1 className="text-lg font-semibold md:text-2xl">Devices</h1>
      </div>
      <div className="flex flex-2 rounded-lg shadow-sm overflow-y-auto">
        <div className="grid lg:grid-cols-5 gap-1 min-w-full min-h-full">
          {devices?.map((device) => (
            <Card
              key={device.mac_id}
              className={`${
                device.minute_difference && device.minute_difference > 1440
                  ? "bg-red-300"
                  : device.minute_difference && device.minute_difference > 240
                  ? "bg-red-100"
                  : device.minute_difference && device.minute_difference > 35
                  ? "bg-yellow-100"
                  : "bg-white"
              }
              ${
                device.isUpdated
                  ? "border-green-600 bg-green-300 animate-flash"
                  : "border-gray-300"
              }`}
            >
              <CardHeader>
                <span className="flex gap-2">
                  <WifiStrength rssi={device.rssi} />
                  <CardTitle className="text-xl mr-auto">
                    {device.name}
                  </CardTitle>
                  <MachineDialog device={device} />
                </span>
              </CardHeader>
              <CardContent>
                <span className="flex text-sm gap-2">
                  <p className="text-muted-foreground">Last reported:</p>
                  <p className="">{device.time_difference}</p>
                </span>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
