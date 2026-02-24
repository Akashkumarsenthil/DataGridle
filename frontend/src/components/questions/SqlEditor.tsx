"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import Button from "@/components/ui/Button";
import { Play, RotateCcw } from "lucide-react";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), {
  ssr: false,
  loading: () => (
    <div className="flex h-full items-center justify-center text-xs text-gray-500">
      Loading SQL editor...
    </div>
  ),
});

interface SqlEditorProps {
  starterCode?: string;
  onSubmit?: (code: string) => void;
}

export default function SqlEditor({
  starterCode = "-- Write your SQL query here\nSELECT ",
  onSubmit,
}: SqlEditorProps) {
  const [code, setCode] = useState(starterCode);
  const [output, setOutput] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  const handleRun = async () => {
    setIsRunning(true);
    setOutput(null);
    try {
      // DuckDB-WASM execution will be integrated here
      // For now, just record the submission
      onSubmit?.(code);
      setOutput("Query submitted. DuckDB-WASM sandbox will evaluate this in-browser.");
    } catch (err) {
      setOutput(`Error: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setIsRunning(false);
    }
  };

  const handleReset = () => {
    setCode(starterCode);
    setOutput(null);
  };

  return (
    <div className="flex h-full min-h-[360px] flex-col overflow-hidden rounded-xl border border-gray-800">
      <div className="flex items-center justify-between border-b border-gray-800 bg-gray-900/80 px-4 py-2">
        <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">SQL Editor</span>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={handleReset}>
            <RotateCcw className="h-3.5 w-3.5" />
            Reset
          </Button>
          <Button size="sm" onClick={handleRun} disabled={isRunning}>
            <Play className="h-3.5 w-3.5" />
            {isRunning ? "Running..." : "Run"}
          </Button>
        </div>
      </div>
      <div className="flex-1 bg-[#1e1e1e]">
        {isClient ? (
          <MonacoEditor
            height="100%"
            language="sql"
            theme="vs-dark"
            value={code}
            onChange={(v) => setCode(v || "")}
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
              scrollBeyondLastLine: false,
              wordWrap: "on",
              padding: { top: 16 },
              lineNumbers: "on",
              renderLineHighlight: "line",
            }}
          />
        ) : (
          <textarea
            className="h-full w-full resize-none bg-[#1e1e1e] p-4 font-mono text-sm text-gray-100 outline-none"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            spellCheck={false}
          />
        )}
      </div>
      {output && (
        <div className="border-t border-gray-800 bg-gray-950 p-4">
          <h4 className="mb-2 text-xs font-medium text-gray-400 uppercase tracking-wider">Output</h4>
          <pre className="overflow-auto rounded-lg bg-black/50 p-3 font-mono text-sm text-green-400">
            {output}
          </pre>
        </div>
      )}
    </div>
  );
}
