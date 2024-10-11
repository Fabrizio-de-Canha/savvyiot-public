import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Maximize2 } from "lucide-react";
import { device } from "@/pages/Devices";
import { useState } from "react";
import { WifiStrength } from "./wifiStrength";
import axios from "axios";
import {
  Bar,
  BarChart,
  CartesianGrid,
  LabelList,
  XAxis,
  YAxis,
} from "recharts";
import { ChartConfig, ChartContainer } from "@/components/ui/chart";

interface MachineProps {
  callback?: void;
  device: device;
}

interface DeviceDetails {
  value: number;
  message_timestamp: Date;
  rounded_value: number;
}

const chartConfig = {
  desktop: {
    label: "Desktop",
    color: "hsl(var(--primary))",
  },
  mobile: {
    label: "Mobile",
    color: "#60a5fa",
  },
} satisfies ChartConfig;

export function MachineDialog(props: MachineProps) {
  const [data, setData] = useState<DeviceDetails[]>([] as DeviceDetails[]);
  const [maxVal, setMaxVal] = useState<number>();

  const fetchData = async () => {
    try {
      axios
        .post(
          "http://localhost:8000/devices/deviceData",
          {
            device_mac: props.device.mac_id,
            value_type: "cycle_time_1",
            limit: 10,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token_local")}`,
            },
          }
        )
        .then(function (response) {
          if (response.data) {
            const updatedData: DeviceDetails[] = response.data.map(
              (data: DeviceDetails) => ({
                ...data,
                rounded_value: (data.value / 1000).toFixed(2),
              })
            );

            setMaxVal(Math.max(...updatedData.map((d) => d.rounded_value)));
            setData(updatedData);
          }
        });
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <Dialog onOpenChange={(isOpen) => isOpen && fetchData()}>
      <DialogTrigger asChild>
        <Maximize2 className="p-1 opacity-50 hover:cursor-pointer" />
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px] flex flex-col lg:max-w-[50%] lg:max-h-[60%]">
        <DialogHeader>
          <DialogTitle className="flex flex-row items-center gap-2 ">
            <WifiStrength rssi={props.device.rssi} />
            {props.device.name}
            <p className="font-normal opacity-50">{props.device.mac_id}</p>
          </DialogTitle>
        </DialogHeader>
        <ChartContainer config={chartConfig} className="my-8">
          <BarChart
            accessibilityLayer
            data={data}
            margin={{ top: 10, right: 10 }}
          >
            <CartesianGrid vertical={false} />
            <YAxis
              domain={[0, maxVal!]}
              padding={{ top: 30 }}
              axisLine={false}
              tick={false}
              label={{
                value: "Cycle time [s]", // Replace with your label
                angle: -90, // Rotates the label to be vertical
                position: "insideLeft",
                style: {
                  textAnchor: "middle",
                  fill: "var(--color-foreground)",
                }, // Adjust styles as needed
              }}
            />
            <Bar
              dataKey="rounded_value"
              fill="var(--color-desktop)"
              radius={4}
              className="py-4"
            >
              <LabelList
                position="top"
                offset={12}
                className="fill-foreground"
                fontSize={12}
              />
            </Bar>
          </BarChart>
        </ChartContainer>
        <div className="flex flex-col">
          <div className=" flex w-full">
            <h2 className="mr-auto font-bold">Last Booted:</h2>
            <p>
              {props.device.last_booted
                ? new Date(props.device.last_booted! + "Z").toLocaleString()
                : "Not recorded"}
            </p>
          </div>
          <div className=" flex w-full">
            <h2 className="mr-auto font-bold">Last Cycle:</h2>
            <p>
              {data[0]
                ? new Date(data[0].message_timestamp! + "Z").toLocaleString()
                : "Not recorded"}
            </p>
          </div>
          <div className=" flex w-full">
            <h2 className="mr-auto font-bold">Last Reported:</h2>
            <p>
              {props.device.last_reported
                ? new Date(props.device.last_reported! + "Z").toLocaleString()
                : "Not recorded"}
            </p>
          </div>
        </div>

        <DialogFooter></DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
