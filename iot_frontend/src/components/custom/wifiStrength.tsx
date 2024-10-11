import { Wifi, WifiHigh, WifiLow, WifiOff } from "lucide-react";

interface WifiStrengthProps {
  rssi?: number;
}

export function WifiStrength(props: WifiStrengthProps) {
  if (props.rssi! < -70) {
    return <WifiLow className="text-red-500"/>;
  } else if (props.rssi! < -70) {
  }

  if (props.rssi! < -55) {
    return <WifiHigh className="text-yellow-600"/>;
  }

  if (props.rssi! < -20) {
    return <Wifi className="text-green-600"/>;
  }

  return <WifiOff />;
}
