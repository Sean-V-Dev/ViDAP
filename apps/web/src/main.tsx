import { createRoot } from "react-dom/client";
import { createSliceClient } from "./editor/api";
import { Editor } from "./editor/Editor";

createRoot(document.getElementById("root")!).render(
  <Editor client={createSliceClient()} />,
);
