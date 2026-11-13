import { useState } from "react";
import Sidebar from "../components/layout/Sidebar";
import axiosClient from "../api/axiosClient";
import { Send, CheckCircle2, AlertCircle } from "lucide-react";

export default function DashboardPage() {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [reason, setReason] = useState("");
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const handleLeaveSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setFeedback(null);

    try {
      await axiosClient.post("/leave/", {
        start_date: startDate,
        end_date: endDate,
        reason: reason,
        leave_paper_image_url: null,
      });
      setFeedback({
        type: "success",
        text: "Leave request submitted successfully and sent to director!",
      });
      setStartDate("");
      setEndDate("");
      setReason("");
    } catch (err) {
      setFeedback({
        type: "error",
        text: err.response?.data?.detail || "Failed to submit leave request.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-darkBg text-white font-sans overflow-hidden">
      {/* Sidebar Navigation */}
      <Sidebar />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col items-center justify-center px-6 relative">
        <div className="max-w-2xl w-full text-center space-y-6">
          <h1 className="text-4xl font-bold tracking-tight text-white">
            Attendance & Leave Made Easy
          </h1>
          <p className="text-gray-400 text-sm max-w-md mx-auto">
            Submit your leave details below. Requests are routed directly to the
            school director for review.
          </p>

          {feedback && (
            <div
              className={`p-4 rounded-xl flex items-center gap-3 text-sm ${
                feedback.type === "success"
                  ? "bg-emerald-500/10 border border-emerald-500/20 text-emerald-400"
                  : "bg-red-500/10 border border-red-500/20 text-red-400"
              }`}
            >
              {feedback.type === "success" ? (
                <CheckCircle2 size={18} />
              ) : (
                <AlertCircle size={18} />
              )}
              <span>{feedback.text}</span>
            </div>
          )}

          {/* Leave Submission Card */}
          <form
            onSubmit={handleLeaveSubmit}
            className="bg-sidebar border border-gray-800/80 p-6 rounded-2xl shadow-2xl space-y-4 text-left"
          >
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-gray-400">
                  Start Date
                </label>
                <input
                  type="date"
                  required
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full bg-card border border-gray-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-accentBlue"
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-gray-400">
                  End Date
                </label>
                <input
                  type="date"
                  required
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="w-full bg-card border border-gray-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-accentBlue"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium text-gray-400">
                Reason for Leave
              </label>
              <textarea
                required
                rows="3"
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                placeholder="Describe your reason..."
                className="w-full bg-card border border-gray-800 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-accentBlue resize-none"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-accentBlue hover:bg-blue-700 text-white font-semibold rounded-lg shadow-lg shadow-blue-600/30 transition flex items-center justify-center gap-2 text-sm"
            >
              <Send size={16} />
              {loading ? "SUBMITTING..." : "SUBMIT LEAVE REQUEST"}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
