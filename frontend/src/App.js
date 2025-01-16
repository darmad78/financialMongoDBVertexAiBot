import React, { useState } from "react";
import './App.css';
import ReactJson from 'react-json-view';  // Ensure you have installed react-json-view

function App() {
    const [message, setMessage] = useState("");
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [statusMessage, setStatusMessage] = useState(""); // Status for loading data
    const [messages, setMessages] = useState([]); // Chat history
    const [input, setInput] = useState(""); // User input
    const [data, setData] = useState(null); // Store loaded data
    const [showData, setShowData] = useState(true); // State for controlling data visibility

    const loadData = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/load_client", {
                method: "POST",
            });
            const result = await response.json();
            console.log(result);  // Log the full response to check for any issues
            setMessage(result.message);  // Show success or failure message
            setData(result.data);  // Set the loaded data to state (assuming `data` is part of the response)
        } catch (error) {
            console.error("Error:", error);  // Log any errors that occur
            setMessage("Failed to update data. Please try again.");
        }
    };

    const askQuestion = async () => {
        if (!input.trim()) return; // Prevent sending empty input

        const userMessage = { sender: "user", text: input };
        setMessages((prevMessages) => [...prevMessages, userMessage]); // Add user's message to the chat

        try {
            const response = await fetch("http://127.0.0.1:8000/ask_question/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question: input }),
            });
            const result = await response.json();

            const botMessage = {
                sender: "bot",
                text: result.answer || "Sorry, I couldn't find an answer.",
            };
            setMessages((prevMessages) => [...prevMessages, botMessage]); // Add bot's response to the chat
        } catch (error) {
            const errorMessage = {
                sender: "bot",
                text: "Failed to process your question. Please try again.",
            };
            setMessages((prevMessages) => [...prevMessages, errorMessage]);
        }

        setInput(""); // Clear the input field
    };

    const clearChat = () => {
        setMessages([]); // Clear chat messages
    };

    const toggleDataVisibility = () => {
        setShowData(prev => !prev);  // Toggle the state for data visibility
    };

    // Function to format the message and handle newlines
    const formatMessage = (msg) => {
        if (!msg) return null; // Return null if no message
        const formattedMsg = msg.split("\n").join("<br />"); // Replace \n with <br />
        return { __html: formattedMsg }; // Return HTML for rendering
    };

    return (
        <div className="App">
            <h1 className="title">Client Financial Assistant</h1> {/* Title */}

            <div className="chat-container">
                {/* Chatbox for displaying messages */}
                <div className="chatbox">
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`message ${msg.sender === "user" ? "user" : "bot"}`}
                            dangerouslySetInnerHTML={formatMessage(msg.text)} // Insert the formatted HTML here
                        />
                    ))}
                </div>

                {/* Input Area for asking questions */}
                <div className="input-area">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask a question..."
                    />
                    <button onClick={askQuestion}>Send</button>
                </div>

                {/* Clear Chat Button */}
                <button onClick={clearChat} className="clear-chat-btn">
                    Clear Chat
                </button>

                {/* Buttons for loading and showing data */}
                <div className="buttons-container">
                    <button onClick={loadData} className="load-data-btn">
                        Load Data into MongoDB
                    </button>
                    <button onClick={toggleDataVisibility} className="toggle-data-btn">
                        {showData ? "Hide Data" : "Show Data"}
                    </button>
                </div>

                {/* Status and message display */}
                <p className="status-message">{statusMessage}</p>
                {message && <p className="status-message">{message}</p>} {/* Display status or any additional message */}

                {/* Data display area */}
                {showData && data && (
                    <div className="data-and-question-container">
                        <div className="loaded-data">
                            <h3>Loaded Data:</h3>
                            <ReactJson src={data} theme="monokai" collapsed={false} />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;