import React, { useState, useEffect, useRef } from "react";
import Webcam from "react-webcam";
import axios from "axios";
import "./app.css";

const App = () => {
  const [step, setStep] = useState(0);
  const [userType, setUserType] = useState("");
  const [role, setRole] = useState("");
  const [message, setMessage] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [employeeId, setEmployeeId] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [query, setQuery] = useState("");
  const chatboxRef = useRef(null);

  useEffect(() => {
    if (chatboxRef.current) {
      chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
    }
  }, [chatMessages]);

  const handleUserSelection = (e) => {
    setUserType(e.target.value);
    setRole("");
    setStep(1);
  };

  const handleRoleSelection = (e) => {
    setRole(e.target.value);
  };

  const handleFacialRecognition = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/facial-recognition"
      );
      if (response.data.status === "success") {
        setMessage(response.data.message);
        setTimeout(() => setStep(2), 1000);
      } else {
        setMessage("Facial recognition failed. Please try again.");
      }
    } catch (error) {
      setMessage("Error connecting to the server. Please try again.");
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/login", {
        username,
        password,
        employeeId,
        userType,
        role,
      });
      if (response.data.status === "success") {
        setMessage(response.data.message);
        setStep(3);
      } else {
        setMessage(response.data.message);
      }
    } catch (error) {
      setMessage("Error connecting to server. Please try again.");
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMessage = { user: query, bot: "Thinking..." };
    setChatMessages((prev) => [...prev, userMessage]);
    setQuery("");

    try {
      const response = await axios.post("http://127.0.0.1:5000/api/query", {
        query,
      });

      setChatMessages((prev) => [
        ...prev.slice(0, -1),
        { user: query, bot: response.data.response },
      ]);
    } catch (error) {
      console.error("Error during chatbot interaction:", error);
      setChatMessages((prev) => [
        ...prev.slice(0, -1),
        {
          user: query,
          bot: "Sorry, I encountered an error. Please try again.",
        },
      ]);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-zinc-900 to-black text-white flex flex-col items-center justify-start">
      {/* Fixed Top Header */}
      <div className="fixed top-0 left-0 w-full bg-gray-900 text-white text-center p-4 shadow-md z-50">
        <h1 className="text-2xl font-bold">ZABIVERSE</h1>
        <p className="text-sm text-gray-300 mbn">
          Your All-in-One Smart Campus Companion
        </p>
      </div>

      {/* Main Content Area */}
      <div className="pt-24 w-full flex justify-center items-center flex-grow p-4">
        {step < 3 ? (
          <div className="bg-zinc-800 rounded-2xl shadow-lg p-8 w-full max-w-lg space-y-4">
            {message && <p className="text-center text-red-400">{message}</p>}

            {step === 0 && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm mb-1">Select User Type</label>
                  <select
                    value={userType}
                    onChange={handleUserSelection}
                    className="w-full p-2 rounded bg-zinc-700 text-white border border-zinc-600"
                  >
                    <option value="">Select User Type</option>
                    <option value="Student">Student</option>
                    <option value="Faculty">Faculty</option>
                    <option value="Management">Management</option>
                    <option value="Higher Management">Higher Management</option>
                  </select>
                </div>
                {userType && userType !== "Student" && (
                  <div>
                    <label className="block text-sm mb-1">Select Role</label>
                    <select
                      value={role}
                      onChange={handleRoleSelection}
                      className="w-full p-2 rounded bg-zinc-700 text-white border border-zinc-600"
                    >
                      <option value="">Select Role</option>
                      <option value="Teacher">Teacher</option>
                      <option value="Program Manager">Program Manager</option>
                      <option value="Head of Department">
                        Head of Department
                      </option>
                      <option value="Finance">Finance</option>
                      <option value="Examination">Examination</option>
                      <option value="Department">Department</option>
                      <option value="VP">Vice President</option>
                      <option value="President">President</option>
                    </select>
                  </div>
                )}
              </div>
            )}

            {step === 1 && userType !== "Student" && (
              <div className="space-y-4">
                <h2 className="text-xl font-medium">Facial Recognition</h2>
                <Webcam className="rounded-lg border border-zinc-600" />
                <button
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded"
                  onClick={handleFacialRecognition}
                >
                  Start Recognition
                </button>
              </div>
            )}

            {step === 1 && userType === "Student" && (
              <form onSubmit={handleLogin} className="space-y-4">
                <div>
                  <label className="block text-sm mb-1">Username</label>
                  <input
                    type="text"
                    className="w-full p-2 rounded bg-zinc-700 text-white border border-zinc-600"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm mb-1">Password</label>
                  <input
                    type="password"
                    className="w-full p-2 rounded bg-zinc-700 text-white border border-zinc-600"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 rounded"
                >
                  Login
                </button>
              </form>
            )}
          </div>
        ) : (
          <div className="bg-zinc-800 rounded-2xl shadow-lg w-full max-w-5xl h-[85vh] flex flex-col">
            <div
              className="flex-1 overflow-y-auto mb p-4 space-y-4"
              ref={chatboxRef}
            >
              {chatMessages.map((msg, index) => (
                <div key={index} className="space-y-4">
                  <div className="flex justify-end mb">
                    <div className="max-w-[80%]">
                      <div className="text-xs text-zinc-400 ">You:</div>
                      <div className="bg-blue-600 text-white p-3 rounded-xl rounded-br-none shadow-lg">
                        {msg.user}
                      </div>
                    </div>
                  </div>
                  <div className="flex justify-start mb">
                    <div className="max-w-[80%]">
                      <div className="text-xs text-zinc-400 mb-1">
                        Zabiverse:
                      </div>
                      <div className="bg-zinc-700 text-white p-3 rounded-xl rounded-bl-none shadow-lg">
                        {msg.bot}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <form
              onSubmit={handleChatSubmit}
              className="p-4 border-t border-zinc-700 bg-zinc-800/90 backdrop-blur-sm"
            >
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask me anything about ZABIVERSE..."
                  className="flex-1 p-3 text-sm rounded-xl bg-zinc-700 text-white border border-zinc-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  type="submit"
                  className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-lg"
                >
                  Send
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
