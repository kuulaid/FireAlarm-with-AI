import { ChipStatus } from "../types";
import { getChipClass } from "../utils/theme";

interface ChipProps {
  status: ChipStatus;
}

// Small badge that renders a status label with the correct color palette.
export function Chip({ status }: ChipProps) {
  return (
    <span className={`text-[10px] font-bold tracking-wider uppercase px-2 py-0.5 rounded-md whitespace-nowrap ${getChipClass(status)}`}>
      {status}
    </span>
  );
}
