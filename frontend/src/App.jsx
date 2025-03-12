import React, { useState } from "react";
import ProgressStepper from "./PipelineProgress";

const App = () => {
  const [topic, setTopic] = useState("");
  const [userDetails, setUserDetails] = useState("");
  const [progress, setProgress] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [buffer, setBuffer] = useState(""); // Holds merged chunks

  const handleGenerateBlog = async () => {
    if (!topic.trim() || !userDetails.trim()) return alert("All fields are required!");

    setProgress([]);
    setIsGenerating(true);
    setBuffer(""); // Reset buffer

    const eventSource = new EventSource(
      `http://127.0.0.1:8000/stream?topic=${encodeURIComponent(topic)}&user_details=${encodeURIComponent(userDetails)}`
    );

    eventSource.onmessage = (event) => {
      let formattedOutput = event.data.replace(/<br\s*\/?>/g, "\n"); // Convert <br> to new lines
    
      setProgress((prevOutput) => {
        let updatedProgress = [...prevOutput];
    
        // ✅ Always find the existing "Final Workflow" step
        let existingStepIndex = updatedProgress.findIndex((step) => step.step === "Final Workflow");
    
        if (formattedOutput.includes("Running final crew workflow")) {
          if (existingStepIndex === -1) {
            // ✅ Create "Final Workflow" step only once
            updatedProgress.push({ step: "Final Workflow", content: formattedOutput });
          }
        } else if (existingStepIndex !== -1) {
          // ✅ Append all further messages to "Final Workflow"
          updatedProgress[existingStepIndex].content += "\n" + formattedOutput;
        } else {
          // ✅ Handle other steps normally
          let stepNumber = updatedProgress.length + 1;
          updatedProgress.push({ step: `Step ${stepNumber}`, content: formattedOutput });
        }
    
        if (event.data.includes("✅ Blog Generation Complete!")) {
          eventSource.close();
          setIsGenerating(false);
        }
    
        return updatedProgress;
      });
    };
    
    

    eventSource.onerror = (error) => {
      console.error("SSE Error:", error);
      eventSource.close();
      setIsGenerating(false);
    };
  };

  return (
    <>
   <div className="flex items-center justify-center m-6">
   <h1 className="text-[30px] font-[600]">Agentic Workflows : Crew AI </h1>
    </div>
    <div className="max-w-[50rem] mx-auto mt-10 p-6 bg-gray-100 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Generate a Blog</h2>

      <input
        type="text"
        placeholder="Enter Blog Topic"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        className="w-full p-2 border border-gray-300 rounded-md mb-2"
      />

      <textarea
        placeholder="Enter User Details"
        value={userDetails}
        onChange={(e) => setUserDetails(e.target.value)}
        className="w-full p-2 border border-gray-300 rounded-md mb-2"
      />

      <button
        onClick={handleGenerateBlog}
        disabled={isGenerating}
        className={`w-full p-2 text-white font-semibold rounded-md ${
          isGenerating ? "bg-gray-500 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"
        }`}
      >
        {isGenerating ? "Generating..." : "Generate Blog"}
      </button>
    </div>
    <div className="mt-10 mx-8 bg-white rounded-md shadow-sm">
        <ProgressStepper progress={progress} />
      </div>
    </>
  );
};

export default App;


