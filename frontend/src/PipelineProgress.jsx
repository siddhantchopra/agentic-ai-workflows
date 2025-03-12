import { useState } from "react";
import clsx from "clsx";
import MarkdownRenderer from "./ContentArea";

const ProgressStepper = ({ progress }) => {
  const [expandedStep, setExpandedStep] = useState(null);

  return (
    <div className="p-4 bg-white border rounded-md shadow-sm relative">
      <h3 className="font-semibold text-lg mb-4">Progress:</h3>
      <div className="flex items-center justify-center space-x-6 relative">
        {progress.map((msg, index) => {
          const isCompleted = index < progress.length - 1;
          const isCurrent = index === progress.length - 1;
          const title =
            msg.content.length > 30
              ? msg.content.substring(0, 30) + "..."
              : msg.content;

          return (
            <div key={index} className="flex items-center relative">
              {/* Step Circle */}
              <div className="flex flex-col items-center relative">
                <div
                  className={clsx(
                    "w-12 h-12 flex items-center justify-center rounded-full border-2 font-bold transition-all duration-300 cursor-pointer",
                    isCompleted ? "bg-blue-500 text-white border-blue-500" : "",
                    isCurrent
                      ? "border-4 border-blue-500 text-blue-500"
                      : "border-gray-300"
                  )}
                  onClick={() =>
                    setExpandedStep(expandedStep === index ? null : index)
                  }
                >
                  {isCompleted ? "✔" : index + 1}
                </div>

                {/* Step Title */}
                <div
                  className="text-xs mt-2 text-center w-24 cursor-pointer"
                  onClick={() => setExpandedStep(index)}
                >
                  {title}
                </div>

                {/* Expanded Content (Fix Positioning) */}
                {expandedStep === index && (
                  <div
                    className="absolute top-full mt-2 left-1/2 transform -translate-x-1/2 
             w-64 p-3 text-sm text-gray-700 border rounded bg-gray-100 shadow-md z-10"
                  >
                    <MarkdownRenderer content={msg.content} />
                  </div>
                )}
              </div>

              {/* Progress Arrow (Only if not the last step) */}
              {index < progress.length - 1 && (
                <div className="flex items-center">
                  {/* Horizontal Progress Line */}
                  <div
                    className={clsx(
                      "w-12 h-1",
                      isCompleted ? "bg-blue-500" : "bg-gray-300"
                    )}
                  />

                  {/* Triangle Arrow (Properly Centered & Filled) */}
                  <div
                    className={clsx(
                      "w-3 h-3 rotate-45 -ml-1",
                      isCompleted ? "bg-blue-500" : "bg-gray-300"
                    )}
                  />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ProgressStepper;
