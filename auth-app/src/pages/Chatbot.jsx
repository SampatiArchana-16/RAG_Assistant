import { useState } from "react";

import axios from "axios";

function Chatbot() {

    const [file, setFile] = useState(null);

    const [question, setQuestion] = useState("");

    const [messages, setMessages] = useState([]);

    const askQuestion = async () => {

        if (!file) {
            alert("Upload PDF");
            return;
        }

        if (!question) {
            return;
        }

        const userMessage = {
            sender: "user",
            text: question
        };

        setMessages((prev) => [
            ...prev,
            userMessage
        ]);

        try {

            const formData = new FormData();

            formData.append("pdf", file);

            formData.append(
                "question",
                question
            );

            const response = await axios.post(
                "http://127.0.0.1:8000/chat/ask",
                formData
            );

            const botMessage = {
                sender: "bot",
                text: response.data.answer
            };

            setMessages((prev) => [
                ...prev,
                botMessage
            ]);

            setQuestion("");

        } catch (error) {

            const botMessage = {
                sender: "bot",
                text: "Error getting answer"
            };

            setMessages((prev) => [
                ...prev,
                botMessage
            ]);
        }
    };

    return (

        <div style={{ padding: "20px" }}>

            <h1>
                AI PDF Chatbot 🤖
            </h1>

            <input
                type="file"
                accept=".pdf"
                onChange={(e) =>
                    setFile(
                        e.target.files[0]
                    )
                }
            />

            <br /><br />

            <div
                style={{
                    border: "1px solid gray",
                    minHeight: "400px",
                    padding: "20px",
                    borderRadius: "10px"
                }}
            >

                {
                    messages.map(
                        (msg, index) => (

                            <div
                                key={index}
                                style={{
                                    textAlign:
                                        msg.sender === "user"
                                        ? "right"
                                        : "left",

                                    marginBottom: "20px"
                                }}
                            >

                                <div
                                    style={{
                                        display: "inline-block",
                                        padding: "10px",
                                        borderRadius: "10px",
                                        background:
                                            msg.sender === "user"
                                            ? "#cfe2ff"
                                            : "#e2e2e2",

                                        maxWidth: "70%"
                                    }}
                                >

                                    <b>
                                        {
                                            msg.sender === "user"
                                            ? "You"
                                            : "Bot"
                                        }
                                        :
                                    </b>

                                    <br />

                                    {msg.text}

                                </div>

                            </div>
                        )
                    )
                }

            </div>

            <br />

            <input
                type="text"
                placeholder="Type message..."
                value={question}
                onChange={(e) =>
                    setQuestion(
                        e.target.value
                    )
                }
                style={{
                    width: "400px",
                    padding: "10px"
                }}
            />

            <button
                onClick={askQuestion}
                style={{
                    marginLeft: "10px",
                    padding: "10px"
                }}
            >
                Send
            </button>

        </div>
    );
}

export default Chatbot;